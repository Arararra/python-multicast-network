import socket
import struct
import json
import sys
from collections import defaultdict

MCAST_GRP = '224.1.1.1'
DELIMITER = b'##HEADER_END##'

received_chunks = defaultdict(dict)
progress_state = {}

def print_progress(name, index, total):
  percent = int((index + 1) / total * 100)
  bar_length = 30
  filled_length = int(bar_length * percent // 100)
  bar = '=' * filled_length + '-' * (bar_length - filled_length)
  sys.stdout.write(f"\r📥 [{bar}] {percent}% menerima file: {name}")
  sys.stdout.flush()

def save_if_complete(header):
  name = header['name']
  total = header['total']
  received = received_chunks[name]

  if len(received) == total:
    print(f"\n💾 Menyusun file '{name}' dari {total} chunk...")
    with open(name, 'wb') as f:
      for i in range(total):
        f.write(received[i])
    print(f"✅ File '{name}' berhasil disimpan!\n")
    del received_chunks[name]
    del progress_state[name]

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
      print("❌ Header delimiter tidak ditemukan.")
      continue

    try:
      header = json.loads(data[:delimiter_index].decode('utf-8'))
      payload = data[delimiter_index + len(DELIMITER):]

      if header['type'] == 'text':
        print(f"\n📩 Pesan teks diterima dari {addr}:\n{payload.decode('utf-8')}\n")

      elif header['type'] == 'file':
        name = header['name']
        index = header['index']
        total = header['total']
        received_chunks[name][index] = payload

        if name not in progress_state:
          progress_state[name] = set()
        progress_state[name].add(index)

        print_progress(name, len(progress_state[name]) - 1, total)
        save_if_complete(header)

    except Exception as e:
      print(f"\n❌ Error parsing data: {e}")
      continue

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('--port', type=int, required=True, help='Port receiver')
  args = parser.parse_args()

  start_receiver(args.port)
