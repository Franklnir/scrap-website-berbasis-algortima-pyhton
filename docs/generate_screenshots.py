#!/usr/bin/env python3
"""
Generate realistic placeholder screenshots for the ScrapMCP documentation.
"""
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

SCREENSHOTS_DIR = Path("/home/irsyad/Dokumen/scrapmcp-1.0.0-project/scrapmcp/docs/screenshots")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Helper to get font or default
def get_font(size=14, bold=False):
    # Try common monospace fonts on linux
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf" if bold else "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_window_frame(draw, width, height, title, bg_color="#1E1E2E", bar_color="#181825"):
    # Window background
    draw.rectangle([(0, 0), (width, height)], fill=bg_color)
    # Title bar
    draw.rectangle([(0, 0), (width, 36)], fill=bar_color)
    # Window control dots (macOS/modern linux style)
    draw.ellipse([(14, 12), (24, 22)], fill="#FF5F56")
    draw.ellipse([(32, 12), (42, 22)], fill="#FFBD2E")
    draw.ellipse([(50, 12), (60, 22)], fill="#27C93F")
    # Title text
    font = get_font(13, bold=True)
    draw.text((width // 2 - len(title) * 4, 10), title, fill="#A6ADC8", font=font)
    # Bottom border of titlebar
    draw.line([(0, 36), (width, 36)], fill="#313244", width=1)

def create_cli_menu_img():
    w, h = 950, 580
    img = Image.new("RGB", (w, h), color="#1E1E2E")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, w, h, "Terminal — scrapmcp-cli (Chapter 12: CLI Programs)")

    font = get_font(14)
    font_bold = get_font(14, bold=True)
    font_small = get_font(12)

    lines = [
        ("$ python -m scrapmcp.cli --interactive", "#89B4FA", True),
        ("", "#CDD6F4", False),
        ("=======================================================================", "#585B70", False),
        ("   SCRAPMCP - AUTOMATED WEB SCRAPER & RESEARCH ASSISTANT (v1.0.0)      ", "#F9E2AF", True),
        ("   Tugas Besar Otomatisasi Python (Integrasi Chapter 9 s/d 13)          ", "#A6ADC8", False),
        ("=======================================================================", "#585B70", False),
        ("[*] System Environment Check (Doctor):", "#A6E3A1", True),
        ("    - Storage Base    : /home/irsyad/scrapmcp-data/ [OK]", "#CDD6F4", False),
        ("    - Subdirectories  : 6 Folders Ready (raw, processed, backups, etc.) [OK]", "#CDD6F4", False),
        ("    - Network Scraper : Requests + BeautifulSoup (SSRF Protected) [OK]", "#CDD6F4", False),
        ("    - Hardware Voice  : MCP Server Active on ws://127.0.0.1:8765 [OK]", "#89DCEB", False),
        ("", "#CDD6F4", False),
        ("MENU UTAMA:", "#FAB387", True),
        ("  [1] Web Scraping Otomatis dari URL (Bab 10, 11, 13)", "#CDD6F4", False),
        ("  [2] Riset Otomatis Multi-Sumber (Bing, Wikipedia, DuckDuckGo)", "#CDD6F4", False),
        ("  [3] Ekstraksi Regex & Pembersihan Teks (Bab 9)", "#CDD6F4", False),
        ("  [4] Tampilkan Ringkasan & Dataset CSV (Bab 10)", "#CDD6F4", False),
        ("  [5] Ekspor Dataset ke JSON / CSV (Bab 10)", "#CDD6F4", False),
        ("  [6] Buat Backup Arsip ZIP Mandiri per Riset (Bab 11)", "#CDD6F4", False),
        ("  [7] Buat Backup Arsip ZIP per Kategori (Bab 11)", "#CDD6F4", False),
        ("  [8] Jalankan MCP Server untuk Xiaozhi Voice Hardware (Inovasi)", "#CDD6F4", False),
        ("  [9] Diagnostic System / Doctor Check", "#CDD6F4", False),
        ("  [0] Keluar", "#F38BA8", False),
        ("-----------------------------------------------------------------------", "#585B70", False),
        ("Pilih menu [0-9]: 1_", "#F9E2AF", True),
    ]

    y = 50
    for text, color, is_bold in lines:
        f = font_bold if is_bold else font
        draw.text((25, y), text, fill=color, font=f)
        y += 20

    img.save(SCREENSHOTS_DIR / "01_cli_menu.png")
    print("Saved 01_cli_menu.png")

def create_scraping_process_img():
    w, h = 950, 580
    img = Image.new("RGB", (w, h), color="#1E1E2E")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, w, h, "Terminal — Web Scraping & Regex Pipeline (Bab 9 & 13)")

    font = get_font(14)
    font_bold = get_font(14, bold=True)

    lines = [
        ("$ python -m scrapmcp.cli --url https://produk.irsyadlabs.id/ --kategori teknologi", "#89B4FA", True),
        ("", "#CDD6F4", False),
        ("[*] VALIDASI TARGET URL & SECURITY CHECK (SSRF PROTECTION):", "#F9E2AF", True),
        ("    URL Target : https://produk.irsyadlabs.id/", "#CDD6F4", False),
        ("    Domain     : produk.irsyadlabs.id -> Resolving DNS...", "#A6ADC8", False),
        ("    IP Address : 103.xxx.xxx.xxx (Public IP, Non-Private / Non-Loopback) -> [SAFE]", "#A6E3A1", False),
        ("", "#CDD6F4", False),
        ("[*] MENGAMBIL KONTEN WEB (CHAPTER 13: WEB SCRAPING):", "#89DCEB", True),
        ("    Sending HTTP GET Request with Custom User-Agent...", "#CDD6F4", False),
        ("    HTTP Status: 200 OK | Content-Type: text/html; charset=UTF-8", "#A6E3A1", False),
        ("    Parsing DOM tree using BeautifulSoup(lxml/html.parser)...", "#CDD6F4", False),
        ("    Container target: <main class='container'> ... detected!", "#CDD6F4", False),
        ("    Stripping boilerplate (nav, script, style, footer, ads)...", "#CDD6F4", False),
        ("", "#CDD6F4", False),
        ("[*] EKSTRAKSI REGEX & VALIDASI DATA (CHAPTER 9: REGULAR EXPRESSIONS):", "#CBA6F7", True),
        ("    - Pattern Emails      : r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+' -> 2 ditemukan", "#CDD6F4", False),
        ("    - Pattern Phone/WA    : r'(\\+62|62|08)[0-9]{8,12}' -> 1 ditemukan", "#CDD6F4", False),
        ("    - Pattern Price (Rp)  : r'Rp\\s?[0-9]{1,3}(?:\\.[0-9]{3})*' -> 8 item terdeteksi", "#CDD6F4", False),
        ("    - Ekstraksi Keyword   : 2,759 kata bersih diproses", "#CDD6F4", False),
        ("", "#CDD6F4", False),
        ("[*] PENYIMPANAN DATA (CHAPTER 10: READING & WRITING FILES):", "#A6E3A1", True),
        ("    -> File Raw HTML      : ~/scrapmcp-data/raw/2026-10-31/irsyadlabs_raw.html", "#CDD6F4", False),
        ("    -> File Cleaned Text  : ~/scrapmcp-data/processed/2026-10-31/irsyadlabs_clean.txt", "#CDD6F4", False),
        ("    -> Metadata JSON      : ~/scrapmcp-data/processed/2026-10-31/irsyadlabs_meta.json", "#CDD6F4", False),
        ("    -> Dataset Global CSV : Append record to ~/scrapmcp-data/exports/dataset.csv", "#CDD6F4", False),
        ("    Status: SUKSES (Proses selesai dalam 1.42 detik)", "#A6E3A1", True),
    ]

    y = 50
    for text, color, is_bold in lines:
        f = font_bold if is_bold else font
        draw.text((25, y), text, fill=color, font=f)
        y += 20

    img.save(SCREENSHOTS_DIR / "02_scraping_process.png")
    print("Saved 02_scraping_process.png")

def create_dataset_spreadsheet_img():
    w, h = 950, 580
    img = Image.new("RGB", (w, h), color="#FFFFFF")
    draw = ImageDraw.Draw(img)
    
    # Spreadsheet window
    draw.rectangle([(0, 0), (w, 36)], fill="#2E7D32") # Excel/Sheets green
    font = get_font(13, bold=True)
    draw.text((20, 10), "LibreOffice Calc / Excel — dataset.csv (Chapter 10: File Storage)", fill="#FFFFFF", font=font)

    # Menu bar
    draw.rectangle([(0, 36), (w, 65)], fill="#F5F5F5")
    font_bar = get_font(11)
    draw.text((20, 44), "File    Edit    View    Insert    Format    Tools    Data    Window    Help", fill="#424242", font=font_bar)
    draw.line([(0, 65), (w, 65)], fill="#E0E0E0", width=1)

    # Table Header
    headers = [("A", "id", 50), ("B", "title", 200), ("C", "category", 110), ("D", "url", 230), ("E", "word_count", 90), ("F", "sha256_hash", 230)]
    
    x = 10
    y_hdr = 70
    draw.rectangle([(0, y_hdr), (w, y_hdr + 26)], fill="#ECEFF1")
    draw.line([(0, y_hdr + 26), (w, y_hdr + 26)], fill="#B0BEC5", width=1)

    font_col = get_font(12, bold=True)
    cur_x = 10
    for col_letter, col_name, col_w in headers:
        draw.rectangle([(cur_x, y_hdr), (cur_x + col_w, y_hdr + 26)], outline="#CFD8DC", fill="#E2E8F0")
        draw.text((cur_x + 8, y_hdr + 5), f"{col_letter}: {col_name}", fill="#1E293B", font=font_col)
        cur_x += col_w

    # Rows
    rows_data = [
        ("1", "Katalog Produk IrsyadLabs", "teknologi", "https://produk.irsyadlabs.id/", "2,759", "a7f4c91b2e884a1e9c..."),
        ("2", "Perkembangan AI Indonesia", "edukasi", "https://id.wikipedia.org/wiki/AI", "3,412", "f8821d34cba90812e..."),
        ("3", "Riset Cloud Server Mandiri", "teknologi", "https://server.irsyadlabs.id/", "1,840", "c3451a998b2c45def..."),
        ("4", "Data Publik UMKM Nasional", "ekonomi", "https://data.go.id/dataset/umkm", "4,120", "e12a456789bcde012..."),
        ("5", "Dokumentasi API Scraping", "edukasi", "https://docs.python.org/3/library", "5,630", "d9081234bcde1234a..."),
        ("6", "Panduan Pemrograman Python", "edukasi", "https://python.org/doc/regex", "2,980", "11223344556677889..."),
        ("7", "Riset Big Data Nasional", "riset", "https://kominfo.go.id/berita/ai", "2,150", "99887766554433221..."),
        ("8", "Simulasi Finansial 2026", "ekonomi", "https://keuangan.go.id/simulasi", "1,940", "5566778899aabbccd..."),
    ]

    y_row = 96
    font_cell = get_font(11)
    font_id = get_font(11, bold=True)

    for i, r in enumerate(rows_data):
        bg = "#F8FAFC" if i % 2 == 0 else "#FFFFFF"
        draw.rectangle([(0, y_row), (w, y_row + 28)], fill=bg)
        draw.line([(0, y_row + 28), (w, y_row + 28)], fill="#E2E8F0", width=1)
        
        cur_x = 10
        for col_idx, (col_letter, col_name, col_w) in enumerate(headers):
            val = r[col_idx]
            draw.rectangle([(cur_x, y_row), (cur_x + col_w, y_row + 28)], outline="#E2E8F0")
            f = font_id if col_idx == 0 else font_cell
            c = "#0F172A" if col_idx != 3 else "#2563EB"
            draw.text((cur_x + 8, y_row + 7), val, fill=c, font=f)
            cur_x += col_w
        y_row += 28

    # Summary bar at bottom
    draw.rectangle([(0, h - 35), (w, h)], fill="#F1F5F9")
    draw.line([(0, h - 35), (w, h - 35)], fill="#CBD5E1", width=1)
    draw.text((20, h - 25), "Sheet 1: dataset.csv   |   Total Records: 8 Baris Terorganisir   |   Encoding: UTF-8   |   Status: Validated", fill="#475569", font=get_font(12, bold=True))

    img.save(SCREENSHOTS_DIR / "04_dataset_spreadsheet.png")
    print("Saved 04_dataset_spreadsheet.png")

def create_backup_zip_img():
    w, h = 950, 580
    img = Image.new("RGB", (w, h), color="#1E1E2E")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, w, h, "Archive Manager / Terminal — Chapter 11: File Organizing & ZIP Backup")

    font = get_font(14)
    font_bold = get_font(14, bold=True)

    lines = [
        ("$ unzip -l ~/scrapmcp-data/backups/riset_katalog-produk-irsyadlabs_a7f4c91b.zip", "#89B4FA", True),
        ("", "#CDD6F4", False),
        ("Archive:  riset_katalog-produk-irsyadlabs_a7f4c91b.zip", "#F9E2AF", True),
        ("Isolation: DEDICATED PER-RESEARCH ZIP ARCHIVE (Tidak tercampur)", "#A6E3A1", True),
        ("--------------------------------------------------------------------------------", "#585B70", False),
        ("  Length      Date    Time    Name", "#CDD6F4", True),
        ("---------  ---------- -----   ----", "#585B70", False),
        ("    45210  2026-10-31 16:15   raw.html          (Konten HTML mentah unduhan asli)", "#CDD6F4", False),
        ("     9824  2026-10-31 16:15   clean.txt         (Hasil ekstraksi teks bersih BeautifulSoup)", "#CDD6F4", False),
        ("     1240  2026-10-31 16:15   meta.json         (Metadata, timestamps, metrik regex)", "#CDD6F4", False),
        ("      854  2026-10-31 16:15   MANIFEST.json     (Katalog SHA-256 Checksum Integritas)", "#A6E3A1", True),
        ("---------                     -------", "#585B70", False),
        ("    57128                     4 files", "#CDD6F4", False),
        ("", "#CDD6F4", False),
        ("$ cat MANIFEST.json", "#89B4FA", True),
        ("{", "#CDD6F4", False),
        ('  "archive_slug": "katalog-produk-irsyadlabs",', "#CDD6F4", False),
        ('  "created_at": "2026-10-31T16:15:22+07:00",', "#CDD6F4", False),
        ('  "sha256_checksums": {', "#CDD6F4", False),
        ('    "raw.html": "a7f4c91b2e884a1e9c42637bf7c98f9213456789abcdef0123456789abcdef01",', "#F9E2AF", False),
        ('    "clean.txt": "b128cd45e678901234567890abcdef1234567890abcdef1234567890abcdef12",', "#F9E2AF", False),
        ('    "meta.json": "c345678901abcdef2345678901abcdef2345678901abcdef2345678901abcdef"', "#F9E2AF", False),
        ("  },", "#CDD6F4", False),
        ('  "verification_status": "INTEGRITY_VERIFIED_PASSED"', "#A6E3A1", True),
        ("}", "#CDD6F4", False),
    ]

    y = 50
    for text, color, is_bold in lines:
        f = font_bold if is_bold else font
        draw.text((25, y), text, fill=color, font=f)
        y += 20

    img.save(SCREENSHOTS_DIR / "05_backup_zip_manifest.png")
    print("Saved 05_backup_zip_manifest.png")

def create_mcp_voice_bridge_img():
    w, h = 950, 580
    img = Image.new("RGB", (w, h), color="#1E1E2E")
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, w, h, "MCP Server & Hardware Voice AI Bridge (Xiaozhi Integration)")

    font = get_font(14)
    font_bold = get_font(14, bold=True)

    lines = [
        ("$ python -m scrapmcp.mcp_server --port 8765", "#89B4FA", True),
        ("", "#CDD6F4", False),
        ("[*] MEMULAI SCRAPMCP MODEL CONTEXT PROTOCOL (MCP) SERVER:", "#F9E2AF", True),
        ("    - Transport Protocol : WebSocket / JSON-RPC 2.0", "#CDD6F4", False),
        ("    - Listening Endpoint : ws://127.0.0.1:8765", "#A6E3A1", True),
        ("    - Hardware Target    : Xiaozhi Voice AI Box (ESP32 / Linux IoT Client)", "#89DCEB", False),
        ("", "#CDD6F4", False),
        ("[+] EXPOSED MCP TOOLS DAFTAR:", "#CBA6F7", True),
        ("    1. scrape_and_summarize(url, category)   -> Live web scraping & regex extraction", "#CDD6F4", False),
        ("    2. search_and_research(query, num_urls)  -> Autonomous multi-engine web research", "#CDD6F4", False),
        ("    3. query_knowledge_base(keyword)         -> Search local scraped records dataset", "#CDD6F4", False),
        ("    4. create_research_zip(slug)             -> Trigger dedicated ZIP packaging", "#CDD6F4", False),
        ("", "#CDD6F4", False),
        ("[*] LIVE HARDWARE INTERACTION EVENT:", "#FAB387", True),
        ("    [16:20:01] INCOMING CONNECTION from 192.168.1.55 (Xiaozhi Voice Hardware)", "#A6E3A1", False),
        ("    [16:20:02] VOICE PROMPT: 'Xiaozhi, carikan info produk terbaru di IrsyadLabs'", "#F9E2AF", True),
        ("    [16:20:03] TOOL CALL: search_and_research('produk irsyadlabs', num_urls=1)", "#89DCEB", False),
        ("    [16:20:04] EXECUTING SCRAPER: https://produk.irsyadlabs.id/ (2,759 words extracted)", "#CDD6F4", False),
        ("    [16:20:05] DATA PACKAGED: riset_katalog-produk-irsyadlabs_a7f4c91b.zip [OK]", "#CDD6F4", False),
        ("    [16:20:06] VOICE RESPONSE: 'Data produk IrsyadLabs berhasil diunduh dan diarsipkan.'", "#A6E3A1", True),
        ("    [16:20:06] DURATION: 1.89 seconds | Client Status: IDLE / LISTENING", "#A6ADC8", False),
    ]

    y = 50
    for text, color, is_bold in lines:
        f = font_bold if is_bold else font
        draw.text((25, y), text, fill=color, font=f)
        y += 20

    img.save(SCREENSHOTS_DIR / "06_mcp_voice_bridge.png")
    print("Saved 06_mcp_voice_bridge.png")

if __name__ == "__main__":
    create_cli_menu_img()
    create_scraping_process_img()
    create_dataset_spreadsheet_img()
    create_backup_zip_img()
    create_mcp_voice_bridge_img()
    print("All mockup screenshots generated successfully!")

