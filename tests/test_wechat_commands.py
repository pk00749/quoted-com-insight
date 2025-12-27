import pytest

from app.routers.commands import (
    handle_add,
    handle_del,
    handle_subscribe,
    handle_query,
    fmt_utc_iso_to_cst_min,
)


class DummySubService:
    def __init__(self):
        self.added = []
        self.deleted = []
        self.codes = []
        self.summaries = {}
        self.timestamps = {}

    def add_code(self, from_user, code):
        self.added.append((from_user, code))
        return True, f"已订阅 {code}"

    def del_code(self, from_user, code):
        self.deleted.append((from_user, code))
        return True, f"已取消订阅 {code}"

    def list_codes(self, from_user):
        return list(self.codes)

    def get_summary_timestamps(self, codes):
        return {c: self.timestamps.get(c, "") for c in codes}

    def load_summary_text(self, code):
        return self.summaries.get(code, "")


def test_handle_add(monkeypatch):
    svc = DummySubService()
    monkeypatch.setattr("app.routers.commands.add.subscription_service", svc)
    msg = handle_add("user", "add600000")
    assert "已订阅 600000" in msg
    assert svc.added == [("user", "600000")]


def test_handle_del(monkeypatch):
    svc = DummySubService()
    monkeypatch.setattr("app.routers.commands.delete.subscription_service", svc)
    msg = handle_del("user", "del600000")
    assert "已取消订阅 600000" in msg
    assert svc.deleted == [("user", "600000")]


def test_handle_subscribe_with_timestamps(monkeypatch):
    svc = DummySubService()
    svc.codes = ["600000", "000001"]
    svc.timestamps = {"600000": "2024-01-02T03:04:00+00:00", "000001": ""}
    monkeypatch.setattr("app.routers.commands.subscribe.subscription_service", svc)
    msg = handle_subscribe("user")
    assert "订阅列表(2):" in msg
    assert "600000 2024-01-02 11:04" in msg
    assert "000001 尚未刷新" in msg


def test_handle_subscribe_empty(monkeypatch):
    svc = DummySubService()
    monkeypatch.setattr("app.routers.commands.subscribe.subscription_service", svc)
    msg = handle_subscribe("user")
    assert "当前未订阅" in msg


def test_handle_query_with_cache(monkeypatch):
    svc = DummySubService()
    svc.summaries = {"600000": "cached summary"}
    svc.timestamps = {"600000": "2024-01-02T03:04:00+00:00"}
    monkeypatch.setattr("app.routers.commands.query.subscription_service", svc)
    result = handle_query("user", "600000")
    assert "600000 2024-01-02 11:04" in result
    assert "cached summary" in result


def test_handle_query_no_cache(monkeypatch):
    svc = DummySubService()
    monkeypatch.setattr("app.routers.commands.query.subscription_service", svc)
    result = handle_query("user", "600000")
    assert result == "600000 无公告摘要，稍后再试"


def test_fmt_utc_iso_to_cst_min():
    assert fmt_utc_iso_to_cst_min("2024-01-02T03:04:00+00:00") == "2024-01-02 11:04"
    assert fmt_utc_iso_to_cst_min("") == ""
    assert fmt_utc_iso_to_cst_min("bad") == ""
