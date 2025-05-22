import socket
import argparse
import os

def send_file(file_path, host, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((host, port))

  filename = os.path.basename(file_path)
  filesize = os.path.getsize(file_path)

  # Kirim nama file dan ukuran
  sock.sendall(f"{filename}|{filesize}".encode() + b'\n')

  # Kirim isi file
  with open(file_path, 'rb') as f:
    while chunk := f.read(4096):
      sock.sendall(chunk)

  print(f"File {filename} berhasil dikirim ke {host}:{port}")
  sock.close()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--file', required=True)
  parser.add_argument('--host', default='localhost')
  parser.add_argument('--port', type=int, required=True)
  args = parser.parse_args()

  send_file(args.file, args.host, args.port)
