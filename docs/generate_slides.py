#!/usr/bin/env python3
"""
Generate a professional 7-slide PowerPoint presentation for ScrapMCP project.
Strictly 7 slides according to the user specification.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
import os

OUTPUT_PATH = "/home/irsyad/Dokumen/scrapmcp-1.0.0-project/scrapmcp/docs/PRESENTASI_7_SLIDE.pptx"

# Initialize presentation with 16:9 widescreen
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette
DARK_BG = RGBColor(15, 23, 42)       # Slate 900
CARD_BG = RGBColor(30, 41, 59)       # Slate 800
CARD_BORDER = RGBColor(51, 65, 85)   # Slate 700
PRIMARY = RGBColor(14, 165, 233)     # Sky 500
ACCENT = RGBColor(16, 185, 129)      # Emerald 500
PURPLE = RGBColor(168, 85, 247)      # Purple 500
TEXT_MAIN = RGBColor(248, 250, 252)  # Slate 50
TEXT_MUTED = RGBColor(148, 163, 184) # Slate 400
TEXT_DIM = RGBColor(100, 116, 139)   # Slate 500

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = DARK_BG

def add_header(slide, title_text, category_text="TUGAS BESAR OTOMATISASI PYTHON"):
    # Category badge
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = PRIMARY

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN

def add_card(slide, left, top, width, height, title="", border_color=CARD_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = CARD_BG
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    
    if title:
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = PRIMARY
        p.alignment = PP_ALIGN.LEFT
    return shape

# ==========================================
# SLIDE 1: Title Slide (Cover)
# ==========================================
s1 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s1)

# Badge
badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2), Inches(4.5), Inches(0.4))
badge.fill.solid()
badge.fill.fore_color.rgb = CARD_BG
badge.line.color.rgb = PRIMARY
b_p = badge.text_frame.paragraphs[0]
b_p.text = "PROYEK AKADEMIK OTOMATISASI PYTHON"
b_p.font.size = Pt(11)
b_p.font.bold = True
b_p.font.color.rgb = PRIMARY
b_p.alignment = PP_ALIGN.CENTER

# Main Title
title_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(1.8))
tf = title_box.text_frame
tf.word_wrap = True
p1 = tf.paragraphs[0]
p1.text = "SCRAPMCP"
p1.font.size = Pt(44)
p1.font.bold = True
p1.font.color.rgb = TEXT_MAIN

p2 = tf.add_paragraph()
p2.text = "Automated Web Scraping, Regex Pipeline & Secure File Archive"
p2.font.size = Pt(22)
p2.font.bold = True
p2.font.color.rgb = PRIMARY

p3 = tf.add_paragraph()
p3.text = "Implementasi Terpadu Chapter 9-13 dengan Ekstensi Hardware Voice AI (MCP Protocol)"
p3.font.size = Pt(14)
p3.font.color.rgb = TEXT_MUTED

# 3 Team Members Cards (Kelompok 3 Mahasiswa)
team_w = Inches(3.64)
team_h = Inches(2.2)
y_team = Inches(4.4)

roles = [
    ("MAHASISWA 1", "Ketua & Data Engineer", "Arsitektur Sistem, File Organization (Bab 11),\nReading/Writing Files & CSV/JSON (Bab 10),\nVerifikasi Checksum SHA-256."),
    ("MAHASISWA 2", "Pipeline & Regex Specialist", "Web Scraping Requests & BS4 (Bab 13),\nEkstraksi Pola Regex & Sanitasi (Bab 9),\nProteksi Keamanan SSRF & Parsing DOM."),
    ("MAHASISWA 3", "CLI & Hardware Integrator", "Command Line Interface & argparse (Bab 12),\nMenu Interaktif Terminal [0-9],\nInovasi WebSocket MCP Server (Hardware AI).")
]

for i, (name, role, desc) in enumerate(roles):
    x = Inches(0.8 + i * 4.0)
    card = add_card(s1, x, y_team, team_w, team_h, border_color=PRIMARY if i == 0 else CARD_BORDER)
    tf = card.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = name
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT if i == 0 else PRIMARY
    
    p_role = tf.add_paragraph()
    p_role.text = role
    p_role.font.size = Pt(12)
    p_role.font.bold = True
    p_role.font.color.rgb = TEXT_MAIN
    
    p_desc = tf.add_paragraph()
    p_desc.text = desc
    p_desc.font.size = Pt(10.5)
    p_desc.font.color.rgb = TEXT_MUTED

# ==========================================
# SLIDE 2: Latar Belakang & Rumusan Masalah
# ==========================================
s2 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s2)
add_header(s2, "Latar Belakang & Rumusan Masalah", "PROBLEMATIKA PENGELOLAAN DATA")

# Left Column: Permasalahan Riil
c_left = add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Permasalahan di Lapangan")
tf_l = c_left.text_frame
tf_l.word_wrap = True
tf_l.paragraphs[0].text = "Tantangan Manualisasi Data:"
tf_l.paragraphs[0].font.size = Pt(16)
tf_l.paragraphs[0].font.bold = True
tf_l.paragraphs[0].font.color.rgb = RGBColor(244, 63, 94) # Rose

bullets_prob = [
    ("Data Tersebar & Heterogen:", "Informasi bisnis, katalog produk, dan riset terpecah di berbagai situs web, dokumen publik, dan portal tanpa struktur standar."),
    ("Ekstraksi Manual Tidak Efisien:", "Pengumpulan informasi dengan 'copy-paste' manual menghabiskan banyak jam kerja dan memiliki tingkat kesalahan (human-error) tinggi."),
    ("Teks Mentah Belum Terstruktur:", "Dokumen hasil unduh dipenuhi tag HTML, iklan, dan script asing tanpa validasi format baku (email, telepon, entitas)."),
    ("File Berantakan & Rawan Hilang:", "Penyimpanan dokumen tidak memiliki pembagian direktori jelas, tanpa kompresi ZIP otomatis, dan tanpa jaminan keaslian data.")
]

for title, desc in bullets_prob:
    p = tf_l.add_paragraph()
    p.text = f"• {title} "
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    
    p_sub = tf_l.add_paragraph()
    p_sub.text = f"   {desc}"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = TEXT_MUTED

# Right Column: Solusi Terpadu ScrapMCP
c_right = add_card(s2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), "Solusi Terpadu: ScrapMCP")
tf_r = c_right.text_frame
tf_r.word_wrap = True
tf_r.paragraphs[0].text = "Otomatisasi Berbasis Python:"
tf_r.paragraphs[0].font.size = Pt(16)
tf_r.paragraphs[0].font.bold = True
tf_r.paragraphs[0].font.color.rgb = ACCENT

bullets_sol = [
    ("Automated Web Ingestion:", "Pengambilan konten otomatis dari URL target atau multi-search engine secara simultan dan terproteksi dari ancaman SSRF."),
    ("Regex Parsing & Sanitasi Pintar:", "Pembersihan tag boilerplate serta ekstraksi otomatis entitas kontak, angka harga, dan ringkasan berbasis frekuensi kata."),
    ("Penyimpanan Multi-Tier & CSV:", "Setiap riset disimpan ke HTML mentah, teks bersih, metadata JSON, dan dataset CSV konsolidasi terindeks."),
    ("Organisasi 6 Folder & Backup ZIP:", "Sistem isolasi arsip mandiri per sesi riset dengan katalog SHA-256 MANIFEST untuk jaminan integritas.")
]

for title, desc in bullets_sol:
    p = tf_r.add_paragraph()
    p.text = f"✔ {title} "
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    
    p_sub = tf_r.add_paragraph()
    p_sub.text = f"   {desc}"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = TEXT_MUTED

# ==========================================
# SLIDE 3: Integrasi Kurikulum Wajib (Bab 9-13)
# ==========================================
s3 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s3)
add_header(s3, "Integrasi Kurikulum Wajib (Chapter 9 s/d 13)", "KEPATUHAN SILABUS & IMPLEMENTASI TEKNIS")

chapters = [
    ("Chapter 9", "Regular Expressions (re)", "Ekstraksi & Pembersihan", 
     "• Ekstraksi email, no telp/WA, pola harga Rp.\n• Sanitasi whitespace & penghapusan simbol.\n• Modul: scrapmcp/cleaner.py"),
    
    ("Chapter 10", "Reading & Writing Files", "Manajemen File & Format", 
     "• Pembacaan & penulisan via open() & pathlib.\n• Penyimpanan file teks (.txt), raw HTML (.html).\n• Serialisasi metadata JSON & dataset global CSV."),
    
    ("Chapter 11", "Organizing Files", "Folder & ZIP Backup", 
     "• Pengelolaan otomatis 6 folder penyimpanan data.\n• Pembuatan arsip ZIP mandiri per riset.\n• Pembuatan manifest SHA-256 integritas data."),
    
    ("Chapter 12", "Command Line Programs", "Antarmuka CLI Interaktif", 
     "• Parsing argumen CLI menggunakan argparse.\n• Menu navigasi interaktif terminal [0-9].\n• Fitur diagnostic system check (--doctor)."),
    
    ("Chapter 13", "Web Scraping", "Pengambilan Data Web", 
     "• Pengambilan HTML via library requests.\n• Parsing DOM cerdas dengan BeautifulSoup4.\n• Proteksi validasi SSRF (Private IP rejection).")
]

card_w = Inches(2.2)
card_h = Inches(4.8)
for i, (chap, mat, focus, detail) in enumerate(chapters):
    x = Inches(0.8 + i * 2.4)
    card = add_card(s3, x, Inches(1.8), card_w, card_h, border_color=PRIMARY if i == 0 else CARD_BORDER)
    tf = card.text_frame
    tf.word_wrap = True
    
    p_chap = tf.paragraphs[0]
    p_chap.text = chap
    p_chap.font.size = Pt(13)
    p_chap.font.bold = True
    p_chap.font.color.rgb = PRIMARY
    
    p_mat = tf.add_paragraph()
    p_mat.text = mat
    p_mat.font.size = Pt(12)
    p_mat.font.bold = True
    p_mat.font.color.rgb = TEXT_MAIN
    
    p_foc = tf.add_paragraph()
    p_foc.text = focus
    p_foc.font.size = Pt(10)
    p_foc.font.bold = True
    p_foc.font.color.rgb = ACCENT
    
    p_det = tf.add_paragraph()
    p_det.text = f"\n{detail}"
    p_det.font.size = Pt(10)
    p_det.font.color.rgb = TEXT_MUTED

# ==========================================
# SLIDE 4: Arsitektur Sistem & Alur Kerja Data
# ==========================================
s4 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s4)
add_header(s4, "Arsitektur Sistem & Pipeline Pengolahan Data", "DESAIN SISTEM & WORKFLOW DATA")

# 4 Horizontal Workflow Stages
stages = [
    ("TAHAP 1: INGESTION", "Web Scraping & Keamanan", 
     "• Input URL / Kueri Topik\n• Validasi URL & Anti-SSRF (Network Check)\n• HTTP Fetch via requests\n• Output: Raw HTML Response"),
    
    ("TAHAP 2: PROCESSING", "BeautifulSoup & Regex", 
     "• Parsing DOM via BeautifulSoup4\n• Eliminasi tag skrip, iklan, navigasi\n• Ekstraksi pola Regex (Kontak & Harga)\n• Pembentukan Ringkasan Teks & Slug"),
    
    ("TAHAP 3: PERSISTENCE", "Organisasi File & Dataset", 
     "• Penyimpanan raw/*.html ke folder tanggal\n• Penyimpanan processed/*.txt & meta.json\n• Append ke exports/dataset.csv\n• Log transaksi ke logs/scraping.log"),
    
    ("TAHAP 4: ARCHIVING", "ZIP Backup & Hash Manifest", 
     "• Pembentukan ZIP mandiri per riset\n• File ZIP: riset_{slug}_{hash}.zip\n• Komputasi Checksum SHA-256 tiap file\n• Penyusunan MANIFEST.json verifikasi")
]

stage_w = Inches(2.75)
stage_h = Inches(3.6)
for i, (stg_name, stg_sub, stg_desc) in enumerate(stages):
    x = Inches(0.8 + i * 2.95)
    card = add_card(s4, x, Inches(1.8), stage_w, stage_h, border_color=PRIMARY if i == 1 or i == 3 else CARD_BORDER)
    tf = card.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = stg_name
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT
    
    p_sub = tf.add_paragraph()
    p_sub.text = stg_sub
    p_sub.font.size = Pt(13)
    p_sub.font.bold = True
    p_sub.font.color.rgb = TEXT_MAIN
    
    p_desc = tf.add_paragraph()
    p_desc.text = f"\n{stg_desc}"
    p_desc.font.size = Pt(10.5)
    p_desc.font.color.rgb = TEXT_MUTED

# Storage Organization Diagram Box
store_box = add_card(s4, Inches(0.8), Inches(5.6), Inches(11.6), Inches(1.3), border_color=ACCENT)
tf_sb = store_box.text_frame
tf_sb.word_wrap = True
p_sb1 = tf_sb.paragraphs[0]
p_sb1.text = "STRUKTUR DATA TERORGANISIR (~/scrapmcp-data/):"
p_sb1.font.size = Pt(12)
p_sb1.font.bold = True
p_sb1.font.color.rgb = PRIMARY

p_sb2 = tf_sb.add_paragraph()
p_sb2.text = "[raw/] (arsip HTML asli) | [processed/] (teks bersih & JSON) | [backups/] (arsip ZIP mandiri) | [exports/] (dataset CSV & JSON) | [reports/] (laporan ringkasan) | [logs/] (audit trail)"
p_sb2.font.size = Pt(11)
p_sb2.font.color.rgb = TEXT_MAIN

# ==========================================
# SLIDE 5: Fitur Unggulan & Inovasi Hardware Voice AI
# ==========================================
s5 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s5)
add_header(s5, "Inovasi & Keunggulan: Model Context Protocol (MCP)", "NILAI TAMBAH & KONEKTIVITAS HARDWARE")

# Left Column: Dual Interaction Mode
c_feat = add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Dual Mode Interaksi")
tf_f = c_feat.text_frame
tf_f.word_wrap = True
tf_f.paragraphs[0].text = "Fleksibilitas Pengoperasian:"
tf_f.paragraphs[0].font.size = Pt(16)
tf_f.paragraphs[0].font.bold = True
tf_f.paragraphs[0].font.color.rgb = PRIMARY

features = [
    ("CLI Mode Interaktif (Manual & Script):", "Operator dapat menggunakan menu terminal angka [0-9] atau eksekusi otomatis via flag argument seperti --url, --kategori, dan --doctor."),
    ("Standar Protokol Modern MCP:", "Mengimplementasikan Model Context Protocol (MCP) resmi Anthropic / Open Protocol standar industri AI."),
    ("Dedicated Per-Research ZIP Backup:", "Setiap sesi riset menghasilkan arsip mandiri yang tidak bercampur dengan topik lain, dilengkapi slug nama isi konten otomatis."),
    ("Keamanan Berlapis (SSRF Guard):", "Mencegah serangan Localhost & Private IP scanning saat melakukan web crawling.")
]

for title, desc in features:
    p = tf_f.add_paragraph()
    p.text = f"★ {title}"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    
    p_sub = tf_f.add_paragraph()
    p_sub.text = f"   {desc}"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = TEXT_MUTED

# Right Column: Xiaozhi Voice AI Box Integration
c_voice = add_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), "Integrasi Hardware: Xiaozhi Voice AI")
tf_v = c_voice.text_frame
tf_v.word_wrap = True
tf_v.paragraphs[0].text = "Autonomous Voice Research Agent:"
tf_v.paragraphs[0].font.size = Pt(16)
tf_v.paragraphs[0].font.bold = True
tf_v.paragraphs[0].font.color.rgb = PURPLE

voice_points = [
    ("Konektivitas WebSocket:", "Server MCP berjalan pada ws://127.0.0.1:8765 siap menerima panggilan fungsi dari perangkat AI eksternal."),
    ("Perintah Suara Pengguna:", "User dapat langsung berbicara: 'Xiaozhi, tolong riset tentang produk teknologi terbaru di website ini.'"),
    ("Eksekusi Background Otomatis:", "Xiaozhi memanggil tool scrape_and_summarize atau search_and_research tanpa perlu mengetik CLI."),
    ("Feedback Suara Cerdas:", "Hasil scraping diekstrak dan diringkas secara instan untuk disuarakan kembali oleh Xiaozhi kepada pengguna.")
]

for title, desc in voice_points:
    p = tf_v.add_paragraph()
    p.text = f"🎙 {title}"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    
    p_sub = tf_v.add_paragraph()
    p_sub.text = f"   {desc}"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = TEXT_MUTED

# ==========================================
# SLIDE 6: Hasil Pengujian & Validasi Integritas
# ==========================================
s6 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s6)
add_header(s6, "Hasil Pengujian & Verifikasi Integritas Data", "PENGUJIAN SISTEM & TOLOK UKUR KEBERHASILAN")

# 3 Metric Cards
metrics = [
    ("2,759 KATA", "Ekstraksi Konten Web Nyata", "Pengujian scraping pada situs live https://produk.irsyadlabs.id/ berhasil mengekstrak seluruh katalog produk dan harga secara utuh."),
    ("100% PASS", "Automated Test Suite", "Seluruh 21 unit test (test_pipeline.py, test_network.py, test_mcp.py) sukses tanpa error."),
    ("SHA-256", "Jaminan Integritas File", "Setiap arsip ZIP memiliki MANIFEST.json dengan hash kriptografis untuk mencegah modifikasi atau korupsi data.")
]

for i, (val, title, desc) in enumerate(metrics):
    x = Inches(0.8 + i * 4.0)
    card = add_card(s6, x, Inches(1.8), Inches(3.64), Inches(2.2), border_color=ACCENT if i == 1 else PRIMARY)
    tf = card.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = val
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT if i == 1 else PRIMARY
    
    p_t = tf.add_paragraph()
    p_t.text = title
    p_t.font.size = Pt(12)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_MAIN
    
    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.size = Pt(10.5)
    p_d.font.color.rgb = TEXT_MUTED

# Test Matrix Bottom Table
test_box = add_card(s6, Inches(0.8), Inches(4.3), Inches(11.6), Inches(2.3), "Tabel Hasil Pengujian Modul:")
tf_tb = test_box.text_frame
tf_tb.word_wrap = True

test_rows = [
    "• Modul Scraper (Requests + BS4): Sukses scraping web lokal & publik; lolos proteksi SSRF.",
    "• Modul Regex & Sanitasi (re): Berhasil mengekstrak email, no telepon/WA, dan label mata uang Rp.",
    "• Modul Penyimpanan (File I/O): File raw.html, clean.txt, meta.json, dan dataset.csv tersimpan rapi.",
    "• Modul Pengarsipan (Organizing): Pembentukan ZIP mandiri dengan manifest SHA-256 berhasil 100%.",
    "• Modul MCP Server & CLI: Respon WebSocket < 2 detik dan menu CLI interaktif berfungsi lancar."
]

for row in test_rows:
    p = tf_tb.add_paragraph()
    p.text = row
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MAIN

# ==========================================
# SLIDE 7: Kesimpulan, Peran Tim & Q&A
# ==========================================
s7 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s7)
add_header(s7, "Kesimpulan & Pembagian Peran Tim", "EVALUASI AKHIR & SESI TANYA JAWAB")

# Left Column: Kesimpulan Proyek
c_conc = add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "Kesimpulan Proyek")
tf_c = c_conc.text_frame
tf_c.word_wrap = True
tf_c.paragraphs[0].text = "Pencapaian Utama:"
tf_c.paragraphs[0].font.size = Pt(16)
tf_c.paragraphs[0].font.bold = True
tf_c.paragraphs[0].font.color.rgb = ACCENT

conclusions = [
    ("Kepatuhan Penuh Silabus:", "Proyek sukses mengintegrasikan secara utuh materi Chapter 9 (Regex), 10 (File I/O), 11 (File Org), 12 (CLI Programs), dan 13 (Web Scraping)."),
    ("Struktur Data Standar Industri:", "Manajemen 6 folder data, dataset CSV konsolidasi, dan pengarsipan ZIP mandiri dengan hash SHA-256 menjamin keandalan data."),
    ("Solusi Masalah Riil:", "Mengotomatiskan seluruh alur manualisasi riset data dari internet menjadi proses satu klik atau perintah suara."),
    ("Kesiapan Masa Depan (IoT/AI):", "Integrasi Model Context Protocol membuktikan bahwa aplikasi otomasi Python dapat berkomunikasi langsung dengan perangkat AI fisik.")
]

for title, desc in conclusions:
    p = tf_c.add_paragraph()
    p.text = f"✔ {title}"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    
    p_sub = tf_c.add_paragraph()
    p_sub.text = f"   {desc}"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = TEXT_MUTED

# Right Column: Pembagian Peran 3 Mahasiswa & Sesi Q&A
c_team = add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), "Kolaborasi 3 Mahasiswa & Q&A")
tf_t = c_team.text_frame
tf_t.word_wrap = True
tf_t.paragraphs[0].text = "Pembagian Tanggung Jawab Anggota:"
tf_t.paragraphs[0].font.size = Pt(15)
tf_t.paragraphs[0].font.bold = True
tf_t.paragraphs[0].font.color.rgb = PRIMARY

team_roles = [
    ("Mahasiswa 1 (Ketua / Data Lead):", "Bertanggung jawab atas arsitektur penyimpanan 6 folder, modul storage.py, kompresi ZIP mandiri, dan integritas manifest SHA-256 (Bab 10 & 11)."),
    ("Mahasiswa 2 (Pipeline & Regex Lead):", "Bertanggung jawab atas modul upstream_scraper.py, requests & BeautifulSoup, modul cleaner.py, dan aturan ekstraksi Regex (Bab 9 & 13)."),
    ("Mahasiswa 3 (CLI & System Integrator):", "Bertanggung jawab atas modul cli.py (argparse & interactive menu), diagnostic doctor, serta implementasi MCP server WebSocket (Bab 12 & Nilai Tambah).")
]

for title, desc in team_roles:
    p = tf_t.add_paragraph()
    p.text = f"👤 {title}"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    
    p_sub = tf_t.add_paragraph()
    p_sub.text = f"   {desc}"
    p_sub.font.size = Pt(10.5)
    p_sub.font.color.rgb = TEXT_MUTED

# Q&A Box
qa_p = tf_t.add_paragraph()
qa_p.text = "\nSESI TANYA JAWAB (Q&A)"
qa_p.font.size = Pt(14)
qa_p.font.bold = True
qa_p.font.color.rgb = RGBColor(249, 226, 175) # Warm Yellow

qa_sub = tf_t.add_paragraph()
qa_sub.text = "Terima kasih atas perhatian Bapak/Ibu Dosen Penguji dan rekan-rekan. Kami siap mendemonstrasikan aplikasi dan menjawab pertanyaan."
qa_sub.font.size = Pt(10.5)
qa_sub.font.color.rgb = TEXT_MUTED

# Save presentation
prs.save(OUTPUT_PATH)
print(f"Presentation saved successfully with exactly {len(prs.slides)} slides to {OUTPUT_PATH}")

