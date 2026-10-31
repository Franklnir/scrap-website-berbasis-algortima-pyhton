import asyncio
import json
import pytest
from websockets.asyncio.server import serve
from websockets.asyncio.client import connect
from scrapmcp.mcp_server import serve_connection, validate_endpoint
from scrapmcp.service import Service


def test_endpoint_validation():
    assert validate_endpoint('wss://api.xiaozhi.me/mcp/?token=example')
    for url in ('https://xiaozhi.me/console/agents','ws://localhost','token-only'):
        with pytest.raises(ValueError): validate_endpoint(url)


def test_real_websocket_mcp_handshake_tools_and_reconnect(tmp_path, monkeypatch):
    async def scenario():
        service=Service(tmp_path)
        completed = []
        monkeypatch.setattr(service.engine, 'scrape', lambda url: service.engine.demo())
        monkeypatch.setattr(service.engine, 'research', lambda topic, mode: {
            'success':True, 'summary':'Riset simulasi', 'materi_siap_simpan':{
                'title':'Riset', 'url':'https://example.org/research', 'content':'Hasil riset simulasi untuk pengujian.', 'category':'riset'
            }
        })
        async def fake_xiaozhi(ws):
            async def rpc(ident,method,params=None):
                req={'jsonrpc':'2.0','id':ident,'method':method}
                if params is not None: req['params']=params
                await ws.send(json.dumps(req))
                while True:
                    result=json.loads(await asyncio.wait_for(ws.recv(),10))
                    if result.get('id')==ident: return result
            init=await rpc(1,'initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'mock-xiaozhi','version':'1.0'}})
            assert init['result']['serverInfo']['name']=='scrapmcp'
            await ws.send(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'}))
            listing=await rpc(2,'tools/list')
            names={t['name'] for t in listing['result']['tools']}
            assert {'scrape_webpage','research_topic','backup_dataset'} <= names
            call=await rpc(3,'tools/call',{'name':'list_materials','arguments':{}})
            assert not call['result'].get('isError')
            invalid=await rpc(4,'tools/call',{'name':'scrape_webpage','arguments':{}})
            assert invalid['result']['isError']
            saved=await rpc(5,'tools/call',{'name':'scrape_webpage','arguments':{'url':'https://example.org'}})
            assert not saved['result'].get('isError')
            result=json.loads(saved['result']['content'][0]['text'])
            assert service.store.read(result['id'])['word_count'] > 40
            preview=await rpc(7,'tools/call',{'name':'research_topic','arguments':{'topic':'simulasi'}})
            candidate=json.loads(preview['result']['content'][0]['text'])['candidate_id']
            before=len(service.store.records())
            confirmed=await rpc(8,'tools/call',{'name':'confirm_and_save_research_material','arguments':{'candidate_id':candidate}})
            assert not confirmed['result'].get('isError')
            assert len(service.store.records()) >= before
            backup=await rpc(9,'tools/call',{'name':'backup_dataset','arguments':{}})
            assert not backup['result'].get('isError')
            ping=await rpc(6,'ping')
            assert ping['result']=={}
            completed.append(True)
            await ws.close()
        async with serve(fake_xiaozhi,'127.0.0.1',0) as server:
            port=server.sockets[0].getsockname()[1]
            for _ in range(2):
                async with connect(f'ws://127.0.0.1:{port}') as ws:
                    await asyncio.wait_for(serve_connection(ws,service),20)
        assert len(completed) == 2
        assert (tmp_path / 'logs/events.jsonl').exists()
        assert (tmp_path / 'logs/activity.log').exists()
        events_text = (tmp_path / 'logs/events.jsonl').read_text()
        assert 'mcp_connect' in events_text
        assert 'mcp_scrape' in events_text
        assert 'mcp_backup_dataset' in events_text
    asyncio.run(scenario())
