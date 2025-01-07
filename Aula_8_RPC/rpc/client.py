import socket
import json
import random
import pickle

class Client:
    def __init__(self, config_file='rpc/config.json'):
        self.load_config(config_file)
        self.server_address = ''
        self.server_port = ''
        self.sum_cache = {}
        self.div_cache = {}

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            self.div_cache_n = config['client']['div_cache_n']
            self.dns_address = config['dns_server']['address']
            self.dns_address_port = config['dns_server']['port']

    def handle_domain(self, operation):
        self.server_address = ''
        self.server_port = ''
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(operation.encode(), (self.dns_address, self.dns_address_port))
        domains = []
        data, _ = client_socket.recvfrom(1024)

        domains = pickle.loads(data)
        operation_server = random.choice(domains)
        return operation_server.split(':')[0], int(operation_server.split(':')[1])

    def start(self, operation):
        self.server_address, self.server_port = self.handle_domain(operation)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_address, self.server_port))
        return client_socket
        
    def send_message(self, client_socket, operation):
        operation += '\0'
        client_socket.sendall(operation.encode())
        
        data = ''
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            chunk_str = chunk.decode()
            if '\0' in chunk_str:
                data += chunk_str.split('\0')[0]
                break
            data += chunk_str
        
        return data

    def format_message(self, operator, first, second):
        client_socket = self.start(operator)
        operation = str(operator) + str(first) + ' ' + str(second)
        return self.send_message(client_socket, operation)
    
    def wait_n_seconds(self, n):
        return self.format_message('wait_n_seconds ', n, 0)

    def sum(self, first, second):
        if f'{first} + {second}' in self.sum_cache:
            return self.sum_cache[f'{first} + {second}']
        else:
            self.sum_cache[f'{first} + {second}'] = self.format_message('sum ', first, second)
            return self.sum_cache[f'{first} + {second}']
    
    def sum_n(self, list: list):
        client_socket = self.start('sum_n')
        operation = 'sum_n ' + ' '.join(map(str, list))
        return self.send_message(client_socket, operation)
    
    def check_primes(self, list: list[int]):
        client_socket = self.start('check_primes')
        operation = 'check_primes ' + ' '.join(map(str, list))
        return self.send_message(client_socket, operation)
    
    def check_primes_parallel(self, list: list[int], n_process: int):
        client_socket = self.start('check_primes_parallel')
        operation = 'check_primes_parallel ' + ' '.join(map(str, list)) + ' ' + str(n_process)
        return self.send_message(client_socket, operation)
        
    def mul(self, first, second):
        return self.format_message('mul ', first, second)

    def div(self, first, second):
        if len(self.div_cache) == self.div_cache_n:
            first_key = next(iter(self.div_cache))
            del self.div_cache[first_key]
        if f'{first} / {second}' in self.div_cache:
            return self.div_cache[f'{first} / {second}']
        else:
            self.div_cache[f'{first} / {second}'] = self.format_message('div ', first, second)
            return self.div_cache[f'{first} / {second}']

    def sub(self, first, second):
        return self.format_message('sub ', first, second)
    
    def validate_cpf(self, cpf):
        client_socket = self.start('validate_cpf')
        operation = 'validate_cpf ' + cpf
        return self.send_message(client_socket, operation)