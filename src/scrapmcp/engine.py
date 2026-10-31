"""Reuse the full source scraper; isolate it from the web application."""
import base64
import re
import urllib.parse
from bs4 import BeautifulSoup
from contextvars import ContextVar
from importlib.resources import files
from . import upstream_scraper as upstream
from .network import PublicHTTP, validate_url

_allow_jina = ContextVar('allow_jina', default=False)
_original_jina = upstream.scrape_via_jina_reader
upstream.requests = PublicHTTP
upstream.HAS_REQUESTS = True
upstream.validate_scrape_url = validate_url

def _jina(url, max_chars=25000):
    if _allow_jina.get():
        checked = validate_url(url)
        if checked['valid']:
            return _original_jina(url, max_chars)
    return None

upstream.scrape_via_jina_reader = _jina

def detect_category(raw):
    source_type = raw.get('source_type', '')
    url = str(raw.get('url', '')).lower()
    title = str(raw.get('title', ''))
    content = str(raw.get('content', ''))
    text = f"{title} {raw.get('description', '')} {content[:1500]}".lower()

    if re.search(r'arxiv|doi\.org|journal|jurnal|ieee|research|sciencedirect|scholar|penelitian', url + ' ' + text):
        return 'jurnal-ilmiah'
    if source_type == 'youtube_transcript' or 'youtube.com' in url or 'youtu.be' in url:
        return 'video-edukasi'
    if source_type == 'pdf_document' or url.endswith('.pdf'):
        return 'dokumen-pdf'
    if re.search(r'python|javascript|typescript|golang|rust|coding|pemrograman|software|github|api-docs|tutorial|informatika|komputer|database', text):
        return 'informatika'
    if re.search(r'berita|news|breaking|detik|kompas|tempo|tribun|cnn', url + ' ' + text):
        return 'berita'
    if re.search(r'kampus|universitas|sekolah|kuliah|pendidikan|pustaka|perpustakaan|akademik', text):
        return 'edukasi'
    if re.search(r'kesehatan|medis|penyakit|dokter|farmasi|obat', text):
        return 'kesehatan'
    if re.search(r'ekonomi|bisnis|keuangan|finansial|saham|investasi|perbankan', text):
        return 'ekonomi'

    title_words = re.findall(r'[a-zA-Z]{4,}', title.lower())
    stopwords = {'home', 'index', 'page', 'post', 'article', 'berita', 'website', 'tentang', 'untuk', 'dengan', 'yang'}
    meaningful = [w for w in title_words if w not in stopwords]
    if meaningful:
        return meaningful[0]
    return 'umum'

def clean_search_query(raw_query: str) -> str:
    q = str(raw_query).strip()
    patterns = [
        r'^(tolong|coba|mohon|bisakah|bisa|harap)\s+(carikan|cari|cek|temukan|lihat|tanya|info)\s+(dong|kan|tentang|mengenai)?\s*',
        r'^(apakah\s+kamu\s+tahu|kamu\s+tahu\s+nggak|tau\s+gak|tahu\s+kah)\s+(tentang|mengenai)?\s*',
        r'^(apa\s+itu|siapa\s+itu|di\s+mana|dimana|bagaimana|kapan)\s*',
        r'^(beritahu\s+saya|kasih\s+tahu|jelaskan\s+tentang|info\s+tentang|mencari\s+informasi\s+tentang)\s*',
    ]
    for pattern in patterns:
        q = re.sub(pattern, '', q, flags=re.IGNORECASE).strip()
    q = re.sub(r'[\?\!\.\,]+$', '', q).strip()
    return q if len(q) >= 2 else str(raw_query).strip()

def search_internet_multi(query: str, max_results: int = 5, read_content: bool = True):
    clean_q = clean_search_query(query)
    search_q = clean_q or query
    broad_q = re.sub(r'\bsite:\S+', '', search_q).strip() or search_q
    results = []
    seen_urls = set()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    # 1. Bing News Search: Berita & ulasan teknologi terverifikasi dengan URL asli
    try:
        url_news = f'https://www.bing.com/news/search?q={urllib.parse.quote_plus(broad_q)}'
        r = PublicHTTP.get(url_news, headers=headers, timeout=5)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for c in soup.select('.news-card, .card'):
                a = c.select_one('a.title')
                p = c.select_one('.snippet, .desc')
                src = c.select_one('.source')
                if a:
                    href = a.get('href', '')
                    t = a.get_text(strip=True)
                    s = p.get_text(strip=True) if p else ''
                    source_name = src.get_text(strip=True) if src else 'Portal Berita Terverifikasi'
                    if href and href.startswith('http') and href not in seen_urls:
                        seen_urls.add(href)
                        results.append({'title': t, 'url': href, 'snippet': s, 'source': source_name})
                if len(results) >= max_results:
                    break
    except Exception:
        pass

    # 2. Bing Web Search: E-commerce, review portal, spesifikasi gadget, & situs resmi
    if len(results) < max_results:
        try:
            url_web = f'https://www.bing.com/search?q={urllib.parse.quote_plus(search_q)}'
            r = PublicHTTP.get(url_web, headers=headers, timeout=5)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                for li in soup.select('li.b_algo'):
                    h2 = li.select_one('h2 a')
                    p = li.select_one('.b_caption p')
                    if not h2:
                        continue
                    t = h2.get_text(strip=True)
                    href = h2.get('href', '')
                    real_url = href
                    if 'bing.com/ck/a?' in href and 'u=' in href:
                        qs = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                        u_val = qs.get('u', [''])[0]
                        if u_val.startswith('a1'):
                            raw_b64 = u_val[2:] + '=' * (-len(u_val[2:]) % 4)
                            try:
                                real_url = base64.urlsafe_b64decode(raw_b64).decode('utf-8', errors='ignore')
                            except Exception:
                                pass
                    s = p.get_text(strip=True) if p else ''
                    if real_url and real_url.startswith('http') and real_url not in seen_urls:
                        seen_urls.add(real_url)
                        results.append({'title': t, 'url': real_url, 'snippet': s, 'source': 'Web Terverifikasi'})
                    if len(results) >= max_results * 2:
                        break
        except Exception:
            pass

    # 3. Wikipedia Ensiklopedia (Untuk definisi, konsep akademik, dan sains)
    if len(results) < max_results:
        try:
            wiki_api = f'https://id.wikipedia.org/w/api.php?action=opensearch&search={urllib.parse.quote(broad_q)}&limit={max_results}&namespace=0&format=json'
            resp = PublicHTTP.get(wiki_api, timeout=4)
            if resp.status_code == 200:
                data = resp.json()
                if len(data) >= 4:
                    for t, s, u in zip(data[1], data[2], data[3]):
                        if u not in seen_urls:
                            seen_urls.add(u)
                            results.append({
                                'title': t,
                                'url': u,
                                'snippet': s or f'Artikel ensiklopedia {t}',
                                'source': 'Wikipedia Ensiklopedia'
                            })
                            if len(results) >= max_results:
                                break
        except Exception:
            pass

    # 4. Scoring Relevansi Kata Kunci
    keywords = [w.lower() for w in re.findall(r'[a-zA-Z0-9]{3,}', search_q) if w.lower() not in {'harga', 'ribu', 'rekomendasi', 'terbaik', '2026', 'site'}]
    def score_item(it):
        text = (it.get('title', '') + ' ' + it.get('snippet', '')).lower()
        score = sum(3 for kw in keywords if kw in text)
        if any(w in text for w in ('tws', 'soundcore', 'earphone', 'earbuds', 'headset', 'audio', 'anc')):
            score += 5
        return score

    results.sort(key=score_item, reverse=True)

    # 5. Multi-Page Deep Scraper jika read_content aktif (ekstrak isi dengan BeautifulSoup)
    if read_content and results:
        for item in results[:2]:
            u = item.get('url', '')
            if u and u.startswith('http') and not u.startswith('https://news.google.com'):
                try:
                    scraped = upstream.scrape_url(u, max_length=2500)
                    if scraped.get('success') and scraped.get('content'):
                        item['snippet'] = scraped['content'][:1500]
                        item['is_deep_content'] = True
                        break
                except Exception:
                    pass

    final_results = results[:max_results]
    return {
        'success': bool(final_results),
        'query': query,
        'clean_query': search_q,
        'results': final_results,
        'total_found': len(final_results),
        'instruksi_ai': (
            "PANDUAN MENJAWAB PENGGUNA VIA SUARA/CHAT:\n"
            "1. Jawab secara ringkas, jelas, dan informatif berdasarkan data 'results' di atas (sebutkan nama produk, spesifikasi/fitur, dan kisaran harga).\n"
            "2. Jika pengguna meminta untuk menyimpan atau membuat arsip, panggil tool 'scrape_and_save_to_knowledge' menggunakan URL dari hasil di atas (tool ini otomatis langsung membuatkan arsip ZIP terpisah khusus untuk materi riset tersebut). Jika pengguna ingin mengompres topik terkait, panggil 'backup_dataset' dengan kategori topik agar file ZIP fokus dan tidak tercampur topik lain."
        )
    }

def _search_web_for_upstream(q, max_results=5):
    res = search_internet_multi(q, max_results=max_results, read_content=False)
    return res.get('results', [])

upstream.search_web_sources = _search_web_for_upstream

def clean_record(result):
    record = dict(result)
    content = str(record.get('content', ''))
    content = upstream.clean_indonesian_news_noise(content)
    content = re.sub(r'[ \t]+', ' ', content)
    content = re.sub(r'\n{3,}', '\n\n', content).strip()
    record.update(content=content, word_count=len(content.split()), size_bytes=len(content.encode('utf-8')))
    record['emails'] = sorted(set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', content)))
    doi = str(record.get('doi', '')).removeprefix('https://doi.org/')
    record['doi_valid'] = bool(re.fullmatch(r'10\.\d{4,9}/\S+', doi)) if doi else None
    return record

class Engine:
    def __init__(self, allow_jina=False):
        self.allow_jina = allow_jina

    def scrape(self, url):
        token = _allow_jina.set(self.allow_jina)
        try:
            result = upstream.scrape_url(url, max_length=50000)
            if not result.get('success'):
                raise ValueError(result.get('error', 'Scraping gagal.'))
            if len(result.get('content', '').split()) < 15:
                raise ValueError('Konten terlalu pendek; halaman mungkin memerlukan JavaScript/login.')
            return result
        finally:
            _allow_jina.reset(token)

    def research(self, topic, mode='auto'):
        token = _allow_jina.set(self.allow_jina)
        try:
            result = upstream.conduct_autonomous_research(topic, mode)
            if not result.get('success'):
                raise ValueError(result.get('error', 'Riset gagal.'))
            return result
        finally:
            _allow_jina.reset(token)

    def academic(self, query, limit=5):
        return upstream.search_academic_papers_unified(query, max_results=min(max(limit, 1), 10))

    def search_web(self, query, limit=5, read_content=True):
        return search_internet_multi(query, max_results=min(max(limit, 1), 10), read_content=read_content)

    def detect_category(self, raw):
        return detect_category(raw)

    def demo(self):
        html = files('scrapmcp').joinpath('fixtures/materi.html').read_text(encoding='utf-8')
        result = upstream._extract_page_data_bs4(html, 50000, 'https://example.org/simulasi/materi')
        result.update(success=True, url='https://example.org/simulasi/materi', dataset_kind='simulation', source_type='offline_fixture')
        return result
