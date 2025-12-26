import re
from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo
from ..services.subscription_service import subscription_service


_QUERY_RE = re.compile(r"^(\d{6})$")


def _fmt_utc_iso_to_cst_min(iso_str: str) -> str:
    try:
        if not iso_str:
            return ""
        if iso_str.endswith("Z"):
            iso_str = iso_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(iso_str)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))
        cst = dt.astimezone(ZoneInfo("Asia/Shanghai"))
        return cst.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ""


def handle_query(from_user: str, content: str) -> Optional[str]:
    m = _QUERY_RE.match(content)
    if not m:
        return None
    code = m.group(1)
    # 先读取缓存文本
    cached = subscription_service.load_summary_text(code)
    # 获取缓存时间戳
    ts_map = subscription_service.get_summary_timestamps([code])
    ts_fmt = _fmt_utc_iso_to_cst_min(ts_map.get(code, ""))
    if cached:
        prefix = f"{code} {ts_fmt}" if ts_fmt else code
        return f"{prefix}\n\n{cached}"
    return f"{code} 无公告摘要，稍后再试"
