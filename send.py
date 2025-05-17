# File: sender.py (updated)
import socket
import os


def send_file():
    target_ip = input("Enter target IP: ")
    file_path = input("Enter file path: ").strip('"')
    file_path = os.path.normpath(file_path)
    port = 5001
    client = None

    try:
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found")
            return

        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as file:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((target_ip, port))

            # Send filename metadata
            client.sendall(len(file_name).to_bytes(4, 'big'))
            client.sendall(file_name.encode('utf-8'))

            # Send file data
            while True:
                data = file.read(4096)
                if not data:
                    break
                client.sendall(data)

            print("File sent successfully")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if client:
            client.close()


if __name__ == "__main__":
    send_file()
