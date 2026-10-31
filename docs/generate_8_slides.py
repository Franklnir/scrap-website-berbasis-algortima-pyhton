#!/usr/bin/env python3
"""
Generate a simplified, concise 8-slide PowerPoint presentation for ScrapMCP.
With exact team member names:
- Irsyad (Ketua & Storage Architect)
- Sena Dwi Ilham (Scraper & Regex Specialist)
- Dhean Shafwan (CLI & IoT Integrator)
Optimized for NotebookLM ingestion and clean visual presentations:
- Concise, high-impact bullet points (no wall of text)
- 100% focused on application algorithms, modules, and architecture
- Clean modern aesthetic with generous breathing room
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_PATH = "/home/irsyad/Dokumen/scrapmcp-1.0.0-project/scrapmcp/docs/PRESENTASI_8_SLIDE.pptx"

# Initialize presentation with 16:9 widescreen
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette (Clean Modern Dark Theme)
DARK_BG = RGBColor(15, 23, 42)       # Slate 900
CARD_BG = RGBColor(30, 41, 59)       # Slate 800
CARD_BORDER = RGBColor(51, 65, 85)   # Slate 700
PRIMARY = RGBColor(14, 165, 233)     # Sky 500
ACCENT = RGBColor(16, 185, 129)      # Emerald 500
PURPLE = RGBColor(168, 85, 247)      # Purple 500
AMBER = RGBColor(245, 158, 11)       # Amber 500
ROSE = RGBColor(244, 63, 94)         # Rose 500
TEXT_MAIN = RGBColor(248, 250, 252)  # Slate 50
TEXT_MUTED = RGBColor(148, 163, 184) # Slate 400

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = DARK_BG

def add_header(slide, title_text, category_text="SCRAPMCP ARCHITECTURE"):
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.35))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = PRIMARY

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(23)
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
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = PRIMARY
        p.alignment = PP_ALIGN.LEFT
    return shape

# ==============================================================================
# SLIDE 1: Judul Aplikasi & Identitas Tim Proyek
# ==============================================================================
s1 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s1)

# Badge
badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.9), Inches(4.8), Inches(0.38))
badge.fill.solid()
badge.fill.fore_color.rgb = CARD_BG
badge.line.color.rgb = PRIMARY
b_p = badge.text_frame.paragraphs[0]
b_p.text = "PROYEK KELOMPOK OTOMATISASI PYTHON"
b_p.font.size = Pt(11)
b_p.font.bold = True
b_p.font.color.rgb = PRIMARY
b_p.alignment = PP_ALIGN.CENTER

# Main Title & Subtitle
title_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(2.3))
tf1 = title_box.text_frame
tf1.word_wrap = True

p1 = tf1.paragraphs[0]
p1.text = "SCRAPMCP"
p1.font.size = Pt(46)
p1.font.bold = True
p1.font.color.rgb = TEXT_MAIN

p2 = tf1.add_paragraph()
p2.text = "Sistem Otomatisasi Web Scraping, Pembersihan Regex & Pengarsipan Aman"
p2.font.size = Pt(19)
p2.font.bold = True
p2.font.color.rgb = PRIMARY

p3 = tf1.add_paragraph()
p3.text = "Solusi Cerdas Pengambilan Data Web Publik, Manajemen Direktori Terstruktur & Integrasi Perangkat IoT"
p3.font.size = Pt(13)
p3.font.color.rgb = TEXT_MUTED

# 3 Team Members Cards with exact names
roles = [
    ("IRSYAD", "Ketua & Storage Architect", 
     "• Arsitektur 6 Direktori Penyimpanan\n• Serialisasi JSON & Dataset CSV (RFC 4180)\n• Integritas Kriptografis SHA-256 MANIFEST"),
    ("SENA DWI ILHAM", "Scraper & Regex Specialist", 
     "• Web Scraping (Requests & BeautifulSoup)\n• Penelusuran Hierarki DOM & Pruning Tag\n• Ekstraksi Pola Regex & Frekuensi Kata"),
    ("DHEAN SHAFWAN", "CLI & IoT Integrator", 
     "• State Machine CLI REPL Menu [0–9]\n• Diagnostik Kesehatan Sistem (doctor)\n• Server WebSocket JSON-RPC 2.0 (MCP)")
]

for i, (name, role, desc) in enumerate(roles):
    x = Inches(0.8 + i * 4.0)
    card = add_card(s1, x, Inches(4.3), Inches(3.64), Inches(2.4), border_color=PRIMARY if i == 0 else CARD_BORDER)
    tf = card.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = name
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT if i == 0 else PRIMARY
    
    p_role = tf.add_paragraph()
    p_role.text = role
    p_role.font.size = Pt(11.5)
    p_role.font.bold = True
    p_role.font.color.rgb = TEXT_MAIN
    
    p_desc = tf.add_paragraph()
    p_desc.text = f"\n{desc}"
    p_desc.font.size = Pt(10.5)
    p_desc.font.color.rgb = TEXT_MUTED

# ==============================================================================
# SLIDE 2: Latar Belakang Masalah & Solusi
# ==============================================================================
s2 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s2)
add_header(s2, "Latar Belakang Masalah & Solusi Otomasi", "ANALISIS KEBUTUHAN SISTEM")

c_prob = add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.9), "Tantangan Pengelolaan Data Manual")
tf_p = c_prob.text_frame
tf_p.word_wrap = True
tf_p.paragraphs[0].text = "Problematika Manual Saat Ini:"
tf_p.paragraphs[0].font.size = Pt(15)
tf_p.paragraphs[0].font.bold = True
tf_p.paragraphs[0].font.color.rgb = ROSE

probs = [
    "• Manual & Lambat: Salin-tempel data menyita waktu dan rawan human-error.",
    "• Struktur Kotor: HTML mentah dipenuhi iklan, navigasi, dan skrip pelacak.",
    "• Tanpa Integritas: Berkas tidak terstruktur dan tidak memiliki validasi keaslian.",
    "• Format Berantakan: Data tercerai-berai tanpa indeks tabel atau dataset konsolidasi."
]

for p_text in probs:
    p = tf_p.add_paragraph()
    p.text = f"\n{p_text}"
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_MAIN

c_sol = add_card(s2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), "Solusi Sistemik ScrapMCP")
tf_s = c_sol.text_frame
tf_s.word_wrap = True
tf_s.paragraphs[0].text = "Solusi Otomasi ScrapMCP:"
tf_s.paragraphs[0].font.size = Pt(15)
tf_s.paragraphs[0].font.bold = True
tf_s.paragraphs[0].font.color.rgb = ACCENT

sols = [
    "✔ Ekstraksi Otomatis: Pengambilan data web terprogram via HTTP requests.",
    "✔ Pembersihan Cerdas: Pemangkasan tag DOM (BeautifulSoup) dan filter Regex.",
    "✔ Penyimpanan Terstruktur: Tata kelola 6 folder berjenjang dan indeks CSV global.",
    "✔ Arsip Terverifikasi: Kompresi ZIP mandiri dengan checksum SHA-256."
]

for s_text in sols:
    p = tf_s.add_paragraph()
    p.text = f"\n{s_text}"
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_MAIN

# ==============================================================================
# SLIDE 3: Pemetaan Algoritma & Modul Aplikasi
# ==============================================================================
s3 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s3)
add_header(s3, "Arsitektur Algoritma & Modul Inti Aplikasi", "PETA SUBSISTEM PIPELINE")

algo_cards = [
    ("Crawler Engine", "upstream_scraper.py", "DOM Traversal & Ingestion",
     "• HTTP GET via requests\n• Depth-first DOM traversal\n• Heuristic container scoring\n• Multi-search autonomous"),
    
    ("Text Intelligence", "cleaner.py", "Pattern Matching Regex",
     "• Regex DFA pattern matching\n• Filter email, WA, dan harga\n• Perhitungan frekuensi kata\n• Auto-slug generator"),

    ("Data Persistence", "storage.py", "Atomic I/O & Indexing",
     "• Atomic file write stream\n• Serialisasi metadata JSON\n• Append dataset global CSV\n• Konsistensi data tinggi"),

    ("Secure Archiving", "storage.py", "Kompresi & Kriptografi",
     "• Algoritma DEFLATE (ZIP)\n• Isolasi arsip per riset\n• Hashing SHA-256 berkas\n• Pembuatan MANIFEST.json"),

    ("Hardware Bridge", "mcp_server.py", "Server WebSocket",
     "• Transport JSON-RPC 2.0\n• Port ws://127.0.0.1:8765\n• Eksekusi tool non-blocking\n• Jembatan perangkat fisik")
]

card_w = Inches(2.2)
card_h = Inches(4.9)
for i, (mod_title, mod_file, algo, detail) in enumerate(algo_cards):
    x = Inches(0.8 + i * 2.4)
    card = add_card(s3, x, Inches(1.8), card_w, card_h, border_color=PRIMARY if i == 0 or i == 1 else CARD_BORDER)
    tf = card.text_frame
    tf.word_wrap = True
    
    p_chap = tf.paragraphs[0]
    p_chap.text = mod_title
    p_chap.font.size = Pt(13)
    p_chap.font.bold = True
    p_chap.font.color.rgb = PRIMARY
    
    p_mat = tf.add_paragraph()
    p_mat.text = mod_file
    p_mat.font.size = Pt(10.5)
    p_mat.font.bold = True
    p_mat.font.color.rgb = TEXT_MAIN
    
    p_alg = tf.add_paragraph()
    p_alg.text = algo
    p_alg.font.size = Pt(9.5)
    p_alg.font.bold = True
    p_alg.font.color.rgb = ACCENT
    
    p_det = tf.add_paragraph()
    p_det.text = f"\n{detail}"
    p_det.font.size = Pt(10)
    p_det.font.color.rgb = TEXT_MUTED

# ==============================================================================
# SLIDE 4: Alur Pengambilan Data & Parsing HTML
# ==============================================================================
s4 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s4)
add_header(s4, "Alur Pengambilan Data & Parsing HTML", "MODUL WEB SCRAPING & DOKUMEN PARSER")

c_req = add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.9), "HTTP Ingestion (requests)")
tf_req = c_req.text_frame
tf_req.word_wrap = True
tf_req.paragraphs[0].text = "1. Mekanisme Ingestion HTTP (requests):"
tf_req.paragraphs[0].font.size = Pt(14)
tf_req.paragraphs[0].font.bold = True
tf_req.paragraphs[0].font.color.rgb = PRIMARY

req_pts = [
    ("HTTP GET Terprogram:", "Mengambil konten web dengan batasan timeout 12 detik."),
    ("Validasi Skema & Respon:", "Memastikan protokol http/https dan verifikasi kode status 200 OK."),
    ("Kueri Multi-Mesin:", "Riset otomatis multi-sumber (Bing Search & Wikipedia) berbasis topik."),
    ("Salinan Mentah Orisinal:", "Kode HTML mentah disimpan utuh ke raw/ (raw.html) untuk audit.")
]

for title, desc in req_pts:
    p = tf_req.add_paragraph()
    p.text = f"\n▶ {title} {desc}"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MAIN

c_dom = add_card(s4, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), "DOM Parsing (BeautifulSoup)")
tf_dom = c_dom.text_frame
tf_dom.word_wrap = True
tf_dom.paragraphs[0].text = "2. Parsing Pohon Elemen HTML (BeautifulSoup):"
tf_dom.paragraphs[0].font.size = Pt(14)
tf_dom.paragraphs[0].font.bold = True
tf_dom.paragraphs[0].font.color.rgb = ACCENT

dom_pts = [
    ("Pruning Tag:", "Menghapus otomatis tag <script>, <style>, <nav>, <footer>, dan iklan."),
    ("Heuristik Konten:", "Mengekstrak kontainer utama secara cerdas (<main>, <article>, #content)."),
    ("Transformasi Format:", "Mengubah judul ke heading rapi, teks ke paragraf bersih, dan tabel ke format Markdown."),
    ("Output Bersih:", "Menghasilkan teks murni bebas noise untuk diproses ke modul pembersih Regex.")
]

for title, desc in dom_pts:
    p = tf_dom.add_paragraph()
    p.text = f"\n▶ {title} {desc}"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MAIN

# ==============================================================================
# SLIDE 5: Ekstraksi Regex & Analisis Teks
# ==============================================================================
s5 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s5)
add_header(s5, "Ekstraksi Regex & Analisis Teks", "MODUL TEXT CLEANER & ENTITY EXTRACTION")

c_rgx = add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.9), "Pola Regex Deterministik")
tf_rgx = c_rgx.text_frame
tf_rgx.word_wrap = True
tf_rgx.paragraphs[0].text = "1. Ekstraksi Pola Regex (re.compile):"
tf_rgx.paragraphs[0].font.size = Pt(14)
tf_rgx.paragraphs[0].font.bold = True
tf_rgx.paragraphs[0].font.color.rgb = PRIMARY

patterns = [
    ("Email Kontak:", r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "Deteksi alamat email resmi."),
    ("WhatsApp / HP:", r"(\+62|62|08)[0-9]{8,12}", "Deteksi nomor seluler lokal & internasional."),
    ("Harga Produk:", r"Rp\s?[0-9]{1,3}(?:\.[0-9]{3})*", "Deteksi angka nominal mata uang Rp."),
    ("Normalisasi Spasi:", r"re.sub(r'\s+', ' ', text)", "Pembersihan tabulasi & baris berlebih.")
]

for label, ptn, note in patterns:
    p = tf_rgx.add_paragraph()
    p.text = f"\n• {label} {note}\n  Regex: {ptn}"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MAIN

c_slug = add_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), "Pemrosesan Konten Cerdas")
tf_slug = c_slug.text_frame
tf_slug.word_wrap = True
tf_slug.paragraphs[0].text = "2. Analisis Kata & Slug Generator:"
tf_slug.paragraphs[0].font.size = Pt(14)
tf_slug.paragraphs[0].font.bold = True
tf_slug.paragraphs[0].font.color.rgb = ACCENT

slug_pts = [
    ("Eliminasi Stopword:", "Menyaring kata umum bahasa Indonesia (di, ke, dari, yang)."),
    ("Pembobotan Frekuensi:", "Menghitung kata terbanyak via collections.Counter."),
    ("Auto-Slug Generator:", "Penamaan otomatis berkas arsip berdasarkan topik riset."),
    ("Hasil Intuitif:", "Arsip bernama jelas (misal: riset_katalog-produk-irsyadlabs.zip).")
]

for title, desc in slug_pts:
    p = tf_slug.add_paragraph()
    p.text = f"\n▶ {title} {desc}"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MAIN

# ==============================================================================
# SLIDE 6: Struktur Direktori & Integritas Data
# ==============================================================================
s6 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s6)
add_header(s6, "Struktur Direktori & Integritas Data", "MODUL STORAGE & DATA ARCHIVING")

strats = [
    ("6 STRUKTUR DIREKTORI", "Tata Kelola Folder",
     "• raw/ : Berkas HTML asli\n• processed/ : Teks bersih & JSON\n• backups/ : Arsip ZIP mandiri\n• exports/ : Dataset CSV global\n• reports/ : Laporan audit sistem\n• logs/ : Audit trail CLI"),
    
    ("ISOLASI ARSIP MANDIRI", "Kompresi DEFLATE",
     "• Format: riset_{slug}_{hash}.zip\n• 1 riset = 1 berkas ZIP mandiri\n• Data riset tidak saling campur\n• Berisi raw, clean, meta, & manifest"),
    
    ("KRIPTOGRAFI SHA-256", "Integritas Berkas",
     "• Hashing via buffer 64 KB\n• Hemat RAM dan konsisten\n• Dicatat pada MANIFEST.json\n• Menjamin data tidak korup/berubah")
]

for i, (st_t, st_sub, st_desc) in enumerate(strats):
    x = Inches(0.8 + i * 4.0)
    card = add_card(s6, x, Inches(1.8), Inches(3.64), Inches(2.7), border_color=PRIMARY if i == 1 else CARD_BORDER)
    tf = card.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = st_t
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT if i == 1 else PRIMARY
    
    p_s = tf.add_paragraph()
    p_s.text = st_sub
    p_s.font.size = Pt(11)
    p_s.font.bold = True
    p_s.font.color.rgb = TEXT_MAIN
    
    p_d = tf.add_paragraph()
    p_d.text = f"\n{st_desc}"
    p_d.font.size = Pt(10.5)
    p_d.font.color.rgb = TEXT_MUTED

# Workflow box (Bottom)
code_card = add_card(s6, Inches(0.8), Inches(4.7), Inches(11.6), Inches(2.0), "Siklus Data Terorganisir:", border_color=ACCENT)
tf_c = code_card.text_frame
tf_c.word_wrap = True

steps_csv = [
    "1. Atomic Write: Menulis berkas sementara lalu me-rename agar tidak rusak saat interupsi.",
    "2. Metadata JSON: Menyimpan metadata riset (waktu, statistik kata, regex) ke JSON.",
    "3. Indeks CSV (RFC 4180): Setiap sesi riset otomatis ditambahkan (append) ke dataset.csv.",
    "4. Verifikasi Checksum: Validasi ulang seluruh hash berkas sebelum arsip ZIP difinalisasi."
]

for row in steps_csv:
    p = tf_c.add_paragraph()
    p.text = f"✔ {row}"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MAIN

# ==============================================================================
# SLIDE 7: Integrasi Server WebSocket & Perangkat Keras Eksternal
# ==============================================================================
s7 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s7)
add_header(s7, "Integrasi Server WebSocket & Perangkat Keras Eksternal", "KONEKTIVITAS PROTOKOL TERBUKA & PERANGKAT FISIK")

c_mcp = add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.9), "Server WebSocket JSON-RPC 2.0")
tf_m = c_mcp.text_frame
tf_m.word_wrap = True
tf_m.paragraphs[0].text = "Protokol Komunikasi WebSocket:"
tf_m.paragraphs[0].font.size = Pt(14)
tf_m.paragraphs[0].font.bold = True
tf_m.paragraphs[0].font.color.rgb = PRIMARY

mcp_pts = [
    ("Endpoint Server:", "Berjalan pada ws://127.0.0.1:8765 dengan latensi sangat rendah (< 50 ms)."),
    ("Prosedur Modular Siap Panggil:", "Mengekspos fungsi scraping dan pembersihan data sebagai API modular."),
    ("Daftar Tool Aktif:", "scrape_and_summarize, search_and_research, dan create_research_zip."),
    ("Isolasi Sandbox:", "Operasi dibatasi hanya pada direktori data yang aman.")
]

for title, desc in mcp_pts:
    p = tf_m.add_paragraph()
    p.text = f"\n⚡ {title} {desc}"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MAIN

c_voice = add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), "Integrasi Perangkat Keras Eksternal")
tf_v = c_voice.text_frame
tf_v.word_wrap = True
tf_v.paragraphs[0].text = "Interaksi Perangkat Fisik Eksternal:"
tf_v.paragraphs[0].font.size = Pt(14)
tf_v.paragraphs[0].font.bold = True
tf_v.paragraphs[0].font.color.rgb = PURPLE

voice_pts = [
    ("Sinyal Kendali Input:", "Menerima sinyal kendali input dari perangkat keras kontrol fisik via soket jaringan."),
    ("Eksekusi Non-Blocking:", "Berjalan di latar belakang tanpa membebani antarmuka pengguna."),
    ("Transmisi Real-Time:", "Transmisi hasil ekstraksi teks bersih langsung ke perangkat klien secara seketika."),
    ("Pemanfaatan Nyata:", "Dapat disambungkan ke voice box AI (Xiaozhi) untuk riset suara bebas ketik.")
]

for title, desc in voice_pts:
    p = tf_v.add_paragraph()
    p.text = f"\n🎙 {title} {desc}"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MAIN

# ==============================================================================
# SLIDE 8: Hasil Pengujian & Evaluasi
# ==============================================================================
s8 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s8)
add_header(s8, "Hasil Pengujian Sistem & Evaluasi Tim", "DEMONSTRASI APLIKASI & SESI TANYA JAWAB")

c_eval = add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.9), "Hasil Pengujian Sistem")
tf_e = c_eval.text_frame
tf_e.word_wrap = True
tf_e.paragraphs[0].text = "Metrik Validasi & Pengujian Nyata:"
tf_e.paragraphs[0].font.size = Pt(14)
tf_e.paragraphs[0].font.bold = True
tf_e.paragraphs[0].font.color.rgb = ACCENT

eval_items = [
    ("Uji Langsung:", "Scraping pada situs publik berhasil mengekstrak 2.759 kata, kontak WA, dan harga produk."),
    ("Unit Testing:", "21 pengujian otomatis lulus 100% (zero regression)."),
    ("Integritas Berkas:", "100% berkas dalam arsip ZIP cocok dengan hash MANIFEST.json."),
    ("Efisiensi Memori:", "Pengoperasian stabil dan hemat konsumsi memori (< 45 MB RAM).")
]

for title, desc in eval_items:
    p = tf_e.add_paragraph()
    p.text = f"\n★ {title} {desc}"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MAIN

c_team = add_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9), "Tanggung Jawab Tim Saat Tanya Jawab")
tf_tm = c_team.text_frame
tf_tm.word_wrap = True
tf_tm.paragraphs[0].text = "Pembagian Tugas Saat Evaluasi / Tanya Jawab:"
tf_tm.paragraphs[0].font.size = Pt(14)
tf_tm.paragraphs[0].font.bold = True
tf_tm.paragraphs[0].font.color.rgb = PRIMARY

team_dist = [
    ("Irsyad (Ketua & Storage Architect):", "Menjawab seputar storage.py, struktur 6 folder, dataset CSV/JSON, dan hash SHA-256."),
    ("Sena Dwi Ilham (Scraper & Regex Lead):", "Menjawab seputar upstream_scraper.py (requests & BS4), struktur DOM, dan pola Regex cleaner.py."),
    ("Dhean Shafwan (CLI & IoT Integrator):", "Mendemonstrasikan menu interaktif CLI terminal, diagnostik doctor, dan koneksi server WebSocket.")
]

for title, desc in team_dist:
    p = tf_tm.add_paragraph()
    p.text = f"\n👤 {title} {desc}"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MAIN

# Q&A Box
qa_p = tf_tm.add_paragraph()
qa_p.text = "\nSESI TANYA JAWAB (Q&A)"
qa_p.font.size = Pt(13)
qa_p.font.bold = True
qa_p.font.color.rgb = RGBColor(249, 226, 175)

qa_sub = tf_tm.add_paragraph()
qa_sub.text = "Terima kasih atas perhatian Bapak/Ibu Dosen Penguji. Kami siap mendemonstrasikan sistem dan menjawab pertanyaan."
qa_sub.font.size = Pt(10)
qa_sub.font.color.rgb = TEXT_MUTED

# Save presentation
prs.save(OUTPUT_PATH)
print(f"Presentation saved successfully with exactly {len(prs.slides)} slides to {OUTPUT_PATH}")
