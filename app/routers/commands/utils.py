from datetime import datetime
from zoneinfo import ZoneInfo


def fmt_utc_iso_to_cst_min(iso_str: str) -> str:
    """Convert ISO UTC string to Asia/Shanghai minute resolution; return empty string on failure."""
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
