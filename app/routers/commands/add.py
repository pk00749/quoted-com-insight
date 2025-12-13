import re
from ..services.subscription_service import subscription_service

ADD_PATTERN = re.compile(r"^add(\d{6})$")

def handle_add(from_user: str, content: str) -> str:
    m = ADD_PATTERN.match(content)
    if not m:
        return "命令格式错误：addXXXXXX"
    code = m.group(1)
    ok, msg = subscription_service.add_code(from_user, code)
    return msg
