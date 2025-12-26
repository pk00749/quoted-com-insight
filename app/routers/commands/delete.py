import re
from app.services.subscription_service import subscription_service

DEL_PATTERN = re.compile(r"^del(\d{6})$")

def handle_del(from_user: str, content: str) -> str:
    m = DEL_PATTERN.match(content)
    if not m:
        return "命令格式错误：delXXXXXX"
    code = m.group(1)
    ok, msg = subscription_service.del_code(from_user, code)
    return msg
