# Python Multicast Network
## Tubes Jaringan Komputer Semester 4

### Langkah penggunaan:
1. Buka 2 konsol sebagai receiver B dan C lalu jalankan perintah ini
   `python receiver.py --port 5000  # Receiver B
   python receiver.py --port 5001  # Receiver C`
3. Buka 1 konsol sebagai sender A lagi lalu jalankan perintah ini untuk mengirim data ke receiver B
   `python sender.py --type text --content "Halo B, ini pesan singkat" --port 5000`
4. Pada konsol sender A jalankan perintah ini untuk mengirim data ke receiver C
   `python sender.py --type file --content gambar.png --port 5001`
