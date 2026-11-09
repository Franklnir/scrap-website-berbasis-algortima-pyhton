# SCRAPMCP 1.0.0
> **Sistem Otomatisasi Web Scraping, Pembersihan Data Berbasis Algoritma Regex, dan Pengorganisasian Arsip Terenkripsi SHA-256**

Proyek Tugas Besar Pemrograman Python Otomatisasi berbasis terminal (CLI) dengan integrasi materi Chapter 9 s/d 13 serta ekstensi Model Context Protocol (MCP) untuk integrasi hardware kontrol eksternal.

---

## 👥 Identitas Tim Pengembang (Kelompok 3)
* **Irsyad** — *Ketua & Storage Architect* (Manajemen 6 Direktori Data, Serialisasi CSV/JSON & Kriptografi Hash SHA-256)
* **Sena Dwi Ilham** — *Scraper & Regex Specialist* (Web Scraping Requests & BeautifulSoup, DOM Parsing, Ekstraksi Pola Regex)
* **Dhean Shafwan** — *CLI & IoT Integrator* (Antarmuka Terminal REPL State Machine [0–9], Diagnostik Doctor, WebSocket MCP Server)

---

## 📑 Berkas Laporan, Presentasi & Spreadsheet
* 📊 **Slide Presentasi (8 Slide Ringkas & Padat):** [`docs/PRESENTASI_8_SLIDE.pptx`](docs/PRESENTASI_8_SLIDE.pptx)
* 📄 **Laporan Dokumentasi Visual (Tangkapan Layar Sistem):** [`docs/DOKUMENTASI_TANGKAPAN_LAYAR.pdf`](docs/DOKUMENTASI_TANGKAPAN_LAYAR.pdf)
* 📈 **Dataset Excel Terformat (.xlsx):** [`sample-output/exports/dataset.xlsx`](sample-output/exports/dataset.xlsx)
* 📋 **Dataset CSV Konsolidasi:** [`sample-output/exports/dataset.csv`](sample-output/exports/dataset.csv)
* 📸 **Koleksi Tangkapan Layar:** [`docs/screenshots/`](docs/screenshots/)

---

## 🔒 Jaminan Keamanan (Security & Privacy Notice)
* **Zero Hardcoded Secrets / Tokens:** Repositori ini **bebas 100% dari token, API key, atau endpoint pribadi**.
* Semua konfigurasi sensitif diproteksi melalui `.gitignore` (`.env`, `.mcp_endpoint`, `scrapmcp-data/`).
* Aplikasi bekerja secara penuh dalam **mode offline / mode lokal manual** tanpa memerlukan token eksternal.

---

## 🚀 Panduan Instalasi (Windows & Linux)

### Prasyarat Sistem
* Python **3.10** atau lebih baru terpasang di sistem ([Unduh Python](https://www.python.org/downloads/))
* Git untuk mengunduh kode program

### Langkah 1: Clone Repositori
Buka Terminal (Linux) atau PowerShell / Git Bash (Windows):
```bash
git clone https://github.com/Franklnir/scrap-website-berbasis-algortima-pyhton.git
cd scrap-website-berbasis-algortima-pyhton
```

---

### Langkah 2A: Instalasi di Sistem Operasi LINUX

#### Opsi 1 — Otomatis (1 Perintah):
```bash
bash install-linux.sh
```

#### Opsi 2 — Manual via Terminal:
```bash
# 1. Buat virtual environment
python3 -m venv .venv

# 2. Aktifkan virtual environment
source .venv/bin/activate

# 3. Pasang dependensi dan paket lokal
pip install -e .
```

---

### Langkah 2B: Instalasi di Sistem Operasi WINDOWS

#### Opsi 1 — Otomatis (Satu Klik):
Cukup **klik ganda (double-click)** pada berkas:
👉 `install-windows.bat`  
Skrip batch akan secara otomatis membuat virtual environment dan memasang semua dependensi.

#### Opsi 2 — Manual via PowerShell:
```powershell
# 1. Buat virtual environment
py -m venv .venv

# 2. Aktifkan virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Pasang dependensi dan paket lokal
pip install -e .
```

#### Opsi 3 — Manual via Command Prompt (CMD):
```cmd
py -m venv .venv
.\.venv\Scripts\activate.bat
pip install -e .
```

---

## 💻 Panduan Cara Pakai Aplikasi (Windows & Linux)

### 1. Menjalankan Menu Interaktif Terminal (CLI REPL)
Mode ini sangat direkomendasikan saat sesi demonstrasi di hadapan dosen/penguji.

* **Di Linux:**
  ```bash
  source .venv/bin/activate
  scrapmcp
  # atau: python -m scrapmcp.cli --interactive
  ```

* **Di Windows (PowerShell/CMD):**
  ```powershell
  .\.venv\Scripts\activate
  scrapmcp
  # atau: python -m scrapmcp.cli --interactive
  ```

Tampilan menu interaktif angka `[0–9]`:
```text
=======================================================================
   SCRAPMCP - AUTOMATED WEB SCRAPER & RESEARCH ASSISTANT (v1.0.0)      
   Tugas Besar Otomatisasi Python (Kelompok 3: Irsyad, Sena, Dhean)    
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
*Cukup ketik angka menu (misal: `1` untuk scraping atau `9` untuk diagnosa), lalu tekan Enter.*

---

### 2. Mode Perintah Cepat (One-Shot CLI)
Bisa langsung dijalankan dari terminal/PowerShell tanpa masuk ke menu:

* **Scraping URL Tertentu & Simpan:**
  ```bash
  scrapmcp scrape "https://produk.irsyadlabs.id/" --category teknologi
  ```
* **Riset Otomatis Berdasarkan Topik (Multi-Source Search):**
  ```bash
  scrapmcp research "kecerdasan buatan" --mode web --save
  ```
* **Scraping Banyak URL Sekaligus (Batch URL):**
  ```bash
  scrapmcp batch urls.txt --category referensi
  ```
* **Melihat Daftar Materi yang Pernah Diambil:**
  ```bash
  scrapmcp list
  ```
* **Membaca Detail Materi Tertentu Berdasarkan ID:**
  ```bash
  scrapmcp read <ID_DOKUMEN>
  ```
* **Membuat Backup ZIP Mandiri:**
  ```bash
  scrapmcp backup
  ```
* **Diagnostik Kesehatan Sistem:**
  ```bash
  scrapmcp doctor
  ```

---

### 3. Cara Membuka Hasil Dataset (Excel & CSV)
Semua rekaman hasil scraping tersimpan secara terorganisir di folder `~/scrapmcp-data/exports/` (atau folder `sample-output/exports/`):

* **Di Windows:**
  * Buka File Explorer, masuk ke folder `exports/`.
  * Klik ganda berkas **`dataset.xlsx`** atau **`dataset.csv`** untuk langsung membukanya di Microsoft Excel.
* **Di Linux:**
  * Buka lewat LibreOffice Calc dengan perintah terminal:
    ```bash
    localc ~/scrapmcp-data/exports/dataset.xlsx &
    ```
  * Atau gunakan shortcut desktop **Microsoft Excel (Calc)** yang telah disediakan.

---

## 📁 Struktur 6 Direktori Data Terorganisir
Semua hasil pemrosesan tersimpan rapi secara terstruktur di `~/scrapmcp-data/`:

| Direktori | Peran & Deskripsi Berkas |
|---|---|
| `raw/<kategori>/<tanggal>/` | Berkas mentah asli unduhan web (`raw.html`) untuk audit data |
| `processed/<kategori>/<tanggal>/` | Teks bersih hasil ekstraksi BeautifulSoup & file metadata JSON |
| `backups/` | Arsip kompresi mandiri per riset (`riset_{slug}_{hash}.zip`) ber-`MANIFEST.json` SHA-256 |
| `exports/` | Dataset tabular konsolidasi: `dataset.xlsx` (Excel), `dataset.csv` & `dataset.json` |
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
