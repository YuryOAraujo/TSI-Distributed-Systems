import socket
import json

class Client:
    def __init__(self, server_address='127.0.0.1', server_port=65432):
        self.server_address = server_address
        self.server_port = server_port

    def start(self):
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
        client_socket = self.start()
        operation = str(operator) + str(first) + ' ' + str(second)
        return self.send_message(client_socket, operation)
    
    def wait_n_seconds(self, n):
        return self.format_message('wait_n_seconds ', n, 0)

    def sum(self, first, second):
        return self.format_message('sum ', first, second)
    
    def sum_n(self, list: list):
        client_socket = self.start()
        operation = 'sum_n ' + ' '.join(map(str, list))
        return self.send_message(client_socket, operation)
    
    def check_primes(self, list: list[int]):
        client_socket = self.start()
        operation = 'check_primes ' + ' '.join(map(str, list))
        return self.send_message(client_socket, operation)
    
    def check_primes_parallel(self, list: list[int], n_process: int):
        client_socket = self.start()
        operation = 'check_primes_parallel ' + ' '.join(map(str, list)) + ' ' + str(n_process)
        return self.send_message(client_socket, operation)
        
    def mul(self, first, second):
        return self.format_message('mul ', first, second)

    def div(self, first, second):
        return self.format_message('div ', first, second)

    def sub(self, first, second):
        return self.format_message('sub ', first, second)