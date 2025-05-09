import socket
import argparse
import os
import json

MCAST_GRP = '224.1.1.1'

def send_data(data_type, content, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

  if data_type == 'text':
    header = json.dumps({'type': 'text'}).encode()
    payload = content.encode()
  else:
    with open(content, 'rb') as f:
      payload = f.read()
    header = json.dumps({
      'type': 'file',
      'name': os.path.basename(content)
    }).encode()

  message = header + b'\n' + payload
  sock.sendto(message, (MCAST_GRP, port))
  print(f"Data berhasil dikirim ke port {port}!")

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--type', choices=['text', 'file'], required=True)
  parser.add_argument('--content', required=True)
  parser.add_argument('--port', type=int, required=True)
  args = parser.parse_args()

  send_data(args.type, args.content, args.port)
