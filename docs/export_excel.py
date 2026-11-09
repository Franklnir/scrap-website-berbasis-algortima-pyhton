#!/usr/bin/env python3
"""
Generate a rich, beautifully formatted Microsoft Excel (.xlsx) file and enhanced CSV
from the scraped records in ~/scrapmcp-data/exports/dataset.json.
"""
import json
import csv
from pathlib import Path
import xlsxwriter

DATA_DIR = Path("/home/irsyad/scrapmcp-data/exports")
JSON_FILE = DATA_DIR / "dataset.json"
XLSX_FILE = DATA_DIR / "dataset.xlsx"
CSV_FILE = DATA_DIR / "dataset.csv"

def generate_excel_and_rich_csv():
    if not JSON_FILE.exists():
        print(f"File {JSON_FILE} not found.")
        return

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)

    print(f"Loaded {len(records)} records from {JSON_FILE}")

    # 1. Update dataset.csv with a summary column
    csv_fields = ["id", "title", "category", "word_count", "summary", "url", "saved_at", "digest"]
    with open(CSV_FILE, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction="ignore")
        writer.writeheader()
        for r in records:
            content = r.get("content", "")
            # Clean content excerpt for CSV
            excerpt = r.get("description") or (content[:250].replace("\n", " ").strip() + "...")
            row = {
                "id": r.get("id", ""),
                "title": r.get("title", ""),
                "category": r.get("category", ""),
                "word_count": r.get("word_count", 0),
                "summary": excerpt,
                "url": r.get("url", ""),
                "saved_at": r.get("saved_at", ""),
                "digest": r.get("digest", "")[:16] + "..." if r.get("digest") else ""
            }
            writer.writerow(row)
    print(f"Updated {CSV_FILE} with rich summary columns.")

    # 2. Build gorgeous Excel (.xlsx) file
    workbook = xlsxwriter.Workbook(str(XLSX_FILE))
    worksheet = workbook.add_worksheet("Dataset Hasil Scraping")

    # Formats
    header_format = workbook.add_format({
        "bold": True,
        "font_color": "#FFFFFF",
        "bg_color": "#1E7E34",  # Excel Green
        "border": 1,
        "align": "center",
        "valign": "vcenter",
        "font_size": 11
    })

    cell_format = workbook.add_format({
        "border": 1,
        "valign": "top",
        "text_wrap": True,
        "font_size": 10
    })

    alt_cell_format = workbook.add_format({
        "border": 1,
        "valign": "top",
        "text_wrap": True,
        "bg_color": "#F8FAFC",
        "font_size": 10
    })

    number_format = workbook.add_format({
        "border": 1,
        "align": "right",
        "valign": "top",
        "font_size": 10
    })

    link_format = workbook.add_format({
        "border": 1,
        "valign": "top",
        "font_color": "#1D4ED8",
        "underline": True,
        "text_wrap": True,
        "font_size": 10
    })

    headers = [
        ("No", 6),
        ("ID Dokumen", 28),
        ("Judul Materi / Halaman", 42),
        ("Kategori", 16),
        ("Jumlah Kata", 14),
        ("Ringkasan Isi Hasil Scraping", 65),
        ("URL Sumber Asli", 35),
        ("Waktu Pengambilan", 22),
        ("Integritas SHA-256 (Katalog)", 20)
    ]

    # Write headers
    worksheet.set_row(0, 28)
    for col_idx, (hdr_text, col_w) in enumerate(headers):
        worksheet.write(0, col_idx, hdr_text, header_format)
        worksheet.set_column(col_idx, col_idx, col_w)

    # Write rows
    for row_idx, r in enumerate(records, start=1):
        cf = alt_cell_format if row_idx % 2 == 0 else cell_format
        worksheet.set_row(row_idx, 55)

        content = r.get("content", "")
        summary_text = r.get("description") or (content[:350].replace("\n", " ").strip() + "...")
        url = r.get("url", "")
        sha_hash = r.get("digest", "")
        short_hash = sha_hash[:16] + "..." if sha_hash else "-"

        worksheet.write(row_idx, 0, row_idx, cf)
        worksheet.write(row_idx, 1, r.get("id", ""), cf)
        worksheet.write(row_idx, 2, r.get("title", ""), cf)
        worksheet.write(row_idx, 3, r.get("category", ""), cf)
        worksheet.write_number(row_idx, 4, r.get("word_count", 0), number_format)
        worksheet.write(row_idx, 5, summary_text, cf)
        if url.startswith("http"):
            worksheet.write_url(row_idx, 6, url, link_format, string=url)
        else:
            worksheet.write(row_idx, 6, url, cf)
        worksheet.write(row_idx, 7, r.get("saved_at", "")[:19].replace("T", " "), cf)
        worksheet.write(row_idx, 8, short_hash, cf)

    workbook.close()
    print(f"Successfully generated {XLSX_FILE} with {len(records)} rows!")

if __name__ == "__main__":
    generate_excel_and_rich_csv()

