import socket
import time
import threading
import multiprocessing
import json
import os
import pickle
from collections import OrderedDict
import ssl

class Server:
    def __init__(self, config_file='config.json', cache_file='cache.json'):
        self.load_config(config_file)
        self.functions = {'sum': self.sum, 'sub': self.sub, 'mul': self.mul, 'div': self.div, 'sum_n': self.sum_n, 'wait_n_seconds': self.wait_n_seconds, 'check_primes': self.check_primes, 'check_primes_parallel': self.check_primes_parallel, 'validate_cpf': self.validate_cpf}
        self.mul_cache = {}
        self.cache_file = cache_file
        self.initialize_cache()
        print(f"Server listening on {self.address}:{self.port}")

    def initialize_cache(self):
        if not os.path.exists(self.cache_file):
            with open(self.cache_file, 'wb') as file:
                pickle.dump(OrderedDict(), file)

    def read_cache(self):
        if os.path.getsize(self.cache_file) > 0:
            with open(self.cache_file, 'rb') as file:
                return pickle.load(file)
        return OrderedDict()
    
    def write_cache(self, cache):
        with open(self.cache_file, 'wb') as file:
            pickle.dump(cache, file)

    def manage_cache_size(self):
        cache = self.read_cache()
        while os.path.getsize(self.cache_file) > self.primes_cache_bytes and cache != {}:
            cache.popitem(last=False)
        self.write_cache(cache)

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            self.address = config['server']['address']
            self.port = config['server']['port']
            self.parallelism = config['server']['parallelism']
            self.primes_cache_bytes = config['server']['primes_cache_bytes']
            self.log_file = config['server']['log_file']

    def verify_operation(self, operation):
        operation, *rest = operation.split(' ')
        if operation in ['sum', 'sub', 'mul', 'div']:
            result = self.functions[operation](float(rest[0]), float(rest[1]))
        elif operation == 'check_primes_parallel':
            result = self.check_primes_parallel([int(i) for i in rest[:-1]], int(rest[-1]))
        elif operation == 'wait_n_seconds':
            result = self.wait_n_seconds(int(rest[0]))
        elif operation == 'validate_cpf':
            result = self.validate_cpf(rest[0])
        else:
            result = self.functions[operation]([float(i) for i in rest])
        return str(result)
    
    def wait_n_seconds(self, n):
        time.sleep(n)
        return f'Done waited {n} seconds'

    def sum(self, first, second):
        print(f'Operação regular: {first} + {second}')
        return first + second
    
    def sub(self, first, second):
        return first - second

    def mul(self, first, second):
        if f'{first} * {second}' in self.mul_cache:
            print(f'Operação em cache: {first} * {second}')
            return self.mul_cache[f'{first} * {second}']
        else:
            print(f'Operação regular: {first} * {second}')
            self.mul_cache[f'{first} * {second}'] = first * second
            return self.mul_cache[f'{first} * {second}']

    def div(self, first, second):
        print(f'Operação regular: {first} / {second}')
        if second == 0:
            return 'Unsupported operation'
        return first / second
    
    def sum_n(self, list: list):
        return sum(list)
    
    def is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    def is_prime_cache(self, n):
        cache = self.read_cache()

        if n in cache:
            return cache[n]
        
        cache[n] = self.is_prime(n)
            
        self.write_cache(cache) 
        self.manage_cache_size()

        return cache[n]
    
    def check_primes(self, list: list[int]):
        return [self.is_prime_cache(i) for i in list]
    
    def check_primes_parallel(self, list: list[int], n_process: int):
        with multiprocessing.Pool(n_process) as pool:
            return pool.map(self.is_prime_cache, list)
        
    def validate_cpf(self, cpf):
        cpf = ''.join(filter(str.isdigit, cpf))

        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        def calculate_digit(cpf, factor):
            total = sum(int(cpf[i]) * (factor - i) for i in range(factor - 1))
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder

        first_digit = calculate_digit(cpf, 10)
        second_digit = calculate_digit(cpf, 11)

        return int(cpf[9]) == first_digit and int(cpf[10]) == second_digit
    
    def generate_log(self, register):
        with open(self.log_file, 'a') as file:
            file.write(register)

    def handle_client(self, client_socket, addr):
        initial_time = time.time()
        print(f"New connection from {addr}")
        data = ''
        with client_socket:
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                chunk_str = chunk.decode()
                if '\0' in chunk_str:
                    data += chunk_str.replace('\0', '')
                    break
                data += chunk_str

            operation = data
            result = self.verify_operation(operation)
            client_socket.sendall(result.encode())
        elapsed_time = max(time.time() - initial_time, 0.01)
        register = f'{initial_time}, {addr[0]}, {operation.split(' ')[0]}, {elapsed_time:.2f}\n'
        self.generate_log(register)
        print(f"Connection from {addr} closed.")

    def start(self):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.address, self.port))
            server_socket.listen()
            print(f"Server listening on {self.address}:{self.port}")

            with context.wrap_socket(server_socket, server_side=True) as ssl_socket:
                while True:
                    client_socket, addr = ssl_socket.accept()
                    if self.parallelism == 'thread':
                        client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                        client_thread.start()
                    elif self.parallelism == 'process':
                        client_process = multiprocessing.Process(target=self.handle_client, args=(client_socket, addr))
                        client_process.start()

if __name__ == "__main__":
    server = Server()
    server.start()
