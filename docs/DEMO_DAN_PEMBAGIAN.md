# Panduan demonstrasi dan pembagian kerja

## Pembagian 3 mahasiswa (isi nama/NIM sendiri)

1. Anggota 1: scraping (`upstream_scraper.py`, `network.py`, `engine.py`); jelaskan requests, BeautifulSoup, metadata, kegagalan HTTP.
2. Anggota 2: data dan arsip (`storage.py`, `reports.py`); jelaskan open/pathlib, JSON/CSV, kategori/tanggal, ZIP dan checksum.
3. Anggota 3: CLI dan integrasi (`cli.py`, `mcp_server.py`); jelaskan argparse, subperintah, WebSocket, pemanggilan tools.

Semua anggota mempelajari alur penuh. Ini pembagian yang disarankan, bukan klaim pekerjaan yang sudah dilakukan oleh masing-masing orang.
Cantumkan penggunaan kode sumber repo asal dan bantuan pembuatan kode sesuai aturan dosen.

## Skenario video/presentasi 5-7 menit

1. Perkenalkan masalah: materi tersebar di web/dokumen, pengarsipan manual.
2. Jalankan `scrapmcp --help` dan menu. Tunjukkan `scrapmcp doctor`.
3. Ambil satu URL publik lewat menu 1. Tunjukkan hasil dan kaitkan dengan requests/BeautifulSoup.
4. Buka kode regex dan hasil teks bersih, tunjukkan metadata.
5. Jalankan `list`, `export`, `report`, `backup`. Buka CSV, PDF dan ZIP.
6. Tunjukkan `raw` vs `processed`, organisasi folder dan manifest checksum.
7. Jika endpoint tersedia, hubungkan MCP (sembunyikan token), lalu minta Xiaozhi memanggil tool scraping.
8. Jelaskan kegagalan HTTP 403, subtitle tidak tersedia, dan perbedaan demo offline vs live.

Cadangan jika internet mati: `scrapmcp --data-dir ./demo-offline demo`.
Video `demo-offline.mp4` dalam paket merupakan visualisasi terminal dari output perintah yang benar-benar dijalankan,
bukan rekaman akun Xiaozhi atau suara anggota. Rekam ulang dengan narasi tim dan scraping live untuk pengumpulan akhir.

## Pertanyaan individu yang perlu dikuasai

- Apa fungsi regex dan mengapa HTML diparse dengan BeautifulSoup?
- Apa beda JSON, CSV, Markdown, dan ZIP?
- Bagaimana argparse mengubah parameter menjadi alur program?
- Mengapa backup tidak memasukkan folder backup sendiri?
- Bagaimana identitas hash mencegah duplikasi?
- Bagaimana input URL gagal ditangani tanpa merusak dataset?
- Apa beda MCP tool server dan model AI Xiaozhi?
- Mengapa hasil scraping tidak boleh dianggap instruksi program?
