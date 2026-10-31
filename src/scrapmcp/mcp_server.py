"""Official MCP SDK over Xiaozhi's outbound JSON-RPC WebSocket bridge."""
import asyncio
import json
import logging
from pathlib import Path
import sys
import uuid
from contextlib import asynccontextmanager
from urllib.parse import urlsplit
import anyio
from mcp import types
from mcp.server.lowlevel import Server
from mcp.shared.message import SessionMessage
from mcp.server.stdio import stdio_server
from websockets.asyncio.client import connect

# Never log a WebSocket URL: it contains the account token.
logging.getLogger('websockets').setLevel(logging.CRITICAL)

def validate_endpoint(url):
    p = urlsplit(url.strip())
    if p.scheme != 'wss' or not p.hostname or p.username or p.password:
        raise ValueError('Masukkan endpoint MCP wss://... yang disalin dari Xiaozhi, bukan token saja.')
    if '/console' in p.path:
        raise ValueError('Ini URL dashboard. Gunakan endpoint WebSocket MCP Xiaozhi.')
    return url.strip()

def make_server(service):
    server = Server(
        'scrapmcp',
        version='1.0.0',
        instructions=(
            'ScrapMCP adalah aplikasi Web Scraping berbasis Python BeautifulSoup dan Requests untuk tugas kuliah otomatisasi. '
            'Tugas utama Anda adalah mencari halaman website/artikel berita HTML di internet, mengekstrak isi teks bersih menggunakan BeautifulSoup, '
            'membersihkan teks dari sampah/iklan dengan Regex (Bab 9), menyimpan rapi ke database lokal (Bab 10), membuat laporan PDF, dan backup arsip ZIP (Bab 11). '
            'JANGAN mencari video atau lagu YouTube! Prioritaskan mencari dan men-scrape artikel halaman website HTML di internet menggunakan tool search_web dan scrape_and_save_to_knowledge.'
        )
    )
    pending = {}
    def tool(name, description, properties=None, required=None):
        return types.Tool(name=name, description=description, inputSchema={'type':'object','properties':properties or {},'required':required or [],'additionalProperties':False})
    string = {'type':'string','minLength':1,'maxLength':2000}
    specs = [
        tool('search_web','Pencarian halaman website & artikel berita di internet. Menemukan link artikel web HTML terverifikasi untuk di-scrape menggunakan BeautifulSoup. Gunakan saat user meminta mencari berita atau mencari materi di internet.',{'query':string,'max_results':{'type':'integer','minimum':1,'maximum':10}},['query']),
        tool('search_news','Pencarian berita online aktual di portal berita Indonesia & internasional secara real-time untuk diekstrak teksnya dengan BeautifulSoup.',{'query':string,'max_results':{'type':'integer','minimum':1,'maximum':10}},['query']),
        tool('search_web_deep','Pencarian website internet mendalam: mengumpulkan link halaman web berita/ensiklopedia dan membaca teks paragraf utama dengan BeautifulSoup.',{'query':string,'max_results':{'type':'integer','minimum':1,'maximum':10}},['query']),
        tool('scrape_and_save_to_knowledge','Buka URL website di internet, ekstrak isi artikel menggunakan BeautifulSoup dan Requests, bersihkan dengan Regex, dan simpan ke database lokal.',{'url':string,'title':{'type':'string','maxLength':160},'category':{'type':'string','maxLength':80}},['url']),
        tool('scrape_webpage','Scrape halaman website HTML di internet menggunakan BeautifulSoup: ambil judul, paragraf teks, heading, dan tabel data lalu simpan secara lokal.',{'url':string,'category':{'type':'string','maxLength':80}},['url']),
        tool('search_academic_papers','Cari jurnal ilmiah arXiv, Semantic Scholar, CrossRef di internet. Tidak menyimpan otomatis.',{'query':string,'max_results':{'type':'integer','minimum':1,'maximum':10}},['query']),
        tool('autonomous_deep_research','Autonomous Deep Research: XiaoZhi secara mandiri menelusuri website di internet menggunakan BeautifulSoup, merangkum isi materi dan kuis pemahaman tanpa input URL manual.',{'topic_or_question':string,'mode':{'type':'string','enum':['auto','web','academic']}},['topic_or_question']),
        tool('research_topic','Riset topik materi web/jurnal di internet menggunakan scraper BeautifulSoup. Pratinjau intisari teks sebelum disimpan.',{'topic':string,'mode':{'type':'string','enum':['auto','web','academic']}},['topic']),
        tool('confirm_and_save_research_material','Simpan materi hasil riset web ke database lokal setelah pengguna memberikan konfirmasi.',{'candidate_id':{'type':'string'},'title':{'type':'string'},'content':{'type':'string'},'url':{'type':'string'},'category':{'type':'string'}}),
        tool('list_materials','Daftar materi website yang sudah berhasil di-scrape dan tersimpan di komputer lokal.'),
        tool('search_course_materials','Cari materi pembelajaran yang tersimpan di database lokal.',{'search_keyword':string}),
        tool('read_material_database','Baca ringkasan database materi lokal.',{'search_keyword':{'type':'string'},'category':{'type':'string'},'limit':{'type':'integer'}}),
        tool('read_material_detail','Baca detail teks isi materi website berdasarkan ID.',{'record_id':string,'material_id':string}),
        tool('create_report','Buat laporan rekap dataset hasil scraping dalam format PDF, Markdown, dan JSON.'),
        tool('backup_dataset','Buat arsip backup ZIP hasil scraping dataset (bisa fokus per topik atau ID riset tertentu agar tidak tercampur materi lain), lengkap dengan manifest SHA-256.',{'tag':{'type':'string','maxLength':50},'category':{'type':'string','maxLength':50},'record_id':{'type':'string','maxLength':80}}),
    ]
    @server.list_tools()
    async def list_tools():
        service.store.event('mcp_connect', True, f'Xiaozhi terhubung & memuat {len(specs)} tools')
        print(f"\n[MCP LIVE] 🤝 Xiaozhi terhubung & memuat {len(specs)} tools otomatis. Siap menerima perintah!", file=sys.stderr, flush=True)
        return specs

    @server.call_tool()
    async def call_tool(name, arguments):
        def log(msg):
            print(msg, file=sys.stderr, flush=True)

        try:
            if name in ('search_web', 'search_web_deep', 'search_web_sources', 'search_news'):
                query = arguments.get('query', '')
                limit = arguments.get('max_results') or arguments.get('limit') or 5
                log(f"\n[MCP LIVE] 🔍 Xiaozhi mencari di internet ({name}): \"{query}\"")
                value = await asyncio.to_thread(service.engine.search_web, query, limit, True)
                results_list = value.get('results', [])
                log(f"  └─ ✅ Ditemukan {len(results_list)} sumber informasi/berita.")
                for idx, s in enumerate(results_list[:3], 1):
                    log(f"     [{idx}] {s.get('title')} ({s.get('source')})")
                service.store.event('mcp_search_web', True, f"tool: {name} | query: {query} | {len(results_list)} hasil")
            elif name in ('scrape_webpage', 'scrape_and_save_to_knowledge'):
                url = arguments.get('url', '')
                cat = arguments.get('category')
                title_hint = arguments.get('title')
                log(f"\n[MCP LIVE] 📥 Xiaozhi memanggil: {name}")
                log(f"  ├─ 🌐 Target URL   : {url}")
                log(f"  ├─ ⏳ Mengunduh & mem-parsing konten halaman dengan BeautifulSoup...")
                value = await asyncio.to_thread(service.scrape, url, cat)
                if title_hint and not value.get('title'):
                    value['title'] = title_hint
                value['success'] = True
                zip_file = Path(value.get('zip_backup', '')).name
                value['message'] = (
                    f"Sukses! Artikel '{value.get('title')}' berhasil di-scrape dan disimpan ke database lokal "
                    f"(Kategori: {value.get('category')}, Jumlah kata: {value.get('word_count')}). "
                    f"Arsip ZIP khusus hasil riset ini otomatis dibuat: '{zip_file}'."
                )
                log(f"  ├─ 🧹 Pembersihan teks & normalisasi regex (Ch. 9)...")
                log(f"  ├─ 📁 Kategori     : {value.get('category')}")
                log(f"  ├─ 📝 Jumlah Kata  : {value.get('word_count')} kata")
                log(f"  ├─ 💾 Berkas Teks  : {value.get('id')}.md")
                log(f"  ├─ 📦 Arsip ZIP    : {zip_file} (Fokus riset ini)")
                log(f"  └─ ✅ Sukses disimpan: \"{value.get('title')}\"")
                service.store.event('mcp_scrape', True, f"id: {value.get('id')} | title: {value.get('title')}")
            elif name == 'search_academic_papers':
                query = arguments.get('query', '')
                limit = arguments.get('max_results') or arguments.get('limit') or 5
                log(f"\n[MCP LIVE] 🎓 Xiaozhi mencari jurnal akademik: \"{query}\"")
                value = await asyncio.to_thread(service.engine.academic, query, limit)
                papers = value.get('papers', [])
                log(f"  └─ ✅ Ditemukan {len(papers)} paper akademik.")
                service.store.event('mcp_academic', True, f"query: {query} | {len(papers)} papers")
            elif name in ('research_topic', 'autonomous_deep_research'):
                topic = arguments.get('topic') or arguments.get('topic_or_question') or ''
                mode = arguments.get('mode', 'auto')
                log(f"\n[MCP LIVE] 🧠 Xiaozhi meriset topik: \"{topic}\" (mode: {mode})")
                log(f"  ├─ ⏳ Menelusuri sumber & membuat kuis pemahaman...")
                value = await asyncio.to_thread(service.research, topic, mode)
                if len(pending) >= 20:
                    pending.pop(next(iter(pending)))
                key = uuid.uuid4().hex
                pending[key] = value.pop('materi_siap_simpan')
                value.pop('instruksi_ai',None)
                value['candidate_id'] = key
                log(f"  └─ ✅ Pratinjau riset selesai. Menunggu konfirmasi simpan pengguna.")
                service.store.event('mcp_research', True, f"topic: {topic} | mode: {mode}")
            elif name == 'confirm_and_save_research_material':
                key = arguments.get('candidate_id')
                if key and key in pending:
                    payload = pending.pop(key)
                elif arguments.get('title') or arguments.get('content'):
                    payload = {
                        'title': arguments.get('title', 'Materi Riset Mandiri'),
                        'content': arguments.get('content', ''),
                        'url': arguments.get('url', 'autonomous_research'),
                        'category': arguments.get('category', 'riset')
                    }
                else:
                    raise ValueError('Kandidat tidak ditemukan/expired setelah koneksi dimulai ulang.')
                log(f"\n[MCP LIVE] 💾 Xiaozhi menyimpan materi riset: \"{payload.get('title')}\"")
                value = await asyncio.to_thread(service.store.save, payload, payload.get('category','riset'))
                value['success'] = True
                zip_file = Path(value.get('zip_backup', '')).name
                value['message'] = (
                    f"Sukses! Materi riset '{payload.get('title')}' berhasil disimpan (Berkas: {value.get('id')}). "
                    f"Arsip ZIP khusus hasil riset ini otomatis dibuat: '{zip_file}'."
                )
                log(f"  ├─ 📦 Arsip ZIP    : {zip_file} (Fokus riset ini)")
                log(f"  └─ ✅ Tersimpan ke database lokal (Berkas: {value.get('id')})")
                service.store.event('mcp_save_research', True, f"id: {value.get('id')} | {payload.get('title')}")
            elif name in ('list_materials', 'read_material_database', 'search_course_materials'):
                kw = str(arguments.get('search_keyword') or arguments.get('query') or '').lower()
                cat = str(arguments.get('category') or '').lower()
                limit = int(arguments.get('limit') or 100)
                log(f"\n[MCP LIVE] 📋 Xiaozhi meminta daftar materi ({name})...")
                rows = await asyncio.to_thread(service.store.records)
                if kw:
                    rows = [r for r in rows if kw in r.get('title','').lower() or kw in r.get('content','').lower()]
                if cat:
                    rows = [r for r in rows if cat in r.get('category','').lower()]
                selected = rows[:limit]
                value = {'total':len(selected),'materials':[{k:r.get(k) for k in ('id','title','url','category')} for r in selected]}
                log(f"  └─ ✅ Mengirim {len(selected)} data materi ke Xiaozhi.")
                service.store.event('mcp_list_materials', True, f"tool: {name} | {len(selected)} materi")
            elif name == 'read_material_detail':
                rec_id = str(arguments.get('record_id') or arguments.get('material_id') or '')
                log(f"\n[MCP LIVE] 📖 Xiaozhi membaca materi ID: {rec_id}")
                value = await asyncio.to_thread(service.store.read, rec_id)
                log(f"  └─ ✅ Materi \"{value.get('title')}\" berhasil dikirim ke Xiaozhi.")
                service.store.event('mcp_read_material', True, f"id: {rec_id}")
            elif name == 'create_report':
                log(f"\n[MCP LIVE] 📊 Xiaozhi meminta pembuatan laporan...")
                log(f"  ├─ ⏳ Mengolah ringkasan statistik dataset...")
                value = await asyncio.to_thread(service.store.report)
                value['success'] = True
                value['message'] = (
                    f"Sukses! Laporan dataset berhasil dibuat dalam format PDF ({Path(value.get('pdf','')).name}) "
                    f"dan Markdown ({Path(value.get('markdown','')).name}) dengan total {value.get('records')} materi dan {value.get('words')} kata."
                )
                log(f"  ├─ 📄 Berkas PDF      : {value.get('pdf')}")
                log(f"  ├─ 📝 Berkas Markdown : {value.get('markdown')}")
                log(f"  └─ ✅ Laporan diperbarui ({value.get('records')} materi, {value.get('words')} kata).")
                service.store.event('mcp_create_report', True, f"{value.get('pdf')}")
            elif name == 'backup_dataset':
                tag = arguments.get('tag')
                cat = arguments.get('category')
                rec_id = arguments.get('record_id') or arguments.get('id')
                log(f"\n[MCP LIVE] 📦 Xiaozhi meminta backup dataset ke file ZIP...")
                log(f"  ├─ 🗜️  Mengompres berkas hasil riset...")
                value = await asyncio.to_thread(service.store.backup, tag=tag, category=cat, record_id=rec_id)
                value['success'] = True
                zip_filename = Path(value.get('path','')).name
                value['message'] = (
                    f"Sukses! Berkas arsip ZIP '{zip_filename}' berhasil dibuat khusus untuk hasil riset topik '{value.get('topic') or 'umum'}' "
                    f"(berisi {value.get('files')} file lengkap dengan verifikasi SHA-256 MANIFEST)."
                )
                log(f"  ├─ 🔒 Menghitung verifikasi hash SHA-256 (MANIFEST.json)...")
                log(f"  ├─ 🏷️  Fokus Topik/Riset: {value.get('topic') or 'umum'}")
                log(f"  ├─ 📂 Jumlah Berkas    : {value.get('files')} file")
                log(f"  └─ 🚀 SELESAI! File ZIP: {value.get('path')}")
                service.store.event('mcp_backup_dataset', True, f"{value.get('path')}")
            else:
                raise ValueError('Tool tidak dikenal.')
            return types.CallToolResult(content=[types.TextContent(type='text',text=json.dumps(value,ensure_ascii=False))], isError=bool(isinstance(value,dict) and value.get('success') is False))
        except Exception as exc:
            log(f"  └─ ❌ Error eksekusi tool: {exc}")
            service.store.event(f'mcp_error_{name}', False, str(exc))
            return types.CallToolResult(content=[types.TextContent(type='text',text=json.dumps({'error':str(exc)},ensure_ascii=False))],isError=True)
    return server

@asynccontextmanager
async def websocket_streams(ws):
    incoming_send, incoming_receive = anyio.create_memory_object_stream(16)
    outgoing_send, outgoing_receive = anyio.create_memory_object_stream(16)
    async def reader():
        async with incoming_send:
            try:
                async for raw in ws:
                    try:
                        message = types.JSONRPCMessage.model_validate_json(raw)
                    except Exception:
                        await ws.send(json.dumps({'jsonrpc':'2.0','id':None,'error':{'code':-32700,'message':'Parse error'}}))
                        continue
                    await incoming_send.send(SessionMessage(message))
            except Exception:
                pass
    async def writer():
        async with outgoing_receive:
            async for message in outgoing_receive:
                await ws.send(message.message.model_dump_json(by_alias=True,exclude_none=True))
    async with anyio.create_task_group() as tasks:
        tasks.start_soon(reader)
        tasks.start_soon(writer)
        try:
            yield incoming_receive, outgoing_send
        finally:
            tasks.cancel_scope.cancel()

async def serve_connection(ws, service):
    server = make_server(service)
    async with websocket_streams(ws) as (read, write):
        await server.run(read, write, server.create_initialization_options())

async def run_bridge(endpoint, service, once=False):
    endpoint = validate_endpoint(endpoint)
    delay = 2
    while True:
        try:
            async with connect(endpoint,open_timeout=20,ping_interval=25,ping_timeout=60,close_timeout=5,max_size=2**20,additional_headers={'User-Agent':'ScrapMCP/1.0'}) as ws:
                print('MCP terhubung. Menunggu Xiaozhi memanggil tools. Ctrl+C untuk berhenti.',file=sys.stderr,flush=True)
                delay = 2
                await serve_connection(ws,service)
        except (asyncio.CancelledError, KeyboardInterrupt):
            raise
        except Exception as exc:
            print(f'Koneksi MCP gagal/terputus ({type(exc).__name__}); periksa endpoint, internet, atau sesi lain.',file=sys.stderr)
            if once:
                raise ValueError('Koneksi MCP gagal. Endpoint tidak ditampilkan demi menjaga token.') from None
        if once:
            return
        print(f'Menghubungkan ulang dalam {delay} detik...',file=sys.stderr,flush=True)
        await asyncio.sleep(delay)
        delay = min(delay*2,60)

async def run_stdio(service):
    server = make_server(service)
    async with stdio_server() as (read,write):
        await server.run(read,write,server.create_initialization_options())
