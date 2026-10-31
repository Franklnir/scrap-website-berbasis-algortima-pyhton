# Hasil pengujian ScrapMCP 1.0

Tanggal: 31 Oktober 2026. Lingkungan: Linux, Python 3.12.

## Dijalankan dan lulus

- `python -m pytest -q`: **19 passed**.
- Pipeline fixture HTML: ekstraksi, regex, folder, JSON/CSV/Markdown, PDF dan ZIP.
- PDF sintetis diparse melalui engine yang sama.
- Duplikasi dan penulisan paralel; nama kategori aman Windows.
- Hash setiap file dalam manifest ZIP diperiksa terhadap byte hasil ekstraksi.
- URL lokal, kredensial di URL, port nonweb, redirect privat dan respons terlalu besar ditolak.
- HTTP 403 diteruskan dengan status yang benar.
- MCP lokal: WebSocket sungguhan, initialize, tools/list, tools/call, validasi argumen, scraping simulasi, kandidat riset/konfirmasi, backup, ping, dan sesi baru setelah putus.
- Build menghasilkan wheel `py3-none-any` dan source distribution.
- Instalasi wheel dalam venv baru diuji dari luar folder source: perintah versi, demo, dan pip check.
- PDF proyek 5 halaman dan rekap dataset 1 halaman diperiksa melalui render.

## Belum diverifikasi langsung

- OS Windows: tidak tersedia di lingkungan ini. Workflow CI Windows/Linux disertakan, belum dijalankan pada GitHub.
- Akun/endpoint Xiaozhi asli: tidak diberikan. Uji transport menggunakan peer lokal simulasi.
- Scraping live: percobaan docs.python.org gagal dengan `Temporary failure in name resolution` pada jaringan lingkungan ini.
- Keberhasilan live Jina, YouTube, CrossRef, arXiv, Semantic Scholar bergantung jaringan dan layanan sumber.

Tes offline membuktikan perilaku kode pada fixture dan respons simulasi, bukan keberhasilan semua sumber internet.
