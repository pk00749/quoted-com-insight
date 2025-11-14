from fastapi import APIRouter, Query, HTTPException, Response, Request
from typing import Optional
import hashlib
import time
import re
import xml.etree.ElementTree as ET
import logging

from ..core.config import settings
from ..services.announcement_service import announcement_service
from ..services.subscription_service import subscription_service  # 新增：订阅服务

router = APIRouter()
logger = logging.getLogger(__name__)


def _sign(token: str, timestamp: str, nonce: str) -> str:
    """按微信规则计算签名：将 token、timestamp、nonce 字典序排序后拼接，做 SHA1。"""
    raw = "".join(sorted([token, timestamp, nonce]))
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def _verify(signature: str, timestamp: str, nonce: str) -> bool:
    expected = _sign(settings.wechat_token, timestamp, nonce)
    return expected == signature


def _extract_text(xml_bytes: bytes) -> dict:
    """解析微信XML文本，仅处理明文模式，返回关键信息字典。"""
    root = ET.fromstring(xml_bytes)
    data = {}
    for tag in [
        "ToUserName",
        "FromUserName",
        "CreateTime",
        "MsgType",
        "Content",
        "MsgId",
    ]:
        elem = root.find(tag)
        data[tag] = elem.text if elem is not None else None
    return data


def _build_text_reply(to_user: str, from_user: str, content: str) -> str:
    now = int(time.time())
    # 被动回复文本消息 XML
    return (
        f"<xml>\n"
        f"  <ToUserName><![CDATA[{to_user}]]></ToUserName>\n"
        f"  <FromUserName><![CDATA[{from_user}]]></FromUserName>\n"
        f"  <CreateTime>{now}</CreateTime>\n"
        f"  <MsgType><![CDATA[text]]></MsgType>\n"
        f"  <Content><![CDATA[{content}]]></Content>\n"
        f"</xml>"
    )


@router.get("/wechat/callback")
async def wechat_verify(
    signature: str = Query(..., description="微信签名"),
    timestamp: str = Query(..., description="时间戳"),
    nonce: str = Query(..., description="随机数"),
    echostr: str = Query(..., description="回显字符串"),
):
    """用于微信公众号服务器接入校验（GET）。验证成功后原样返回 echostr。"""
    if not _verify(signature, timestamp, nonce):
        raise HTTPException(status_code=403, detail="签名校验失败")
    return Response(content=echostr, media_type="text/plain; charset=utf-8")


@router.post("/wechat/callback")
async def wechat_message(
    request: Request,
    signature: str = Query(..., description="微信签名"),
    timestamp: str = Query(..., description="时间戳"),
    nonce: str = Query(..., description="随机数"),
    msg_signature: Optional[str] = Query(None, description="消息体签名（安全/兼容模式预留）"),
    encrypt_type: Optional[str] = Query(None, description="加密类型（aes/明文）"),
):
    """接收微信公众号文本消息（POST），仅处理明文模式；安全模式预留。"""
    # 1) 校验 URL 签名
    if not _verify(signature, timestamp, nonce):
        raise HTTPException(status_code=403, detail="签名校验失败")

    # 2) 仅实现明文模式，安全/兼容模式解密留待后续
    body = await request.body()
    try:
        data = _extract_text(body)
    except Exception as ex:
        raise HTTPException(status_code=400, detail=f"XML解析失败: {ex}")

    from_user = data.get("FromUserName") or ""
    to_user = data.get("ToUserName") or ""
    msg_type = data.get("MsgType") or ""
    content = (data.get("Content") or "").strip()
    event = data.get("Event") or ""
    msg_id = data.get("MsgId") or ""
    msg_data_id = data.get("MsgDataId") or ""

    if msg_type.lower() != "text":
        xml = _build_text_reply(from_user, to_user, "暂仅支持文本消息，请发送6位A股代码，如 000001")
        return Response(content=xml, media_type="application/xml; charset=utf-8")


    if content == "admin":
        reply = (
            f"Event：{event}\n"
            f"From User: {from_user}\n"
            f"To User: {to_user}\n"
            f"Msg ID: {msg_id}\n"
            f"Msg Data ID: {msg_data_id}\n"
        )
        xml = _build_text_reply(from_user, to_user, reply)
        return Response(content=xml, media_type="application/xml; charset=utf-8")

    # 帮助
    if content == "帮助" or content == "help":
        reply = (
            "使用说明:\n"
            "1) 发送 6 位股票代码获取近期公告总结\n"
            "2) addXXXXXX 加入订阅 (例 add600000)\n"
            "3) delXXXXXX 取消订阅 (例 del600000)\n"
            "4) subscribe 获取欢迎信息"
        )
        xml = _build_text_reply(from_user, to_user, reply)
        return Response(content=xml, media_type="application/xml; charset=utf-8")

    # subscribe 欢迎
    if content.lower() == "subscribe":
        reply = (
            f"欢迎 {from_user} 使用公告信息服务！\n"
            "发送 6 位A股代码获取公告总结，或使用 addXXXXXX / delXXXXXX 管理订阅。"
        )
        xml = _build_text_reply(from_user, to_user, reply)
        return Response(content=xml, media_type="application/xml; charset=utf-8")

    # 订阅添加
    m_add = re.match(r"^add(\d{6})$", content)
    if m_add:
        code = m_add.group(1)
        ok, msg = subscription_service.add_code(from_user, code)
        xml = _build_text_reply(from_user, to_user, msg)
        return Response(content=xml, media_type="application/xml; charset=utf-8")

    # 订阅删除
    m_del = re.match(r"^del(\d{6})$", content)
    if m_del:
        code = m_del.group(1)
        ok, msg = subscription_service.del_code(from_user, code)
        xml = _build_text_reply(from_user, to_user, msg)
        return Response(content=xml, media_type="application/xml; charset=utf-8")

    # 直接查询股票代码
    m = re.search(r"\b(\d{6})\b", content)
    if not m:
        xml = _build_text_reply(from_user, to_user, "请输入6位A股代码，如 000001 或使用 help")
        return Response(content=xml, media_type="application/xml; charset=utf-8")

    stock_code = m.group(1)

    # 优先读取缓存
    cached = subscription_service.load_summary_text(stock_code)
    if cached:
        xml = _build_text_reply(from_user, to_user, cached[:1800])  # 控制长度
        return Response(content=xml, media_type="application/xml; charset=utf-8")

    # 缓存无则实时生成
    try:
        result = await announcement_service.summarize_announcements(stock_code)
        subscription_service.save_summary(stock_code, result)
        subscription_service.touch(from_user)
        final_text = result.get("content") or result.get("summary") or "生成总结失败"
    except Exception as ex:
        final_text = f"服务暂不可用：{ex}"

    xml = _build_text_reply(from_user, to_user, final_text[:1800])
    logger.info("Reply XML: %s", xml)
    return Response(content=xml, media_type="application/xml; charset=utf-8")
