import socket
import time
import threading
import multiprocessing
import json

class Server:
    def __init__(self, config_file='rpc/config.json'):
        self.load_config(config_file)
        self.functions = {'+': self.sum, '-': self.sub, '*': self.mul, '/': self.div, '#': self.sum_n, '&': self.wait_n_seconds}
        print(f"Server listening on {self.address}:{self.port}")

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            self.address = config['server']['address']
            self.port = config['server']['port']
            self.parallelism = config['server']['parallelism']

    def verify_operation(self, operation):
        operation, *rest = operation.split(' ')
        if operation != '#' and operation != '&':
            result = self.functions[operation](float(rest[0]), float(rest[1]))
        elif operation == '&':
            result = self.wait_n_seconds(int(rest[0]))
        else:
            result = self.functions[operation]([float(i) for i in rest])
        return str(result)
    
    def wait_n_seconds(self, n):
        time.sleep(n)
        return f'Done waited {n} seconds'


    def sum(self, first, second):
        return first + second
    
    def sub(self, first, second):
        return first - second

    def mul(self, first, second):
        return first * second

    def div(self, first, second):
        if second == 0:
            return 'Unsupported operation'
        return first / second
    
    def sum_n(self, list: list):
        return sum(list)

    def handle_client(self, client_socket, addr):
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
        print(f"Connection from {addr} closed.")

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.address, self.port))
            server_socket.listen()
            print(f"Server listening on {self.address}:{self.port}")

            while True:
                client_socket, addr = server_socket.accept()
                if self.parallelism == 'thread':
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                    client_thread.start()
                elif self.parallelism == 'process':
                    client_process = multiprocessing.Process(target=self.handle_client, args=(client_socket, addr))
                    client_process.start()

if __name__ == "__main__":
    server = Server()
    server.start()
