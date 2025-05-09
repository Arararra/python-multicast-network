import socket
import struct
import json

def start_receiver(port):
  MCAST_GRP = '224.1.1.1'
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind(('', port))

  mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

  print(f"Receiver aktif di port {port} dan group {MCAST_GRP}...")

  while True:
    data, addr = sock.recvfrom(65536)
    header_end = data.find(b'\n')
    if header_end == -1:
      continue

    header = json.loads(data[:header_end])
    payload = data[header_end+1:]

    print(f"\nData diterima oleh port {port} dari {addr}")
    if header['type'] == 'text':
      print("Isi data:")
      print(payload.decode())
    elif header['type'] == 'file':
      filename = header['name']
      with open(filename, 'wb') as f:
        f.write(payload)
      print(f"File {filename} berhasil disimpan!")

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('--port', type=int, required=True, help='Port receiver')
  args = parser.parse_args()

  start_receiver(args.port)
