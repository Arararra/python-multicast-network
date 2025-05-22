import socket
import argparse
import os
import json
import time

MCAST_GRP = '224.1.1.1'
CHUNK_SIZE = 50000  # 50KB per chunk
SLEEP_BETWEEN_CHUNKS = 0.01  # optional: delay untuk menghindari packet loss

def send_file(filepath, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

  filename = os.path.basename(filepath)
  filesize = os.path.getsize(filepath)
  total_chunks = (filesize + CHUNK_SIZE - 1) // CHUNK_SIZE

  with open(filepath, 'rb') as f:
    for i in range(total_chunks):
      chunk = f.read(CHUNK_SIZE)
      header = {
        'type': 'file',
        'name': filename,
        'index': i,
        'total': total_chunks
      }
      message = json.dumps(header).encode('utf-8') + b'##HEADER_END##' + chunk
      sock.sendto(message, (MCAST_GRP, port))
      time.sleep(SLEEP_BETWEEN_CHUNKS)

  print(f"✅ File '{filename}' berhasil dikirim dalam {total_chunks} chunk!")

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--content', required=True, help='Path ke file')
  parser.add_argument('--port', type=int, required=True)
  args = parser.parse_args()

  send_file(args.content, args.port)
