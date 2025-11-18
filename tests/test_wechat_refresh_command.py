import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routers.wechat import REFRESH_INTERVAL_SECONDS
import time

# 简单的XML构造器

def build_text_xml(from_user: str, to_user: str, content: str):
    return f"""<xml>
<ToUserName><![CDATA[{to_user}]]></ToUserName>
<FromUserName><![CDATA[{from_user}]]></FromUserName>
<CreateTime>{int(time.time())}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{content}]]></Content>
<MsgId>1</MsgId>
</xml>"""

client = TestClient(app)

@pytest.mark.asyncio
async def test_refresh_success(monkeypatch):
    # Mock summarize_announcements
    async def fake_summarize(code: str):
        return {"content": f"Summary for {code}"}
    from app.services import announcement_service as mod_ann
    monkeypatch.setattr(mod_ann.announcement_service, "summarize_announcements", fake_summarize)

    # Mock save_summary to avoid filesystem writes complexity
    from app.services import subscription_service as mod_sub
    def fake_save(code, data):
        pass
    monkeypatch.setattr(mod_sub.subscription_service, "save_summary", fake_save)

    xml_body = build_text_xml("userA", "server", "refresh600000")
    params = {"signature": "", "timestamp": "1", "nonce": "2"}
    # Skip signature verification by monkeypatching _verify
    from app.routers import wechat as wechat_mod
    monkeypatch.setattr(wechat_mod, "_verify", lambda a,b,c: True)

    resp = client.post("/wechat/callback", params=params, data=xml_body.encode("utf-8"))
    assert resp.status_code == 200
    # 新的返回格式：600000 已刷新，YYYY-MM-DD HH:MM
    assert "600000 已刷新" in resp.text

@pytest.mark.asyncio
async def test_refresh_rate_limit(monkeypatch):
    async def fake_summarize(code: str):
        return {"content": f"Summary for {code}"}
    from app.services import announcement_service as mod_ann
    monkeypatch.setattr(mod_ann.announcement_service, "summarize_announcements", fake_summarize)
    from app.services import subscription_service as mod_sub
    monkeypatch.setattr(mod_sub.subscription_service, "save_summary", lambda c,d: None)
    from app.routers import wechat as wechat_mod
    monkeypatch.setattr(wechat_mod, "_verify", lambda a,b,c: True)

    xml_body = build_text_xml("userA", "server", "refresh600001")
    params = {"signature": "", "timestamp": "1", "nonce": "2"}
    resp1 = client.post("/wechat/callback", params=params, data=xml_body.encode("utf-8"))
    assert resp1.status_code == 200
    resp2 = client.post("/wechat/callback", params=params, data=xml_body.encode("utf-8"))
    assert resp2.status_code == 200
    assert "刷新过于频繁" in resp2.text

