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
        data = client_socket.recv(1024)
        return data.decode()

    def format_message(self, operator, first, second):
        client_socket = self.start()
        operation = str(operator) + str(first) + ' ' + str(second)
        return self.send_message(client_socket, operation)
    
    def wait_n_seconds(self, n):
        return self.format_message('& ', n, 0)

    def sum(self, first, second):
        return self.format_message('+ ', first, second)
    
    def sum_n(self, list: list):
        client_socket = self.start()
        operation = '# ' + ' '.join(map(str, list))
        return self.send_message(client_socket, operation)
        
    def mul(self, first, second):
        return self.format_message('* ', first, second)

    def div(self, first, second):
        return self.format_message('/ ', first, second)

    def sub(self, first, second):
        return self.format_message('- ', first, second)