import socket

def start_server(host='127.0.0.1', port=65432):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            # Wait for a client connection
            client_socket, addr = server_socket.accept()
            with client_socket:
                print(f"Connected by {addr}")
                data = client_socket.recv(1024)
                if not data:
                    break
                # Convert the received data to uppercase
                response = data.decode().upper()
                # Send the uppercase string back to the client
                client_socket.sendall(response.encode())

if __name__ == "__main__":
    start_server()
