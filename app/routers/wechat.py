from fastapi import APIRouter, Query, HTTPException, Response, Request
from typing import Optional
import hashlib
import time
import re
from collections import defaultdict

# refresh 频控：同一代码刷新间隔秒数
REFRESH_INTERVAL_SECONDS = 60
_last_refresh_ts = defaultdict(lambda: 0.0)  # stock_code -> epoch seconds
import xml.etree.ElementTree as ET
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from ..core.config import settings
from ..services.announcement_service import announcement_service
from ..services.subscription_service import subscription_service  # 新增：订阅服务
from .commands import handle_add, handle_del, handle_subscribe, handle_query

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


def _fmt_utc_iso_to_cst_min(ts: str) -> str:
    """将UTC ISO时间转换为北京时间 YYYY-MM-DD HH:MM；若无效返回“尚未刷新”。"""
    if not ts:
        return "尚未刷新"
    try:
        # 兼容以Z结尾
        if ts.endswith("Z"):
            ts = ts.replace("Z", "+00:00")
        dt = datetime.fromisoformat(ts)
        if not dt.tzinfo:
            # 视为UTC
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))
        cst = dt.astimezone(ZoneInfo("Asia/Shanghai"))
        return cst.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "尚未刷新"


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
            f"Version: {settings.version}\n"
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
            "4) subscribe 查看订阅列表\n"
            "5) refreshXXXXXX 立即刷新公告总结 (例 refresh600000)"
        )
        xml = _build_text_reply(from_user, to_user, reply)
        return Response(content=xml, media_type="application/xml; charset=utf-8")

    # subscribe / list / my 查询订阅列表（任务8 + 任务9：带更新时间显示）
    if content.lower() in ("subscribe", "list", "my"):
        reply = handle_subscribe(from_user)
        xml = _build_text_reply(from_user, to_user, reply)
        return Response(content=xml, media_type="application/xml; charset=utf-8")

    # 订阅添加
    m_add = re.match(r"^add(\d{6})$", content)
    if m_add:
        msg = handle_add(from_user, content)
        xml = _build_text_reply(from_user, to_user, msg)
        return Response(content=xml, media_type="application/xml; charset=utf-8")

    # 订阅删除
    m_del = re.match(r"^del(\d{6})$", content)
    if m_del:
        msg = handle_del(from_user, content)
        xml = _build_text_reply(from_user, to_user, msg)
        return Response(content=xml, media_type="application/xml; charset=utf-8")

    # refresh 命令：即时刷新指定股票公告总结（^refresh\d{6}$）
    m_refresh = re.match(r"^refresh(\d{6})$", content)
    if m_refresh:
        code = m_refresh.group(1)
        now_sec = time.time()
        last_ts = _last_refresh_ts[code]
        if now_sec - last_ts < REFRESH_INTERVAL_SECONDS:
            remain = int(REFRESH_INTERVAL_SECONDS - (now_sec - last_ts))
            reply = f"{code} 刷新过于频繁，请 {remain}s 后再试"
            xml = _build_text_reply(from_user, to_user, reply)
            return Response(content=xml, media_type="application/xml; charset=utf-8")
        try:
            result = await announcement_service.summarize_announcements(code)
            subscription_service.save_summary(code, result)
            _last_refresh_ts[code] = now_sec
            # 根据提案更新：不直接返回总结内容，仅返回已刷新提示 + 北京时间
            refreshed_at = datetime.fromtimestamp(now_sec, tz=ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M")
            reply = f"{code} 已刷新，{refreshed_at}"  # 仍然后台保存内容供后续查询
        except Exception as ex:
            reply = f"刷新失败: {ex}"[:1800]
        xml = _build_text_reply(from_user, to_user, reply)
        return Response(content=xml, media_type="application/xml; charset=utf-8")

    # 直接查询股票代码（模块化处理）
    q = handle_query(from_user, content)
    if q is None:
        xml = _build_text_reply(from_user, to_user, "请输入6位A股代码，如 000001")
        return Response(content=xml, media_type="application/xml; charset=utf-8")
    xml = _build_text_reply(from_user, to_user, q[:1800])
    logger.info("Reply XML: %s", xml)
    return Response(content=xml, media_type="application/xml; charset=utf-8")
