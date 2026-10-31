"""Bounded public-URL HTTP fetches, including every redirect.
DNS is validated before fetch; this is not a DNS-pinning sandbox.
"""
import ipaddress
import socket
import time
from urllib.parse import urlsplit, urljoin
import requests

MAX_BYTES = 15 * 1024 * 1024

def validate_url(url):
    try:
        p = urlsplit(url.strip())
        if p.scheme not in ('http', 'https') or not p.hostname:
            raise ValueError('URL harus HTTP/HTTPS dan memiliki hostname.')
        if p.username or p.password:
            raise ValueError('URL dengan username/password tidak didukung.')
        if p.port not in (None, 80, 443):
            raise ValueError('Hanya port web 80/443 yang didukung.')
        if p.hostname.lower() == 'localhost':
            raise ValueError('Alamat lokal/privat diblokir.')
        addresses = socket.getaddrinfo(p.hostname, p.port or 443, type=socket.SOCK_STREAM)
        if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
            raise ValueError('Alamat lokal/privat diblokir.')
        return {'valid': True, 'url': url.strip(), 'hostname': p.hostname}
    except (ValueError, OSError, AttributeError) as exc:
        return {'valid': False, 'error': str(exc)}

class PublicHTTP:
    exceptions = requests.exceptions

    @staticmethod
    def get(url, **kwargs):
        kwargs.pop('allow_redirects', None)
        kwargs.pop('stream', None)
        kwargs.setdefault('timeout', 15)
        started = time.monotonic()
        for _ in range(6):
            checked = validate_url(url)
            if not checked['valid']:
                raise ValueError(checked['error'])
            response = requests.get(url, allow_redirects=False, stream=True, **kwargs)
            try:
                if response.status_code in (301, 302, 303, 307, 308):
                    location = response.headers.get('Location')
                    if not location:
                        raise ValueError('Redirect tanpa Location.')
                    url = urljoin(url, location)
                    continue
                if int(response.headers.get('Content-Length', '0')) > MAX_BYTES:
                    raise ValueError('Respons melebihi batas 15 MB.')
                chunks, total = [], 0
                for chunk in response.iter_content(65536):
                    total += len(chunk)
                    if total > MAX_BYTES or time.monotonic() - started > 60:
                        raise ValueError('Batas ukuran/waktu unduhan terlampaui.')
                    chunks.append(chunk)
                response._content = b''.join(chunks)
                response._content_consumed = True
                return response
            finally:
                response.close()
        raise ValueError('Terlalu banyak redirect.')
