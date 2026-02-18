import re
from typing import Optional

from app.services.announcement_service import announcement_service


_QUERY_RE = re.compile(r"^(\d{6})$")


async def handle_query(from_user: str, content: str) -> Optional[str]:
    m = _QUERY_RE.match(content)
    if not m:
        return None
    code = m.group(1)
    try:
        result = await announcement_service.summarize_announcements(code)
        return f"{code}\n\n{result}"
    except Exception:
        return f"{code} 获取公告摘要失败，请稍后再试"
