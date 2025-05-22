import socket
import os

def start_receiver(port):
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind(('', port))
  server.listen(1)
  print(f"Receiver aktif di port {port}...")

  conn, addr = server.accept()
  print(f"Koneksi diterima dari {addr}")

  # Terima metadata
  header = b""
  while not header.endswith(b'\n'):
    header += conn.recv(1)
  filename, filesize = header.decode().strip().split('|')
  filesize = int(filesize)

  # Simpan file
  with open(filename, 'wb') as f:
    received = 0
    while received < filesize:
      data = conn.recv(4096)
      if not data:
        break
      f.write(data)
      received += len(data)

  print(f"File {filename} berhasil diterima dan disimpan.")
  conn.close()
  server.close()

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('--port', type=int, required=True)
  args = parser.parse_args()

  start_receiver(args.port)
