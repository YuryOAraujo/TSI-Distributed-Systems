import socket

content = input('Digite a sua mensagem: ')

def start_client(host='127.0.0.1', port=65432, message=content):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((host, port))
        # Send the message to the server
        client_socket.sendall(message.encode())
        # Receive the response from the server
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode()}")

if __name__ == "__main__":
    start_client()
