from typing import List
from app.services.subscription_service import subscription_service
from datetime import datetime
from zoneinfo import ZoneInfo


def handle_subscribe(from_user: str) -> str:
    codes: List[str] = subscription_service.list_codes(from_user)
    if not codes:
        return "当前未订阅任何股票，发送 add600000 开始订阅"
    ts_map = subscription_service.get_summary_timestamps(codes)
    lines = []
    for sc in codes[:100]:
        ts = ts_map.get(sc, "") or ""
        if ts.endswith("Z"):
            ts = ts.replace("Z", "+00:00")
        try:
            dt = datetime.fromisoformat(ts)
            if not dt.tzinfo:
                dt = dt.replace(tzinfo=ZoneInfo("UTC"))
            cst = dt.astimezone(ZoneInfo("Asia/Shanghai"))
            ts_fmt = cst.strftime("%Y-%m-%d %H:%M")
        except Exception:
            ts_fmt = "尚未刷新"
        lines.append(f"{sc} {ts_fmt}")
    reply = "订阅列表(" + str(len(codes)) + "):\n" + "\n".join(lines)
    if len(codes) > 100:
        reply += f"\n其余 {len(codes)-100} 个已省略"
    return reply
