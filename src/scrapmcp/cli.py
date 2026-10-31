"""Ch.12: argparse automation plus beginner-friendly terminal menu."""
import argparse
import asyncio
import getpass
import json
import os
import re
import sys
from pathlib import Path
from . import __version__
from .service import Service

def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))

def show_record(row):
    emit({k:row.get(k) for k in ('id','title','url','category','word_count','duplicate')})

def mask_endpoint(url):
    try:
        return re.sub(r'(token=.{4})[^&]+', r'\1***', str(url))
    except Exception:
        return 'wss://...***'

def endpoint_prompt(root=None):
    if root:
        ef = Path(root) / '.mcp_endpoint'
        if ef.exists():
            return ef.read_text(encoding='utf-8').strip()
    endpoint = os.getenv('SCRAPMCP_MCP_ENDPOINT')
    if endpoint:
        return endpoint
    if not sys.stdin.isatty():
        raise ValueError('Mode noninteraktif: set SCRAPMCP_MCP_ENDPOINT, atau gunakan mcp --stdio.')
    print('Tempel endpoint MCP lengkap wss://... (input disembunyikan).')
    return getpass.getpass('Endpoint: ').strip()

def handle_mcp_menu(service):
    endpoint_file = service.store.root / '.mcp_endpoint'
    saved = None
    if endpoint_file.exists():
        try:
            saved = endpoint_file.read_text(encoding='utf-8').strip()
        except Exception:
            saved = None
    if not saved:
        saved = os.getenv('SCRAPMCP_MCP_ENDPOINT')

    chosen_endpoint = None
    if saved:
        masked = mask_endpoint(saved)
        print(f"\n[MCP Xiaozhi] Ditemukan endpoint tersimpan:")
        print(f"  Endpoint: {masked}")
        print("  1. Lanjutkan koneksi dengan endpoint ini")
        print("  2. Ganti / Hapus endpoint tersimpan")
        print("  0. Kembali ke menu utama")
        sub_choice = input("Pilih [0-2]: ").strip()
        if sub_choice == '1':
            chosen_endpoint = saved
        elif sub_choice == '2':
            if endpoint_file.exists():
                endpoint_file.unlink(missing_ok=True)
            print("Endpoint tersimpan telah dihapus.")
            print("Tempel endpoint WebSocket MCP Xiaozhi yang baru (wss://.../mcp/?token=...):")
            new_ep = getpass.getpass('Endpoint baru: ').strip()
            if not new_ep:
                print("Dibatalkan. Kembali ke menu.")
                return
            from .mcp_server import validate_endpoint
            new_ep = validate_endpoint(new_ep)
            endpoint_file.write_text(new_ep, encoding='utf-8')
            try:
                os.chmod(endpoint_file, 0o600)
            except Exception:
                pass
            chosen_endpoint = new_ep
        else:
            return
    else:
        print("\nBelum ada endpoint MCP tersimpan.")
        print("Tempel endpoint WebSocket MCP Xiaozhi (wss://.../mcp/?token=...):")
        ep = getpass.getpass('Endpoint: ').strip()
        if not ep:
            print("Dibatalkan. Kembali ke menu.")
            return
        from .mcp_server import validate_endpoint
        ep = validate_endpoint(ep)
        endpoint_file.write_text(ep, encoding='utf-8')
        try:
            os.chmod(endpoint_file, 0o600)
        except Exception:
            pass
        chosen_endpoint = ep

    print("\n" + "="*60)
    print("🚀 MEMULAI BRIDGE MCP XIAOZHI")
    print("="*60)
    print("Status : Menghubungkan ke server Xiaozhi...")
    print("Fitur  : Log proses scraping sampai pembuatan ZIP aktif.")
    print("Kontrol: Tekan Ctrl+C kapan saja untuk berhenti & kembali ke menu.")
    print("="*60 + "\n", flush=True)

    try:
        from .mcp_server import run_bridge
        asyncio.run(run_bridge(chosen_endpoint, service))
    except KeyboardInterrupt:
        print('\nMCP dihentikan. Kembali ke menu.')

def menu(service):
    while True:
        print('\nSCRAPMCP | Scraping & Arsip Materi\n'
              '1. Scrap manual (URL HTML/PDF/YouTube)\n'
              '2. Hubungkan MCP Xiaozhi\n'
              '3. Riset topik / jurnal\n'
              '4. Daftar & baca materi\n'
              '5. Ekspor JSON / CSV\n'
              '6. Buat laporan PDF\n'
              '7. Backup ZIP\n'
              '8. Demo offline lengkap\n'
              '9. Lihat folder data\n'
              '0. Keluar')
        try:
            choice = input('Pilih [0-9]: ').strip()
            if choice == '0':
                return
            if choice == '1':
                url = input('URL: ').strip()
                cat_input = input('Kategori (Enter untuk otomatis dari algoritma): ').strip()
                show_record(service.scrape(url, cat_input or None))
            elif choice == '2':
                handle_mcp_menu(service)
            elif choice == '3':
                result = service.research(input('Topik: ').strip())
                print(result.get('summary',''))
                if input('Simpan hasil ini? [y/N]: ').strip().lower() == 'y':
                    payload = result['materi_siap_simpan']
                    show_record(service.store.save(payload,payload.get('category','riset')))
            elif choice == '4':
                rows = service.store.records()
                for row in rows:
                    print(f"{row['id']} | {row['title']} | {row['category']}")
                key = input('ID untuk dibaca (Enter kembali): ').strip()
                if key:
                    print(service.store.read(key)['content'])
            elif choice == '5': emit(service.store.export())
            elif choice == '6': emit(service.store.report())
            elif choice == '7':
                rows = service.store.records()
                all_cats = sorted(set(r.get('category','umum') for r in rows if r.get('category')))
                print('\nPilihan Backup ZIP:')
                print('1. Backup terfokus pada topik/kategori tertentu (Rekomendasi agar tidak campur)')
                print('2. Backup materi riset tertentu berdasarkan ID')
                print('3. Backup seluruh dataset (Gabungan semua topik)')
                sub_c = input('Pilih opsi [1/2/3, default 1]: ').strip() or '1'
                if sub_c == '2':
                    rec_key = input('ID atau judul materi: ').strip()
                    res = service.store.backup(record_id=rec_key)
                elif sub_c == '3':
                    res = service.store.backup(tag='all')
                else:
                    if all_cats:
                        print(f"Topik/kategori tersedia: {', '.join(all_cats)}")
                        cat_chosen = input('Pilih kategori (Enter untuk topik dominan otomatis): ').strip()
                        res = service.store.backup(category=cat_chosen or None)
                    else:
                        res = service.store.backup()
                print(f"Backup ZIP berhasil dibuat: {res.get('path')}")
                emit(res)
            elif choice == '8':
                result = service.demo()
                show_record(result['record'])
                emit({'report':result['report'], 'backup':result['backup']})
            elif choice == '9': print(service.store.root)
            else: print('Pilihan tidak dikenal.')
        except EOFError:
            return
        except (ValueError,OSError) as exc:
            print(f'Gagal: {exc}',file=sys.stderr)

def parser():
    p = argparse.ArgumentParser(prog='scrapmcp',description='Scraping manual dan MCP Xiaozhi. Tanpa subperintah: menu interaktif.')
    p.add_argument('--version',action='version',version=__version__)
    p.add_argument('--data-dir',default=os.getenv('SCRAPMCP_DATA_DIR',str(Path.home()/'scrapmcp-data')),help='Folder data (default: ~/scrapmcp-data); letakkan sebelum subperintah.')
    p.add_argument('--allow-jina',action='store_true',help='Aktifkan fallback Jina Reader; URL sumber akan dikirim ke r.jina.ai.')
    sub = p.add_subparsers(dest='command')
    s = sub.add_parser('scrape',help='Ambil URL dan simpan hasil')
    s.add_argument('url'); s.add_argument('--category',default=None,help='Kategori materi (default: deteksi otomatis)')
    b = sub.add_parser('batch',help='Ambil URL dari file teks, satu URL per baris')
    b.add_argument('file',type=Path); b.add_argument('--category',default=None)
    r = sub.add_parser('research',help='Riset topik; default pratinjau')
    r.add_argument('topic'); r.add_argument('--mode',choices=['auto','web','academic'],default='auto'); r.add_argument('--save',action='store_true')
    a = sub.add_parser('academic',help='Cari jurnal'); a.add_argument('query'); a.add_argument('--limit',type=int,default=5)
    bak = sub.add_parser('backup',help='Buat ZIP dataset lokal')
    bak.add_argument('--tag',default=None,help='Tag/topik nama ZIP (default: deteksi otomatis)')
    bak.add_argument('--category',default=None,help='Fokus backup pada kategori/topik tertentu')
    bak.add_argument('--record',default=None,help='Fokus backup pada satu materi ID riset')
    for name in ('list','export','report','demo','doctor'):
        sub.add_parser(name)
    read = sub.add_parser('read'); read.add_argument('id')
    m = sub.add_parser('mcp',help='Hubungkan endpoint Xiaozhi (prompt/env), atau MCP stdio')
    m.add_argument('--stdio',action='store_true'); m.add_argument('--once',action='store_true')
    return p

def main(argv=None):
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):
            stream.reconfigure(encoding='utf-8',errors='replace')
    args = parser().parse_args(argv)
    try:
        service = Service(args.data_dir,args.allow_jina)
        if args.command is None:
            menu(service)
        elif args.command == 'scrape': show_record(service.scrape(args.url,args.category))
        elif args.command == 'batch':
            import time
            errors = 0
            urls = [l.strip() for l in args.file.read_text(encoding='utf-8-sig').splitlines() if l.strip() and not l.lstrip().startswith('#')]
            for index,url in enumerate(urls):
                if index: time.sleep(1)
                try: show_record(service.scrape(url,args.category))
                except Exception as exc:
                    errors += 1
                    emit({'url':url,'error':str(exc)})
            emit({'total':len(urls),'failed':errors})
            return 1 if errors else 0
        elif args.command == 'research': emit(service.research(args.topic,args.mode,args.save))
        elif args.command == 'academic': emit(service.engine.academic(args.query,args.limit))
        elif args.command == 'list':
            emit([{k:r.get(k) for k in ('id','title','category','url')} for r in service.store.records()])
        elif args.command == 'read': emit(service.store.read(args.id))
        elif args.command == 'export': emit(service.store.export())
        elif args.command == 'report': emit(service.store.report())
        elif args.command == 'backup': emit(service.store.backup(tag=getattr(args, 'tag', None), category=getattr(args, 'category', None), record_id=getattr(args, 'record', None)))
        elif args.command == 'demo':
            result = service.demo()
            show_record(result['record']); emit({'report':result['report'],'backup':result['backup']})
        elif args.command == 'doctor':
            import importlib.metadata as meta
            emit({'python':sys.version.split()[0], 'data_dir':str(service.store.root), 'dependencies':{k:meta.version(k) for k in ('requests','beautifulsoup4','mcp','websockets','pypdf','youtube-transcript-api','reportlab')},'endpoint_in_environment':bool(os.getenv('SCRAPMCP_MCP_ENDPOINT'))})
        elif args.command == 'mcp':
            from .mcp_server import run_bridge, run_stdio
            asyncio.run(run_stdio(service) if args.stdio else run_bridge(endpoint_prompt(args.data_dir),service,args.once))
        return 0
    except KeyboardInterrupt:
        print('\nDihentikan.',file=sys.stderr)
        return 130
    except (ValueError,OSError) as exc:
        print(f'Gagal: {exc}',file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
