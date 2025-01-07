import socket
import json
import pickle

class DNSServer:
    def __init__(self, config_file='config.json'):
        self.load_config(config_file)
        self.start()

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            self.address = config['dns_server']['address']
            self.port = config['dns_server']['port']
            self.servers = config['dns_server']['servers']

    def start(self):
        dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dns_socket.bind((self.address, self.port))
        print(f"DNS Server listening on {self.address}:{self.port}")

        while True:
            operation, client_address = dns_socket.recvfrom(1024)
            operation_str = operation.decode().replace(' ', '')
            if operation_str in self.servers:
                data = pickle.dumps(self.servers[operation_str])
                dns_socket.sendto(data, client_address)

if __name__ == "__main__":
    server = DNSServer()
    server.start()