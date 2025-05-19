import socket
import os
import sys


def send_file(ip, file_path):
    port = 5001
    client = None

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")

        file_name = os.path.basename(file_path)

        with open(file_path, 'rb') as file:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((ip, port))

                # Send filename metadata
                client.sendall(len(file_name).to_bytes(4, 'big'))
                client.sendall(file_name.encode('utf-8'))

                # Send file data
                while True:
                    data = file.read(4096)
                    if not data:
                        break
                    client.sendall(data)

        print(f"File {file_name} sent successfully")
        return True

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python sender.py <target_ip> <file_path>")
        sys.exit(1)

    target_ip = sys.argv[1]
    file_path = sys.argv[2]
    send_file(target_ip, file_path)
