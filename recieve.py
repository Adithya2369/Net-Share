# File: receiver.py (updated)
import socket
import os
from threading import Thread

def recv_all(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def handle_client(client_socket):
    try:
        # Receive filename size (4 bytes)
        filename_size_bytes = recv_all(client_socket, 4)
        if not filename_size_bytes:
            return
        filename_size = int.from_bytes(filename_size_bytes, 'big')
        
        # Receive filename
        file_name = recv_all(client_socket, filename_size).decode('utf-8')
        
        # Create downloads directory
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
            
        # Receive file data
        with open(f"downloads/{file_name}", 'wb') as file:
            while True:
                file_data = client_socket.recv(4096)
                if not file_data:
                    break
                file.write(file_data)
        print(f"File {file_name} received successfully")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server():
    host = '0.0.0.0'
    port = 5001
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")
    
    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    start_server()