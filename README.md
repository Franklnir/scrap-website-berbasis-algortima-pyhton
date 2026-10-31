# SCRAPMCP 1.0.0
> **Sistem Otomatisasi Web Scraping, Pembersihan Data Berbasis Algoritma Regex, dan Pengorganisasian Arsip Terenkripsi SHA-256**

Proyek Tugas Besar Pemrograman Python Otomatisasi berbasis terminal (CLI) dengan integrasi materi Chapter 9 s/d 13 serta ekstensi Model Context Protocol (MCP) untuk integrasi hardware kontrol eksternal.

---

## 👥 Identitas Tim Pengembang (Kelompok 3)
* **Irsyad** — *Ketua & Storage Architect* (Manajemen 6 Direktori Data, Serialisasi CSV/JSON & Kriptografi Hash SHA-256)
* **Sena Dwi Ilham** — *Scraper & Regex Specialist* (Web Scraping Requests & BeautifulSoup, DOM Parsing, Ekstraksi Pola Regex)
* **Dhean Shafwan** — *CLI & IoT Integrator* (Antarmuka Terminal REPL State Machine [0–9], Diagnostik Doctor, WebSocket MCP Server)

---

## 📑 Berkas Laporan & Presentasi
* 📊 **Slide Presentasi (8 Slide Ringkas & Padat):** [`docs/PRESENTASI_8_SLIDE.pptx`](docs/PRESENTASI_8_SLIDE.pptx)
* 📄 **Laporan Dokumentasi Visual (Tangkapan Layar Sistem):** [`docs/DOKUMENTASI_TANGKAPAN_LAYAR.pdf`](docs/DOKUMENTASI_TANGKAPAN_LAYAR.pdf)
* 📸 **Koleksi Tangkapan Layar:** [`docs/screenshots/`](docs/screenshots/)

---

## 🔒 Jaminan Keamanan (Security & Privacy Notice)
* **Zero Hardcoded Secrets / Tokens:** Repositori ini **bebas 100% dari token, API key, atau endpoint pribadi**.
* Semua konfigurasi sensitif diproteksi melalui `.gitignore` (`.env`, `.mcp_endpoint`, `scrapmcp-data/`).
* Aplikasi bekerja secara penuh dalam **mode offline / mode lokal manual** tanpa memerlukan token eksternal.

---

## 🚀 Panduan Instalasi Cepat

### Prasyarat
* Python **3.10** atau lebih baru
* Git & koneksi internet (hanya saat mengunduh dependensi)

### 1. Clone Repositori
```bash
git clone https://github.com/Franklnir/scrap-website-berbasis-algortima-pyhton.git
cd scrap-website-berbasis-algortima-pyhton
```

### 2. Instalasi Dependensi (Linux / macOS)
```bash
# Buat virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install paket lokal
pip install -e .
```
*(Atau jalankan skrip otomatis: `bash install-linux.sh`)*

### 2. Alternatif Instalasi (Windows)
```powershell
# Buat virtual environment
py -m venv .venv
.\.venv\Scripts\activate

# Install paket lokal
pip install -e .
```
*(Atau jalankan skrip otomatis: `install-windows.bat`)*

---

## 💻 Panduan Penggunaan Aplikasi

### 1. Mode Menu Interaktif Terminal (CLI REPL)
Jalankan aplikasi ke dalam menu interaktif angka `[0–9]`:
```bash
scrapmcp
# atau
python -m scrapmcp.cli --interactive
```

Tampilan menu utama:
```text
=======================================================================
   SCRAPMCP - AUTOMATED WEB SCRAPER & RESEARCH ASSISTANT (v1.0.0)      
   Tugas Besar Otomatisasi Python (Integrasi Chapter 9 s/d 13)          
=======================================================================
[*] System Environment Check (Doctor):
    - Storage Base    : ~/scrapmcp-data/ [OK]
    - Subdirectories  : 6 Folders Ready (raw, processed, backups, etc.) [OK]
    - Network Scraper : Requests + BeautifulSoup [OK]

MENU UTAMA:
  [1] Web Scraping Otomatis dari URL Target
  [2] Riset Otomatis Multi-Sumber (Bing Web & Wikipedia OpenSearch)
  [3] Ekstraksi Regex & Pembersihan Teks
  [4] Tampilkan Ringkasan & Dataset CSV
  [5] Ekspor Dataset ke JSON / CSV
  [6] Buat Backup Arsip ZIP Mandiri per Riset
  [7] Buat Backup Arsip ZIP per Kategori
  [8] Jalankan Server WebSocket MCP untuk Kontrol Eksternal
  [9] Diagnostic System / Doctor Check
  [0] Keluar
```

### 2. Mode Perintah Cepat (One-Shot CLI)
Eksekusi langsung melalui flag perintah:

* **Scraping URL Spesifik & Simpan:**
  ```bash
  scrapmcp scrape "https://produk.irsyadlabs.id/" --category teknologi
  ```
* **Riset Otomatis Berdasarkan Topik (Bing & Wikipedia):**
  ```bash
  scrapmcp research "kecerdasan buatan" --mode web --save
  ```
* **Scraping Banyak URL Sekaligus (Batch):**
  ```bash
  scrapmcp batch urls.txt --category referensi
  ```
* **Daftar & Baca Rekaman yang Telah Diambil:**
  ```bash
  scrapmcp list
  scrapmcp read <ID_DARI_LIST>
  ```
* **Pemeriksaan Kesehatan Sistem:**
  ```bash
  scrapmcp doctor
  ```

---

## 📁 Struktur 6 Direktori Data Terorganisir
Semua hasil pemrosesan tersimpan rapi secara terstruktur di `~/scrapmcp-data/`:

| Direktori | Peran & Deskripsi Berkas |
|---|---|
| `raw/<kategori>/<tanggal>/` | Berkas mentah asli unduhan web (`raw.html`) untuk audit data |
| `processed/<kategori>/<tanggal>/` | Teks bersih hasil ekstraksi BeautifulSoup & file metadata JSON |
| `backups/` | Arsip kompresi mandiri per riset (`riset_{slug}_{hash}.zip`) ber-`MANIFEST.json` SHA-256 |
| `exports/` | Dataset tabular konsolidasi global: `dataset.csv` (RFC 4180) & `dataset.json` |
| `reports/` | Laporan audit berkas dan ringkasan eksekutif |
| `logs/` | Jejak audit eksekusi CLI (`scraping.log`) |

---

## 🧪 Pengujian Unit Test Otomatis
Seluruh fitur telah diverifikasi dengan 21 pengujian otomatis (*zero regression*):
```bash
python -m pytest -v
```

---

## 📜 Lisensi & Atribusi
Proyek ini dikembangkan untuk keperluan akademik. Mesin scraping awal mengacu pada arsitektur ekstraksi dokumen `Franklnir/xiaozhi-knowledge-base` (lihat [`SOURCE_ATTRIBUTION.md`](SOURCE_ATTRIBUTION.md)).
