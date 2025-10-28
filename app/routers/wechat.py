from fastapi import APIRouter, Query, HTTPException, Response, Request
from typing import Optional
import hashlib
import time
import re
import xml.etree.ElementTree as ET

from ..core.config import settings
from ..services.announcement_service import announcement_service

router = APIRouter()


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

    if msg_type.lower() != "text":
        reply = "暂仅支持文本消息，请发送6位A股代码，如 000001"
        xml = _build_text_reply(from_user, to_user, reply)
        return Response(content=xml, media_type="application/xml; charset=utf-8")

    # 3) 解析股票代码（6位数字）
    m = re.search(r"\b(\d{6})\b", content)
    if not m:
        reply = "请输入6位A股代码，如 000001"
        xml = _build_text_reply(from_user, to_user, reply)
        return Response(content=xml, media_type="application/xml; charset=utf-8")

    stock_code = m.group(1)

    # 4) 调用内部服务进行总结
    try:
        result = await announcement_service.summarize_announcements(stock_code)
        final_text = result.get("content") or result.get("summary") or "生成总结失败，请稍后重试"
    except Exception as ex:
        final_text = f"服务暂不可用，请稍后重试。错误：{ex}"

    # 5) 构造被动回复
    xml = _build_text_reply(from_user, to_user, final_text)
    return Response(content=xml, media_type="application/xml; charset=utf-8")

