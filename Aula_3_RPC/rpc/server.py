import socket

class Server:
    def __init__(self, address='127.0.0.1', port=65432):
        self.address = address
        self.port = port
        self.functions = {'+': self.sum, '-': self.sub, '*': self.mul, '/': self.div, '#': self.sum_n}
        print(f"Server listening on {self.address}:{self.port}")

    def verify_operation(self, operation):
        operation, *rest = operation.split(' ')
        if operation != '#':
            result = self.functions[operation](float(rest[0]), float(rest[1]))
        else:
            result = self.functions[operation]([float(i) for i in rest])
        return str(result)

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

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.address, self.port))
            server_socket.listen()

            while True:
                client_socket, addr = server_socket.accept()
                with client_socket:
                    data = ''
                    while True:
                        chunk = client_socket.recv(1024)
                        chunk_str = chunk.decode()
                        if '\0' in chunk_str:
                            data += chunk_str.replace('\0', '')
                            break
                        data += chunk_str
                    
                    operation = data
                    result = self.verify_operation(operation)
                    client_socket.sendall(result.encode())