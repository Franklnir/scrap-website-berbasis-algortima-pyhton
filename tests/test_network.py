import socket
import requests
import pytest
from scrapmcp import network
from scrapmcp.engine import Engine, upstream

def dns(host,*args,**kwargs):
    ip = '127.0.0.1' if host in ('localhost','private.example') else '93.184.216.34'
    return [(socket.AF_INET,socket.SOCK_STREAM,6,'',(ip,443))]

@pytest.mark.parametrize('url',['file:///etc/passwd','http://localhost/a','https://private.example','https://user:pass@example.org','https://example.org:22'])
def test_blocks_bad_urls(url,monkeypatch):
    monkeypatch.setattr(socket,'getaddrinfo',dns)
    assert not network.validate_url(url)['valid']


def response(body=b'',status=200,headers=None):
    r=requests.Response(); r.status_code=status; r.headers=headers or {}; r._content=body; r._content_consumed=True
    r.url='https://example.org'
    return r


def test_redirect_private_blocked(monkeypatch):
    monkeypatch.setattr(socket,'getaddrinfo',dns)
    calls=[]
    def get(url,**kwargs):
        calls.append(url)
        return response(status=302,headers={'Location':'http://localhost/private'})
    monkeypatch.setattr(requests,'get',get)
    with pytest.raises(ValueError): network.PublicHTTP.get('https://example.org')
    assert len(calls)==1


def test_large_body_rejected(monkeypatch):
    monkeypatch.setattr(socket,'getaddrinfo',dns)
    monkeypatch.setattr(requests,'get',lambda *a,**k:response(headers={'Content-Length':str(network.MAX_BYTES+1)}))
    with pytest.raises(ValueError): network.PublicHTTP.get('https://example.org')


def test_http_html_pipeline(monkeypatch):
    from importlib.resources import files
    monkeypatch.setattr(socket,'getaddrinfo',dns)
    html=files('scrapmcp').joinpath('fixtures/materi.html').read_bytes()
    monkeypatch.setattr(requests,'get',lambda *a,**k:response(html,headers={'content-type':'text/html; charset=utf-8'}))
    result=Engine().scrape('https://example.org')
    assert result['success'] and 'Dasar Python' in result['content']


def test_http_error_status_not_lost(monkeypatch):
    monkeypatch.setattr(socket,'getaddrinfo',dns)
    monkeypatch.setattr(requests,'get',lambda *a,**k:response(status=403))
    with pytest.raises(ValueError,match='403'): Engine().scrape('https://example.org')


def test_pdf_extraction(monkeypatch):
    import io
    from reportlab.pdfgen.canvas import Canvas
    buf=io.BytesIO(); c=Canvas(buf)
    c.drawString(30,700,'Python automation learns files regex backup CLI scraping and reports for students.')
    c.save()
    monkeypatch.setattr(socket,'getaddrinfo',dns)
    monkeypatch.setattr(requests,'get',lambda *a,**k:response(buf.getvalue(),headers={'content-type':'application/pdf'}))
    result=Engine().scrape('https://example.org/test.pdf')
    assert result['source_type']=='pdf_document'
    assert 'Python automation' in result['content']
