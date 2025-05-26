import socket
import os
from threading import Thread
from datetime import datetime


def log_activity(message):
    with open('activity.log', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")


def recv_all(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


def handle_client(client_socket, addr):
    try:
        # Receive file size
        file_size_bytes = recv_all(client_socket, 8)
        if not file_size_bytes:
            return
        file_size = int.from_bytes(file_size_bytes, 'big')

        # Receive filename size
        filename_size_bytes = recv_all(client_socket, 4)
        if not filename_size_bytes:
            return

        # Receive filename
        file_name = recv_all(client_socket, filename_size).decode('utf-8')

        # Create downloads directory
        os.makedirs('downloads', exist_ok=True)

        # Receive file data
        file_path = os.path.join('downloads', file_name)
        received_size = 0
        with open(file_path, 'wb') as file:
            while received_size < file_size:
                data = client_socket.recv(4096)
                if not data:
                    break
                file.write(data)
                received_size += len(data)

        # Optional: Add a check here to see if received_size == file_size

        log_activity(f"Received file: {file_name}")
        print(f"File {file_name} received from {addr[0]}")

    except Exception as e:
        log_activity(f"Error handling client {addr[0]}:{addr[1]}: {str(e)}")
        print(f"Error: {e}")
    finally:
        client_socket.close()


def start_server():
    host = '0.0.0.0'
    port = 5001
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    log_activity(f"Receiver server started on {host}:{port}")
    print(f"[*] Listening on {host}:{port}")

    try:
        while True:
            client, addr = server.accept()
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
            Thread(target=handle_client, args=(client, addr)).start()
    except KeyboardInterrupt:
        print("\n[*] Shutting down receiver server")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()
