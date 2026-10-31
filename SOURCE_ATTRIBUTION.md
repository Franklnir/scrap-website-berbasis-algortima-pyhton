# Sumber dan perubahan

Proyek ini dibuat atas permintaan pemilik repo untuk memisahkan teknologi scraping menjadi aplikasi CLI tugas kelompok.

- Repo asal: https://github.com/Franklnir/xiaozhi-knowledge-base
- Snapshot commit yang diperiksa: `30d1a7fe99a21c6cceacc736ec677b808df40850`
- File asal: `xiaozhi/services/scraper_service.py`
- Git blob SHA: `32680d9ae35a18b7d381c8b7749c9571ed963142`
- File tujuan: `src/scrapmcp/upstream_scraper.py`
- Referensi transport: `xiaozhi/mcp/bridge.py` (blob `8adaddb0dc45314830fd5dabe770d7f7a54048e3`). Bridge mandiri ditulis ulang menggunakan MCP SDK.

Modul scraper lengkap dipertahankan termasuk fungsi HTML, PDF, YouTube, Jina, kuis, sumber akademik, dan riset. Wrapper CLI memakai jalur sinkron untuk konsistensi, dijalankan di thread saat melayani MCP.

Perubahan pada modul sumber: pencocokan hostname YouTube diperketat; status HTTP error tidak hilang akibat truthiness Response; fallback riset rekursif dihapus untuk mencegah refetch berulang tak terbatas.
Adapter `engine.py` memasang klien HTTP berbatas ukuran dan validasi per-redirect pada jalur requests, serta Jina opt-in. Fungsi async asal tetap disertakan untuk referensi, tidak diekspos oleh aplikasi.

Komponen baru: packaging/entry point, menu dan argparse, penyimpanan lokal, lock/atomic writes, ekspor, report PDF, backup ZIP/checksum, tools MCP, fixture dan tests.

README repo asal mencantumkan metadata `license: apache-2.0`. Pada struktur yang diperiksa tidak ada berkas LICENSE tersendiri. Metadata tersebut dicatat sebagai pernyataan upstream, bukan hasil verifikasi kepemilikan seluruh kode. Atribusi sumber dipertahankan; proyek ini tidak mengklaim seluruh algoritma sebagai karya baru kelompok.
Sebelum publikasi ulang di luar tugas, pemilik repo perlu memastikan ketentuan lisensi seluruh kode/dependensi. Paket ini tidak menambahkan lisensi baru yang mengubah hak kode upstream.

Dependensi Python tetap memiliki lisensi masing-masing. Dependency bukan disalin ke ZIP; pip memasangnya saat instalasi.
