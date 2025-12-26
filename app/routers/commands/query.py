import re
from typing import Optional

from app.services.subscription_service import subscription_service
from .utils import fmt_utc_iso_to_cst_min


_QUERY_RE = re.compile(r"^(\d{6})$")


def handle_query(from_user: str, content: str) -> Optional[str]:
    m = _QUERY_RE.match(content)
    if not m:
        return None
    code = m.group(1)
    # 先读取缓存文本
    cached = subscription_service.load_summary_text(code)
    # 获取缓存时间戳
    ts_map = subscription_service.get_summary_timestamps([code])
    ts_fmt = fmt_utc_iso_to_cst_min(ts_map.get(code, ""))
    if cached:
        prefix = f"{code} {ts_fmt}" if ts_fmt else code
        return f"{prefix}\n\n{cached}"
    return f"{code} 无公告摘要，稍后再试"
