import csv
import hashlib
import io
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from zipfile import ZipFile
import pytest
from scrapmcp.engine import Engine, clean_record
from scrapmcp.storage import Store, slug
from scrapmcp.service import Service
from scrapmcp.cli import main


def test_full_pipeline(tmp_path):
    service = Service(tmp_path)
    output = service.demo()
    row = output['record']
    assert row['dataset_kind'] == 'simulation'
    assert row['word_count'] > 40
    assert 'pustaka@example.org' in row['emails']
    assert 'MENU BERANDA LOGIN' not in row['content']
    assert 'IKLAN FOOTER' not in row['content']
    assert 'Dasar Python' in row['content']
    assert list(tmp_path.glob('raw/*/*/*.json'))
    assert list(tmp_path.glob('processed/*/*/*.md'))
    with open(tmp_path/'exports/dataset.csv',encoding='utf-8-sig') as stream:
        assert len(list(csv.DictReader(stream))) == 1
    assert Path(output['report']['pdf']).read_bytes().startswith(b'%PDF')
    with ZipFile(output['backup']['path']) as z:
        assert z.testzip() is None
        manifest = json.loads(z.read('MANIFEST.json'))
        for name,digest in manifest['files'].items():
            assert hashlib.sha256(z.read(name)).hexdigest() == digest
        assert not any('backups/' in name or '.env' in name for name in z.namelist())


def test_duplicates_and_concurrent_writes(tmp_path):
    raw = Engine().demo()
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda _: Store(tmp_path).save(raw, '../CON'),range(8)))
    rows = Store(tmp_path).records()
    assert len(rows) == 1
    assert rows[0]['category'] == 'category-con'
    assert Store(tmp_path).save(raw,'../CON')['duplicate']


def test_failure_is_logged_without_record(tmp_path,monkeypatch):
    service = Service(tmp_path)
    def fail(url): raise ValueError('blocked')
    monkeypatch.setattr(service.engine,'scrape',fail)
    with pytest.raises(ValueError): service.scrape('https://example.org')
    assert service.store.records() == []
    assert json.loads((tmp_path/'logs/events.jsonl').read_text())['success'] is False


def test_regex_and_csv_formula(tmp_path):
    row = {'title':'=SUM(A1:A2)','url':'https://example.org','content':'Hello    world\n\n\nemail: test@example.org', 'doi':'10.1234/abcd'}
    result = Store(tmp_path).save(row)
    assert result['doi_valid']
    assert 'Hello world' in result['content']
    assert "'=SUM" in (tmp_path/'exports/dataset.csv').read_text()


def test_cli(tmp_path,capsys):
    assert main(['--data-dir',str(tmp_path),'demo']) == 0
    assert main(['--data-dir',str(tmp_path),'list']) == 0
    assert 'Otomatisasi' in capsys.readouterr().out
    assert main(['--data-dir',str(tmp_path),'read','missing']) == 1


def test_empty_report_and_export(tmp_path):
    store=Store(tmp_path)
    assert store.report()['records'] == 0
    assert store.export()['records'] == 0


def test_zip_excludes_external_symlinks(tmp_path):
    store=Store(tmp_path/'data')
    secret=tmp_path/'secret.txt'; secret.write_text('DO_NOT_BACKUP')
    dest=store.root/'raw'; dest.mkdir()
    try: (dest/'link').symlink_to(secret)
    except OSError: pytest.skip('OS cannot create symlink')
    with ZipFile(store.backup()['path']) as z:
        assert 'raw/link' not in z.namelist()


def test_content_slug_naming(tmp_path):
    store = Store(tmp_path)
    sample = {
        'title': 'Rekomendasi 5 TWS Murah Terbaik dengan ANC 2026 - PortalGadget.id',
        'url': 'https://example.com/tws-review',
        'content': 'Ini adalah ringkasan ulasan TWS murah terbaik dengan fitur noise cancellation aktif.'
    }
    saved = store.save(sample, 'tws-review')
    assert 'rekomendasi-5-tws-murah-terbaik-dengan-anc' in saved['id']
    files_md = list(tmp_path.glob('processed/tws-review/*/*.md'))
    assert len(files_md) == 1
    assert 'rekomendasi-5-tws-murah-terbaik' in files_md[0].name
    
    # Read by full id
    read_full = store.read(saved['id'])
    assert read_full['title'] == sample['title']
    
    # Read by short hash or slug substring
    short_hash = saved['id'].split('_')[-1]
    read_short = store.read(short_hash)
    assert read_short['id'] == saved['id']
    
    # Verify backup archive contains the readable slug filename
    backup = store.backup()
    with ZipFile(backup['path']) as z:
        matching_names = [n for n in z.namelist() if 'rekomendasi-5-tws-murah-terbaik' in n]
        assert len(matching_names) >= 2  # raw json and processed md/json


def test_focused_research_zip_and_topic_backup(tmp_path):
    store = Store(tmp_path)
    r1 = {
        'title': 'Ulasan Lengkap Soundcore TWS R50i',
        'url': 'https://example.com/soundcore-r50i',
        'content': 'Soundcore R50i adalah TWS terjangkau dengan bass mantap dan baterai awet.'
    }
    r2 = {
        'title': 'Pengenalan Python Decorator',
        'url': 'https://example.com/python-decorator',
        'content': 'Decorator di Python memungkinkan modifikasi fungsi secara deklaratif.'
    }
    saved1 = store.save(r1, 'tws-review')
    saved2 = store.save(r2, 'informatika')

    # Each save produces its own dedicated research ZIP
    assert 'zip_backup' in saved1
    assert 'zip_backup' in saved2
    zip1 = Path(saved1['zip_backup'])
    zip2 = Path(saved2['zip_backup'])
    assert zip1.exists()
    assert zip2.exists()
    assert zip1.name != zip2.name

    # Check zip1 contains ONLY research 1 materials (no mixing with Python decorator)
    with ZipFile(zip1) as z1:
        names = z1.namelist()
        assert 'RINGKASAN_RISET.md' in names
        assert 'artikel_bersih.md' in names
        assert 'MANIFEST.json' in names
        assert any('soundcore' in n for n in names)
        assert not any('decorator' in n for n in names)

    # Check topic backup for tws-review does NOT mix with informatika
    topic_bak = store.backup(category='tws-review')
    with ZipFile(topic_bak['path']) as zt:
        names = zt.namelist()
        assert any('soundcore' in n for n in names)
        assert not any('decorator' in n for n in names)
