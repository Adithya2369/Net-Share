import socket
import os
import sys


def send_file(ip, file_path):
    port = 5001

    print(f"send_file called with IP: {ip}, File Path: {file_path}")

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")

        file_name = os.path.basename(file_path)
        print(f"Opening file: {file_name}")
        file_size = os.path.getsize(file_path)
        print(f"File size: {file_size} bytes")


        with open(file_path, 'rb') as file:
            file_size = os.path.getsize(file_path)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((ip, port))

                # Send file size (8 bytes)
                client.sendall(file_size.to_bytes(8, 'big'))

                # Send filename metadata
                client.sendall(len(file_name).to_bytes(4, 'big'))
                client.sendall(file_name.encode('utf-8'))

                print(f"Sending file data for: {file_name}")
                # Send file data
                while True:
                    data = file.read(4096)
                    if not data:
                        break
                    client.sendall(data)

        print(f"File {file_name} sent successfully")
        return True

    except Exception as e:
        error_message = str(e)
        if isinstance(e, FileNotFoundError):
            error_message = f"Error: File not found at {file_path}"
        elif isinstance(e, ConnectionRefusedError):
            error_message = f"Error: Connection refused to {ip}:{port}. Make sure the receiver is running."
        print(f"Error: {e}", file=sys.stderr)
        # In a real application, you'd likely return more structured error info.
        # For this diff, we'll just print. The change requested is about
        # app_functions.send_files handling this, which is outside this diff.
        pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python sender.py <target_ip> <file_path>")
        sys.exit(1)

    target_ip = sys.argv[1]
    print(target_ip)
    file_path = sys.argv[2]
    print(file_path)
    send_file(target_ip, file_path)
