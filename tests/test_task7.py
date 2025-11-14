# 任务7测试：订阅 add/del 指令 + 缓存读取 + 实时生成
import time
import hashlib
import os
import json
import re
from contextlib import asynccontextmanager

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.subscription_service import subscription_service
from app.services import announcement_service as ann_mod

TOKEN = os.getenv("WECHAT_TOKEN", "testtoken")  # 与 settings.wechat_token 保持一致（测试环境下）


def wechat_signature(token: str, timestamp: str, nonce: str) -> str:
    raw = "".join(sorted([token, timestamp, nonce]))
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def build_xml(from_user: str, to_user: str, content: str) -> str:
    return (
        f"<xml>"
        f"<ToUserName><![CDATA[{to_user}]]></ToUserName>"
        f"<FromUserName><![CDATA[{from_user}]]></FromUserName>"
        f"<CreateTime>{int(time.time())}</CreateTime>"
        f"<MsgType><![CDATA[text]]></MsgType>"
        f"<Content><![CDATA[{content}]]></Content>"
        f"<MsgId>1</MsgId>"
        f"</xml>"
    )


def extract_reply_text(xml: str) -> str:
    m = re.search(r"<Content><!\[CDATA\[(.*?)\]\]></Content>", xml, re.S)
    return m.group(1).strip() if m else ""


@asynccontextmanager
async def dummy_lifespan(_app):
    # 覆盖真实 lifespan，避免启动长时间睡眠的定时任务
    yield


@pytest.fixture(scope="module")
def client():
    # 覆盖 lifespan，防止每日定时任务阻塞测试
    app.router.lifespan_context = dummy_lifespan
    with TestClient(app) as c:
        yield c


def common_post(client: TestClient, content: str, from_user: str = "user_test", to_user: str = "server"):
    ts = str(int(time.time()))
    nonce = "123456"
    sig = wechat_signature(TOKEN, ts, nonce)
    xml_body = build_xml(from_user, to_user, content)
    resp = client.post(
        "/wechat/callback",
        params={"signature": sig, "timestamp": ts, "nonce": nonce},
        data=xml_body,
        headers={"Content-Type": "application/xml"},
    )
    assert resp.status_code == 200
    return extract_reply_text(resp.text)


def test_add_subscription(client):
    reply = common_post(client, "add600000")
    assert "已订阅" in reply or "已在订阅" in reply
    codes = subscription_service.list_codes("user_test")
    assert "600000" in codes


def test_add_invalid_code(client):
    reply = common_post(client, "add123")
    assert "股票代码格式不正确" in reply


def test_del_subscription(client):
    # 先确保存在
    common_post(client, "add600001")
    reply = common_post(client, "del600001")
    assert "已取消订阅" in reply or "不在订阅" in reply


def test_cache_hit(client, tmp_path):
    # 预写入缓存文件
    subscription_service.save_summary("600002", {"content": "缓存内容测试"})
    reply = common_post(client, "600002")
    assert "缓存内容测试" in reply


@pytest.mark.asyncio
async def test_realtime_generate(monkeypatch, client):
    # 删除可能存在的缓存
    path = subscription_service.summary_path("600003")
    if os.path.exists(path):
        os.remove(path)

    async def fake_sum(code: str):
        return {"content": f"生成内容_{code}"}

    monkeypatch.setattr(ann_mod.announcement_service, "summarize_announcements", fake_sum)

    reply = common_post(client, "600003")
    assert "生成内容_600003" in reply
    # 缓存文件已写入
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    assert obj.get("content") == "生成内容_600003"


def test_help_message(client):
    reply = common_post(client, "help")
    assert "使用说明" in reply


def test_unknown_input(client):
    reply = common_post(client, "hello world")
    assert "请输入6位A股代码" in reply

