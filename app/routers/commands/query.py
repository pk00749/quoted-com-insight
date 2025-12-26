import re
from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo

from app.services.announcement_service import announcement_service


_QUERY_RE = re.compile(r"^(\d{6})$")


def _fmt_utc_iso_to_cst_min(iso_str: str) -> str:
    if iso_str.endswith("Z"):
        iso_str = iso_str.replace("Z", "+00:00")
    dt = datetime.fromisoformat(iso_str)
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    cst = dt.astimezone(ZoneInfo("Asia/Shanghai"))
    return cst.strftime("%Y-%m-%d %H:%M")


def handle_query(from_user: str, content: str) -> Optional[str]:
    m = _QUERY_RE.match(content)
    if not m:
        return None
    code = m.group(1)
    summary = announcement_service.summarize_latest(code)
    ts = announcement_service.get_cached_summary_timestamp(code)
    if summary:
        ts_fmt = _fmt_utc_iso_to_cst_min(ts) if ts else ""
        return f"{code} {ts_fmt}\n\n{summary}"
    return f"{code} 无公告摘要，稍后再试"
