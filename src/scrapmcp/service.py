"""Shared pipeline for interactive CLI and MCP tools."""
from .engine import Engine
from .storage import Store

class Service:
    def __init__(self, root, allow_jina=False):
        self.store = Store(root)
        self.engine = Engine(allow_jina)

    def scrape(self, url, category=None):
        try:
            raw = self.engine.scrape(url)
            if not category or str(category).strip().lower() in ('umum', 'auto', 'otomatis', ''):
                category = self.engine.detect_category(raw)
            row = self.store.save(raw, category)
            self.store.event('scrape', True, f"id: {row['id']} | \"{row.get('title')}\" ({row.get('category')}, {row.get('word_count')} kata)")
            return row
        except Exception as exc:
            self.store.event('scrape', False, f"url: {url} | error: {type(exc).__name__}: {exc}")
            raise

    def demo(self):
        row = self.store.save(self.engine.demo(), 'simulasi')
        self.store.event('demo', True, f"id: {row['id']} | \"{row.get('title')}\" (simulasi offline)")
        return {'record':row, 'report':self.store.report(), 'backup':self.store.backup()}

    def research(self, topic, mode='auto', save=False):
        try:
            result = self.engine.research(topic, mode)
            if save:
                payload = result['materi_siap_simpan']
                result['saved_record'] = self.store.save(payload, payload.get('category','riset'))
                result['saved_to_db'] = False
                result['saved_locally'] = True
                result['needs_user_confirmation'] = False
                result.pop('confirmation_prompt',None)
                result.pop('instruksi_ai',None)
            self.store.event('research', True, f"topic: {topic} | saved: {save}")
            return result
        except Exception as exc:
            self.store.event('research', False, str(exc))
            raise
