"""Ch.10/11: atomic files, category folders, CSV/JSON and ZIP backup."""
import csv
import hashlib
import io
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from filelock import FileLock
from .engine import clean_record

def slug(text):
    value = re.sub(r'[^a-z0-9]+', '-', str(text).lower()).strip('-')[:60] or 'umum'
    if value.upper() in {'CON','PRN','AUX','NUL', *(f'COM{i}' for i in range(10)), *(f'LPT{i}' for i in range(10))}:
        value = 'category-' + value
    return value

def clean_title_for_slug(title):
    t = str(title or '').strip()
    t = re.sub(r'^(transkrip|pdf|artikel|jurnal|laporan|berita|video|catatan)\s*[:\-\|]\s*', '', t, flags=re.IGNORECASE).strip()
    t = re.sub(r'\s+[-–|•]\s+[\w\.\s]+$', '', t).strip()
    return t

def shorten_slug(s, max_len=45):
    s = s.strip('-')
    if len(s) <= max_len:
        return s
    cut = s[:max_len]
    last_dash = cut.rfind('-')
    if last_dash >= 15:
        return cut[:last_dash]
    return cut.rstrip('-')

def make_content_slug(record):
    title = clean_title_for_slug(record.get('title'))
    base_slug = slug(title).strip('-')
    if base_slug and len(base_slug) >= 2 and base_slug not in {'umum', 'untitled', 'home', 'index', 'halaman'}:
        return shorten_slug(base_slug, 45)

    desc = record.get('abstract') or record.get('description') or ''
    if desc:
        desc_clean = re.sub(r'^(berita|artikel|ringkasan)\s*', '', desc, flags=re.IGNORECASE).strip()
        desc_slug = slug(desc_clean).strip('-')
        if desc_slug and len(desc_slug) >= 2 and desc_slug not in {'umum', 'untitled', 'home', 'index', 'halaman'}:
            return shorten_slug(desc_slug, 45)

    content = record.get('content', '')
    for raw_line in content.split('\n'):
        line = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', raw_line)
        line = re.sub(r'[\*\_\`\#\>\-\•\:\d\.]+', ' ', line).strip()
        s = slug(line).strip('-')
        if s and len(s) >= 4 and s not in {'umum', 'untitled', 'home', 'index', 'halaman'}:
            return shorten_slug(s, 45)

    return 'materi-riset'

def atomic_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    with open(tmp, 'w', encoding='utf-8', newline='') as stream:
        stream.write(text)
    os.replace(tmp, path)

def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2)

class Store:
    def __init__(self, root):
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.lock = FileLock(str(self.root / '.store.lock'), timeout=60)

    def records(self):
        rows = []
        for path in sorted((self.root / 'processed').glob('*/*/*.json')):
            if path.is_symlink() or self.root not in path.resolve().parents:
                continue
            with open(path, encoding='utf-8') as stream:
                rows.append(json.load(stream))
        return rows

    def save(self, raw, category='umum'):
        record = clean_record(raw)
        if not record.get('content', '').strip():
            raise ValueError('Konten kosong tidak disimpan.')
        url = record.get('url') or record.get('source_url') or ''
        category = slug(category)
        digest = hashlib.sha256((url + '\n' + record['content'] + '\n' + category).encode()).hexdigest()
        content_slug = make_content_slug(record)
        identity = f"{content_slug}_{digest[:8]}"
        with self.lock:
            existing = next((r for r in self.records() if r.get('id') == identity or r.get('digest') == digest or r.get('id', '').startswith(digest[:8]) or r.get('id', '').endswith(digest[:8])), None)
            if existing:
                return {**existing, 'duplicate': True}
            now = datetime.now(timezone.utc)
            record.update(id=identity, digest=digest, url=url, category=category, saved_at=now.isoformat(), dataset_kind=record.get('dataset_kind','public_web'))
            rel = Path(category) / now.strftime('%Y-%m-%d') / identity
            atomic_text(self.root / 'raw' / rel.with_suffix('.json'), json_text(raw))
            atomic_text(self.root / 'processed' / rel.with_suffix('.md'), record['content'])
            atomic_text(self.root / 'processed' / rel.with_suffix('.json'), json_text(record))
            self._export()
            zip_info = self.package_record_zip(record)
            record['zip_backup'] = zip_info['path']
            return {**record, 'duplicate': False}

    def _export(self):
        rows = self.records()
        atomic_text(self.root / 'exports/dataset.json', json_text(rows))
        fields = ['id','title','url','category','source_type','dataset_kind','word_count','saved_at']
        stream = io.StringIO(newline='')
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            # Prevent spreadsheet formula execution when opening a scraped title.
            writer.writerow({k: ("'"+v if isinstance(v,str) and v.startswith(('=','+','-','@')) else v) for k,v in row.items()})
        atomic_text(self.root / 'exports/dataset.csv', '\ufeff' + stream.getvalue())
        return len(rows)

    def export(self):
        with self.lock:
            res = {'records': self._export(), 'json': str(self.root/'exports/dataset.json'), 'csv': str(self.root/'exports/dataset.csv')}
            self.event('export', True, f"{res['records']} materi diekspor")
            return res

    def read(self, record_id):
        target = str(record_id).strip()
        for row in self.records():
            row_id = str(row.get('id', ''))
            row_digest = str(row.get('digest', ''))
            if target == row_id:
                return row
            if row_digest and target == row_digest:
                return row
            if len(target) >= 6 and (target in row_id or (row_digest and row_digest.startswith(target))):
                return row
        raise ValueError('ID materi tidak ditemukan.')

    def event(self, operation, success, detail=''):
        with self.lock:
            log_dir = self.root / 'logs'
            log_dir.mkdir(parents=True, exist_ok=True)
            iso_time = datetime.now(timezone.utc).isoformat()
            local_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 1. JSON Lines untuk pembacaan mesin & rekap laporan
            jsonl_path = log_dir / 'events.jsonl'
            with open(jsonl_path, 'a', encoding='utf-8') as stream:
                stream.write(json.dumps({'time': iso_time, 'operation': operation, 'success': bool(success), 'detail': str(detail)}, ensure_ascii=False) + '\n')

            # 2. Activity log teks terbaca manusia (Human-readable)
            activity_path = log_dir / 'activity.log'
            status = 'SUCCESS' if success else 'FAILED'
            with open(activity_path, 'a', encoding='utf-8') as stream:
                stream.write(f"[{local_time}] [{status:<7}] [{operation.upper():<16}] {detail}\n")

    def report(self):
        from .reports import write_report
        with self.lock:
            rows = self.records()
            self._export()
            res = write_report(self.root, rows)
            self.event('report', True, f"records: {res.get('records', 0)}")
            return res

    def detect_dominant_topic(self):
        rows = self.records()
        if not rows:
            return None
        categories = [r.get('category') for r in rows if r.get('category') and r.get('category') != 'umum']
        if categories:
            counts = Counter(categories)
            return counts.most_common(1)[0][0]
        titles = ' '.join(str(r.get('title','')) for r in rows)
        words = re.findall(r'[a-zA-Z]{4,}', titles.lower())
        stopwords = {'the', 'and', 'from', 'with', 'untuk', 'pada', 'yang', 'oleh', 'halaman', 'artikel'}
        keywords = [w for w in words if w not in stopwords]
        if keywords:
            return Counter(keywords).most_common(1)[0][0]
        return None

    def package_record_zip(self, record):
        destination = self.root / 'backups'
        destination.mkdir(exist_ok=True)
        rec_id = str(record.get('id', 'materi'))
        cat = slug(record.get('category', 'umum'))
        saved_at = record.get('saved_at', datetime.now(timezone.utc).isoformat())
        date_str = saved_at[:10] if len(saved_at) >= 10 else datetime.now().strftime('%Y-%m-%d')

        proc_md = self.root / 'processed' / cat / date_str / f'{rec_id}.md'
        proc_json = self.root / 'processed' / cat / date_str / f'{rec_id}.json'
        raw_json = self.root / 'raw' / cat / date_str / f'{rec_id}.json'

        zip_name = f'riset_{rec_id}.zip'
        path = destination / zip_name
        hashes = {}

        summary_text = (
            f"# 📑 Ringkasan Riset: {record.get('title', 'Materi Riset')}\n\n"
            f"- **Kategori / Topik**: {cat}\n"
            f"- **Sumber URL**: {record.get('url', '-')}\n"
            f"- **Waktu Penyimpanan**: {saved_at}\n"
            f"- **Jumlah Kata**: {record.get('word_count', 0)} kata\n"
            f"- **Penulis**: {', '.join(record.get('authors', [])) if isinstance(record.get('authors'), list) else (record.get('authors') or 'Tidak tercantum')}\n"
            f"- **Penerbit**: {record.get('journal') or record.get('hostname') or 'Web Portal'}\n\n"
            f"---\n\n"
            f"### 🎯 Intisari / Abstrak\n\n"
            f"{record.get('abstract') or record.get('description') or 'Tidak ada abstrak tambahan.'}\n\n"
            f"---\n\n"
            f"### 📖 Isi Riset Pokok\n\n"
            f"{record.get('content', '')}\n"
        )

        with ZipFile(path.with_suffix('.tmp'), 'w', ZIP_DEFLATED) as archive:
            summary_bytes = summary_text.encode('utf-8')
            archive.writestr('RINGKASAN_RISET.md', summary_bytes)
            hashes['RINGKASAN_RISET.md'] = hashlib.sha256(summary_bytes).hexdigest()

            if proc_md.exists():
                md_bytes = proc_md.read_bytes()
                archive.writestr('artikel_bersih.md', md_bytes)
                hashes['artikel_bersih.md'] = hashlib.sha256(md_bytes).hexdigest()
                rel_md = f'processed/{cat}/{date_str}/{rec_id}.md'
                archive.writestr(rel_md, md_bytes)
                hashes[rel_md] = hashlib.sha256(md_bytes).hexdigest()

            if proc_json.exists():
                json_bytes = proc_json.read_bytes()
                archive.writestr('data_materi.json', json_bytes)
                hashes['data_materi.json'] = hashlib.sha256(json_bytes).hexdigest()
                rel_json = f'processed/{cat}/{date_str}/{rec_id}.json'
                archive.writestr(rel_json, json_bytes)
                hashes[rel_json] = hashlib.sha256(json_bytes).hexdigest()

            if raw_json.exists():
                raw_bytes = raw_json.read_bytes()
                archive.writestr('sumber_mentah.json', raw_bytes)
                hashes['sumber_mentah.json'] = hashlib.sha256(raw_bytes).hexdigest()
                rel_raw = f'raw/{cat}/{date_str}/{rec_id}.json'
                archive.writestr(rel_raw, raw_bytes)
                hashes[rel_raw] = hashlib.sha256(raw_bytes).hexdigest()

            archive.writestr('MANIFEST.json', json_text({'algorithm': 'sha256', 'files': hashes}))

        os.replace(path.with_suffix('.tmp'), path)
        res = {'path': str(path), 'filename': zip_name, 'title': record.get('title'), 'id': rec_id, 'files': len(hashes)}
        self.event('backup_riset', True, f"{zip_name} ({record.get('title')})")
        return res

    def backup(self, tag=None, category=None, record_id=None):
        with self.lock:
            if record_id:
                record = self.read(record_id)
                return self.package_record_zip(record)

            self._export()
            destination = self.root / 'backups'
            destination.mkdir(exist_ok=True)

            rows = self.records()
            all_categories = sorted(set(r.get('category') for r in rows if r.get('category')))

            target_category = None
            is_full = False

            if category:
                target_category = slug(category)
            elif tag:
                tag_str = str(tag).strip().lower()
                if tag_str in ('all', 'semua', 'full', 'gabungan', 'lengkap'):
                    is_full = True
                else:
                    try:
                        rec = self.read(tag)
                        return self.package_record_zip(rec)
                    except ValueError:
                        pass
                    matched_cat = next((c for c in all_categories if slug(tag) == c or slug(tag) in c), None)
                    target_category = matched_cat or slug(tag)
            elif not is_full:
                if all_categories:
                    dom = self.detect_dominant_topic()
                    target_category = slug(dom) if dom else all_categories[0]

            if target_category and not is_full:
                prefix = f'topik_{target_category}'
                topic_label = target_category
            elif is_full:
                prefix = 'scrapmcp_semua_dataset'
                topic_label = 'semua'
            else:
                prefix = 'scrapmcp'
                topic_label = 'umum'

            path = destination / (datetime.now(timezone.utc).strftime(f'{prefix}_%Y%m%d_%H%M%S_%f')+'.zip')
            hashes = {}
            with ZipFile(path.with_suffix('.tmp'), 'w', ZIP_DEFLATED) as archive:
                for folder in ('raw', 'processed'):
                    folder_path = self.root / folder
                    if target_category and not is_full:
                        target_dir = folder_path / target_category
                        scan_paths = sorted(target_dir.rglob('*')) if target_dir.exists() else []
                    else:
                        scan_paths = sorted(folder_path.rglob('*')) if folder_path.exists() else []

                    for source in scan_paths:
                        if source.is_file() and not source.is_symlink() and self.root in source.resolve().parents and source.suffix != '.tmp':
                            rel = source.relative_to(self.root).as_posix()
                            data = source.read_bytes()
                            hashes[rel] = hashlib.sha256(data).hexdigest()
                            archive.writestr(rel, data)

                for folder in ('exports', 'reports', 'logs'):
                    folder_path = self.root / folder
                    if folder_path.exists():
                        for source in sorted(folder_path.rglob('*')):
                            if source.is_file() and not source.is_symlink() and self.root in source.resolve().parents and source.suffix != '.tmp':
                                rel = source.relative_to(self.root).as_posix()
                                data = source.read_bytes()
                                hashes[rel] = hashlib.sha256(data).hexdigest()
                                archive.writestr(rel, data)

                archive.writestr('MANIFEST.json', json_text({'algorithm':'sha256','files':hashes}))
            os.replace(path.with_suffix('.tmp'), path)
            res = {'path':str(path), 'files':len(hashes), 'topic':topic_label}
            self.event('backup', True, f"{path.name} ({len(hashes)} files, topik: {topic_label})")
            return res
