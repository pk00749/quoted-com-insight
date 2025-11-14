# filepath: /Users/yorkhxli/git/quoted-com-insight/app/services/subscription_service.py
import os
import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import List, Tuple, Set, Dict

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data")
DB_PATH = os.path.abspath(os.path.join(DATA_DIR, "subscriptions.db"))
SUMMARY_DIR = os.path.abspath(os.path.join(DATA_DIR, "summaries"))

os.makedirs(os.path.abspath(DATA_DIR), exist_ok=True)
os.makedirs(SUMMARY_DIR, exist_ok=True)


class SubscriptionService:
    """基于SQLite的订阅管理与缓存写入服务"""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with self._conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_user TEXT NOT NULL UNIQUE,
                    stock_code_list TEXT NOT NULL DEFAULT '[]',
                    updated_datetime TEXT
                )
                """
            )
            # 新增：每个股票代码对应的最近 summary 更新时间（全局，不按用户区分）
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS subscription_summaries (
                    stock_code TEXT PRIMARY KEY,
                    summary_updated_datetime TEXT
                )
                """
            )
            conn.commit()

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _normalize_code(code: str) -> str:
        code = (code or "").strip()
        return code if len(code) == 6 and code.isdigit() else ""

    def _get_codes(self, conn: sqlite3.Connection, from_user: str) -> Set[str]:
        cur = conn.execute(
            "SELECT stock_code_list FROM subscriptions WHERE from_user=?",
            (from_user,),
        )
        row = cur.fetchone()
        if not row:
            return set()
        try:
            data = json.loads(row[0])
            return set(data) if isinstance(data, list) else set()
        except Exception:
            return set()

    def add_code(self, from_user: str, code: str) -> Tuple[bool, str]:
        code = self._normalize_code(code)
        if not code:
            return False, "股票代码格式不正确，应为6位数字"
        with self._conn() as conn:
            codes = self._get_codes(conn, from_user)
            if code in codes:
                return True, f"{code} 已在订阅列表"
            codes.add(code)
            payload = json.dumps(sorted(list(codes)))
            conn.execute(
                "INSERT INTO subscriptions(from_user, stock_code_list, updated_datetime) VALUES(?,?,?)\n                 ON CONFLICT(from_user) DO UPDATE SET stock_code_list=excluded.stock_code_list, updated_datetime=excluded.updated_datetime",
                (from_user, payload, self._now_iso()),
            )
            conn.commit()
            return True, f"已订阅 {code}"

    def del_code(self, from_user: str, code: str) -> Tuple[bool, str]:
        code = self._normalize_code(code)
        if not code:
            return False, "股票代码格式不正确，应为6位数字"
        with self._conn() as conn:
            codes = self._get_codes(conn, from_user)
            if code not in codes:
                return True, f"{code} 不在订阅列表"
            codes.remove(code)
            payload = json.dumps(sorted(list(codes)))
            conn.execute(
                "INSERT INTO subscriptions(from_user, stock_code_list, updated_datetime) VALUES(?,?,?)\n                 ON CONFLICT(from_user) DO UPDATE SET stock_code_list=excluded.stock_code_list, updated_datetime=excluded.updated_datetime",
                (from_user, payload, self._now_iso()),
            )
            conn.commit()
            return True, f"已取消订阅 {code}"

    def list_codes(self, from_user: str) -> List[str]:
        with self._conn() as conn:
            return sorted(list(self._get_codes(conn, from_user)))

    def all_rows(self) -> List[Tuple[str, List[str]]]:
        with self._conn() as conn:
            cur = conn.execute("SELECT from_user, stock_code_list FROM subscriptions")
            rows = []
            for from_user, lst in cur.fetchall():
                try:
                    codes = json.loads(lst)
                except Exception:
                    codes = []
                if isinstance(codes, list):
                    rows.append((from_user, codes))
            return rows

    def touch(self, from_user: str):
        with self._conn() as conn:
            conn.execute(
                "UPDATE subscriptions SET updated_datetime=? WHERE from_user=?",
                (self._now_iso(), from_user),
            )
            conn.commit()

    def summary_path(self, stock_code: str) -> str:
        fname = f"{stock_code}.json"
        return os.path.join(SUMMARY_DIR, fname)

    def save_summary(self, stock_code: str, data: Dict):
        # 保存总结文件
        path = self.summary_path(stock_code)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # 更新 summary 更新时间
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO subscription_summaries(stock_code, summary_updated_datetime) VALUES(?,?)\n                 ON CONFLICT(stock_code) DO UPDATE SET summary_updated_datetime=excluded.summary_updated_datetime",
                (stock_code, self._now_iso()),
            )
            conn.commit()

    def load_summary_text(self, stock_code: str) -> str:
        path = self.summary_path(stock_code)
        if not os.path.exists(path):
            return ""
        try:
            with open(path, "r", encoding="utf-8") as f:
                obj = json.load(f)
            # 兼容不同字段名
            return obj.get("content") or obj.get("summary") or json.dumps(obj, ensure_ascii=False)
        except Exception:
            return ""

    def get_summary_timestamps(self, codes: List[str]) -> Dict[str, str]:
        if not codes:
            return {}
        placeholders = ",".join(["?"] * len(codes))
        with self._conn() as conn:
            cur = conn.execute(
                f"SELECT stock_code, summary_updated_datetime FROM subscription_summaries WHERE stock_code IN ({placeholders})",
                codes,
            )
            mapping = {}
            for sc, ts in cur.fetchall():
                mapping[sc] = ts or ""
            return mapping


subscription_service = SubscriptionService()
