import socket
import struct
import json
import os
from collections import defaultdict

MCAST_GRP = '224.1.1.1'
DELIMITER = b'##HEADER_END##'

# Struktur penyimpanan sementara: {filename: {index: data}}
received_chunks = defaultdict(dict)
chunk_counters = {}

def save_if_complete(header):
  name = header['name']
  total = header['total']
  received = received_chunks[name]

  if len(received) == total:
    print(f"💾 Menyusun file '{name}' dari {total} chunk...")
    with open(name, 'wb') as f:
      for i in range(total):
        f.write(received[i])
    print(f"✅ File '{name}' berhasil disimpan!")
    del received_chunks[name]

def start_receiver(port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind(('', port))

  mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

  print(f"📡 Receiver aktif di port {port} dan group {MCAST_GRP}...\n")

  while True:
    data, addr = sock.recvfrom(65536)

    delimiter_index = data.find(DELIMITER)
    if delimiter_index == -1:
      print("❌ Delimiter tidak ditemukan, data diabaikan.")
      continue

    try:
      header = json.loads(data[:delimiter_index].decode('utf-8'))
      payload = data[delimiter_index + len(DELIMITER):]

      if header['type'] == 'file':
        name = header['name']
        index = header['index']
        total = header['total']
        received_chunks[name][index] = payload

        print(f"📥 Chunk {index+1}/{total} dari {name} diterima ({addr})")

        save_if_complete(header)

    except Exception as e:
      print(f"❌ Error memproses data: {e}")
      continue

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('--port', type=int, required=True, help='Port receiver')
  args = parser.parse_args()

  start_receiver(args.port)
