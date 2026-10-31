#!/usr/bin/env python3
"""
Generate a professional PDF Report centered on Screenshots / Visual Documentation.
Follows user requirements:
- Features screenshots prominently
- Exact team names: Irsyad, Sena Dwi Ilham, Dhean Shafwan
- No textbook chapter numbering labels
- Pure web scraping & application focus
"""
import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from PIL import Image as PILImg

PDF_OUTPUT_PATH = "/home/irsyad/Dokumen/scrapmcp-1.0.0-project/scrapmcp/docs/DOKUMENTASI_TANGKAPAN_LAYAR.pdf"
SCREENSHOTS_DIR = Path("/home/irsyad/Dokumen/scrapmcp-1.0.0-project/scrapmcp/docs/screenshots")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Top Running Header (from page 2 onwards)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#0284C7")) # Sky 600
            self.drawString(40, A4[1] - 30, "SCRAPMCP — LAPORAN DOKUMENTASI VISUAL & TANGKAPAN LAYAR")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(A4[0] - 40, A4[1] - 30, "Kelompok 3: Irsyad, Sena Dwi Ilham, Dhean Shafwan")
            
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(40, A4[1] - 34, A4[0] - 40, A4[1] - 34)

        # Bottom Running Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(40, 38, A4[0] - 40, 38)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(40, 26, "Tugas Besar Otomatisasi Python • ScrapMCP v1.0.0")
        
        page_str = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawRightString(A4[0] - 40, 26, page_str)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0F172A"),
        alignment=1,
        spaceAfter=5
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0369A1"),
        alignment=1,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceAfter=5
    )

    caption_style = ParagraphStyle(
        'ImgCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0284C7"),
        alignment=1,
        spaceBefore=4,
        spaceAfter=6
    )

    tip_style = ParagraphStyle(
        'TipText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#475569"),
        alignment=0,
        spaceAfter=4
    )

    story = []

    # ================= COVER / HEADER =================
    story.append(Paragraph("LAPORAN DOKUMENTASI VISUAL & TANGKAPAN LAYAR", title_style))
    story.append(Paragraph("SCRAPMCP: SISTEM OTOMATISASI WEB SCRAPING, PEMBERSIHAN REGEX & PENGARSIPAN AMAN", subtitle_style))
    
    # Meta Box Table with exact names
    meta_data = [
        [
            Paragraph("<b>Mata Kuliah:</b> Pemrograman Python Otomatisasi", body_style),
            Paragraph("<b>Bentuk Ujian:</b> Proyek Kelompok (3 Mahasiswa)", body_style)
        ],
        [
            Paragraph("<b>Kelompok 3:</b><br/>• <b>Irsyad</b> (Ketua & Storage Architect)<br/>• <b>Sena Dwi Ilham</b> (Scraper & Regex Specialist)<br/>• <b>Dhean Shafwan</b> (CLI & IoT Integrator)", body_style),
            Paragraph("<b>Arsitektur Program:</b><br/>• Bahasa: Python 3.12+ (Linux CLI)<br/>• Engine Scraper: Requests & BeautifulSoup<br/>• Engine Regex: re (DFA Pattern Matching)<br/>• Antarmuka: CLI State Machine & WebSocket MCP", body_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[255, 260])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # Note on screenshot replacement
    note_box = [
        [Paragraph("<b>PANDUAN PENGGANTIAN TANGKAPAN LAYAR (UNTUK MAHASISWA):</b><br/>"
                   "Dokumen ini memuat bukti tangkapan layar sistem. Seluruh foto tersimpan di direktori <code>docs/screenshots/</code> dalam format PNG. "
                   "Anda dapat mengganti foto-foto ini dengan screenshot layar terminal Anda sendiri kapan saja dengan nama berkas yang sama, "
                   "lalu jalankan: <code>python docs/generate_screenshot_report.py</code>.", tip_style)]
    ]
    t_note = Table(note_box, colWidths=[515])
    t_note.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_note)
    story.append(Spacer(1, 10))

    # ================= VISUAL ITEMS =================
    items = [
        {
            "img": "01_cli_menu.png",
            "title": "Tangkapan Layar 1: Antarmuka Terminal & Menu Interaktif CLI",
            "modul": "Modul cli.py (Command Center & State Machine Menu [0–9])",
            "desc": "Tangkapan layar di atas memperlihatkan antarmuka Command Line Interface (CLI) saat dijalankan dengan perintah <code>python -m scrapmcp.cli --interactive</code>. Sistem menyajikan diagnostik otomatis (Storage Base, Network Scraper, dan WebSocket MCP), serta daftar 9 menu aksi yang memungkinkan pengguna mengeksekusi operasi otomatisasi secara langsung.",
            "tech": "Argumen CLI dikelola oleh <code>argparse.ArgumentParser</code> dan loop eksekusi interaktif dengan validasi input numerik.",
            "file": "01_cli_menu.png"
        },
        {
            "img": "02_scraping_process.png",
            "title": "Tangkapan Layar 2: Eksekusi Web Scraping & Ekstraksi Regex",
            "modul": "Modul upstream_scraper.py (Requests & BS4) dan cleaner.py (Regex)",
            "desc": "Tangkapan layar di atas mendokumentasikan proses scraping pada website live <code>https://produk.irsyadlabs.id/</code>. Sistem mengirim request HTTP 200 OK dengan custom User-Agent, parsing DOM kontainer utama (2.759 kata berhasil diekstrak), serta eksekusi pola ekspresi reguler untuk mendeteksi email, kontak WhatsApp, dan format harga (Rp).",
            "tech": "Ekstraksi konten menggunakan <code>BeautifulSoup(html, 'html.parser')</code> dan filter regex via <code>re.findall()</code>.",
            "file": "02_scraping_process.png"
        },
        {
            "img": "03_folder_structure.png",
            "title": "Tangkapan Layar 3: Struktur 6 Folder Penyimpanan Data Terorganisir",
            "modul": "Modul storage.py (Arsitektur Direktori Data Terstruktur)",
            "desc": "Tangkapan layar di atas memperlihatkan pengelompokan 6 folder utama pada sistem penyimpanan data (<code>~/scrapmcp-data/</code>). Folder terdiri dari: <b>raw</b> (dokumen HTML mentah), <b>processed</b> (teks hasil pembersihan & JSON), <b>backups</b> (arsip ZIP mandiri per riset), <b>exports</b> (dataset CSV konsolidasi), <b>reports</b> (laporan audit), dan <b>logs</b> (catatan jejak eksekusi sistem).",
            "tech": "Modul: <code>scrapmcp/storage.py</code> membuat dan mengelola hierarki direktori secara otomatis menggunakan <code>pathlib.Path</code>.",
            "file": "03_folder_structure.png"
        },
        {
            "img": "04_dataset_spreadsheet.png",
            "title": "Tangkapan Layar 4: Dataset CSV Terorganisir Terbuka di Spreadsheet",
            "modul": "Modul storage.py & exports/dataset.csv (Serialisasi Tabular)",
            "desc": "Tangkapan layar di atas memperlihatkan berkas luaran <code>dataset.csv</code> yang dibuka pada aplikasi spreadsheet. Setiap baris mewakili satu rekaman riset yang terstruktur rapi dengan kolom: ID, Title, Category, URL, Word Count, dan Checksum SHA-256. Data siap digunakan untuk analisis statistik dan integrasi basis data lanjutan.",
            "tech": "Penulisan tabular dilakukan dengan penguncian mekanis dan kepatuhan standar CSV RFC 4180 melalui <code>csv.DictWriter</code>.",
            "file": "04_dataset_spreadsheet.png"
        },
        {
            "img": "05_backup_zip_manifest.png",
            "title": "Tangkapan Layar 5: Arsip ZIP Mandiri per Riset & Katalog MANIFEST SHA-256",
            "modul": "Modul storage.py (Kompresi DEFLATE & Checksum Integritas)",
            "desc": "Tangkapan layar di atas membuktikan fitur isolasi data: setiap sesi riset dikompresi ke dalam satu berkas ZIP mandiri (misal: <code>riset_katalog-produk-irsyadlabs_a7f4c91b.zip</code>) tanpa tercampur. Di dalam arsip tersimpan berkas <code>raw.html</code>, <code>clean.txt</code>, <code>meta.json</code>, serta berkas integritas <code>MANIFEST.json</code> berisi hash SHA-256 tiap file.",
            "tech": "Metode <code>Store.package_record_zip()</code> menjamin pemulihan data (disaster recovery) dan pembuktian keaslian berkas.",
            "file": "05_backup_zip_manifest.png"
        },
        {
            "img": "06_mcp_voice_bridge.png",
            "title": "Tangkapan Layar 6: Server WebSocket & Integrasi Perangkat Keras Eksternal",
            "modul": "Modul mcp_server.py (WebSocket JSON-RPC 2.0 & Hardware Bridge)",
            "desc": "Tangkapan layar di atas memperlihatkan server WebSocket yang aktif melayani koneksi pada <code>ws://127.0.0.1:8765</code>. Server ini menghubungkan perangkat keras fisik eksternal (Voice AI Box) dengan modul ScrapMCP. Ketika pengguna memberikan instruksi suara, server mengeksekusi pipeline di background dan mengirim hasil secara real-time.",
            "tech": "Implementasi RPC asynchronous berbasis WebSocket dan spesifikasi Model Context Protocol untuk koneksi agen AI.",
            "file": "06_mcp_voice_bridge.png"
        }
    ]

    for idx, item in enumerate(items):
        img_path = SCREENSHOTS_DIR / item["img"]
        
        story.append(Paragraph(f"<b>{item['title']}</b>", h1_style))
        story.append(Paragraph(f"<b>Komponen Modul:</b> <font color='#0284C7'>{item['modul']}</font>", body_style))
        story.append(Spacer(1, 4))

        if img_path.exists():
            with PILImg.open(img_path) as p_img:
                iw, ih = p_img.size
            
            target_w = 495
            target_h = target_w * (ih / iw)
            if target_h > 245:
                target_h = 245
                target_w = target_h * (iw / ih)

            rl_img = RLImage(str(img_path), width=target_w, height=target_h)
            
            img_table = Table([[rl_img]], colWidths=[515])
            img_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
                ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#334155")),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(img_table)
            story.append(Paragraph(f"<i>Gambar {idx+1}: Sumber berkas: <code>docs/screenshots/{item['file']}</code></i>", caption_style))
        
        story.append(Paragraph(f"<b>Deskripsi Operasional:</b> {item['desc']}", body_style))
        story.append(Paragraph(f"<b>Implementasi Teknis:</b> {item['tech']}", body_style))
        story.append(Spacer(1, 8))
        
        if idx < len(items) - 1:
            story.append(PageBreak())

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF screenshot report generated successfully at: {PDF_OUTPUT_PATH}")

if __name__ == "__main__":
    build_pdf()
