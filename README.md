# Python Multicast Network
## Tubes Jaringan Komputer Semester 4

### Langkah penggunaan:
1. Buka 2 konsol sebagai receiver B dan C lalu jalankan perintah ini \
   `python receiver.py --port 5000`
2. Buka 1 konsol sebagai sender A
3. Kirim kalimat \
   `python sender.py --type text --content "Halo B dan C" --port 5000`
4. Kirim kalimat panjang \
   `python sender.py --type text --content "Ini adalah kalimat yang sangat panjang yang dikirim melalui UDP multicast dari A ke B dan C dalam rangka pengujian." --port 5000`
5. Kirim 1 paragraf \
   `python sender.py --type text --content "Ini adalah satu paragraf yang dikirim melalui multicast. Paragraf ini menjelaskan bagaimana data UDP multicast bekerja. Data ini dikirim oleh A dan diterima oleh B dan C dalam jaringan lokal yang sama." --port 5000`
6. Kirim dokumen \
   `python sender.py --type file --content dokumen.pdf --port 5000`
7. Kirim gambar \
   `python sender.py --type file --content gambar.png --port 5000`
8. Kirim audio \
   `python sender.py --type file --content audio.mp3 --port 5000`
9. Kirim video \
   `python sender.py --type file --content video.mp4 --port 5000`
