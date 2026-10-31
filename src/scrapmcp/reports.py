"""Human-readable report of actual local dataset contents."""
from collections import Counter
from datetime import datetime, timezone
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from .storage import atomic_text, json_text

def write_report(root, rows):
    categories = dict(Counter(r['category'] for r in rows))
    events = []
    log = root / 'logs/events.jsonl'
    if log.exists():
        import json
        events = [json.loads(line) for line in log.read_text(encoding='utf-8').splitlines() if line]
    summary = {'generated_at':datetime.now(timezone.utc).isoformat(), 'records':len(rows),
               'words':sum(r['word_count'] for r in rows), 'categories':categories,
               'simulated_records':sum(r.get('dataset_kind') == 'simulation' for r in rows),
               'total_events':len(events),
               'failed_events':sum(not e['success'] for e in events)}
    folder = root / 'reports'
    folder.mkdir(exist_ok=True)
    atomic_text(folder/'summary.json', json_text(summary))
    text = '# Laporan Dataset ScrapMCP\n\n' + '\n'.join(f'- {k}: {v}' for k,v in summary.items())
    text += '\n\n## Sumber\n\n' + '\n'.join(f"- {r['title']} | {r['url']}" for r in rows)
    atomic_text(folder/'summary.md', text+'\n')
    styles = getSampleStyleSheet()
    story = [Paragraph('ScrapMCP | Laporan Dataset', styles['Title']), Spacer(1,16)]
    for label, value in [('Waktu (UTC)', summary['generated_at']), ('Total materi',len(rows)), ('Total kata',summary['words']), ('Materi simulasi',summary['simulated_records']), ('Total riwayat log tercatat',summary['total_events']), ('Operasi gagal tercatat',summary['failed_events'])]:
        story.append(Paragraph(f'<b>{label}:</b> {escape(str(value))}', styles['BodyText']))
    story.append(Spacer(1,16))
    data = [['Kategori','Jumlah']] + [[k,str(v)] for k,v in categories.items()]
    table = Table(data, colWidths=[340,100], repeatRows=1)
    table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#164e63')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('BOTTOMPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),9),('GRID',(0,0),(-1,-1),0.3,colors.lightgrey)]))
    story.extend([table, Spacer(1,18), Paragraph('Daftar sumber',styles['Heading2'])])
    for r in rows:
        story.append(Paragraph(escape(r['title']),styles['Heading3']))
        story.append(Paragraph(escape(r['url']),styles['BodyText']))
        story.append(Paragraph(f"ID: {r['id']} | {r['word_count']} kata | {escape(r.get('dataset_kind',''))}",styles['BodyText']))
    story.append(Spacer(1,16))
    story.append(Paragraph('Materi berlabel simulation berasal dari fixture buatan, bukan hasil pengambilan website langsung. Laporan ini merupakan rekap dataset, bukan penilaian kebenaran isi sumber.',styles['BodyText']))
    path = folder/'summary.pdf'
    SimpleDocTemplate(str(path),pagesize=A4,rightMargin=45,leftMargin=45,topMargin=45,bottomMargin=45).build(story)
    return {**summary, 'pdf':str(path), 'markdown':str(folder/'summary.md')}
