import pytest

from app.routers.commands import handle_query


class DummyAnnouncementService:
    def __init__(self, summaries=None):
        self.summaries = summaries or {}
    
    async def summarize_announcements(self, code):
        if code in self.summaries:
            return self.summaries[code]
        raise Exception(f"No summary for {code}")


@pytest.mark.asyncio
async def test_handle_query_success(monkeypatch):
    svc = DummyAnnouncementService({"600000": "Test summary"})
    monkeypatch.setattr("app.routers.commands.query.announcement_service", svc)
    
    result = await handle_query("user", "600000")
    assert "600000" in result
    assert "Test summary" in result


@pytest.mark.asyncio
async def test_handle_query_failure(monkeypatch):
    svc = DummyAnnouncementService({})
    monkeypatch.setattr("app.routers.commands.query.announcement_service", svc)
    
    result = await handle_query("user", "600000")
    assert "获取公告摘要失败" in result


def test_handle_query_invalid_code():
    result = handle_query("user", "invalid")
    assert result is None


def test_handle_query_non_six_digits():
    result = handle_query("user", "12345")
    assert result is None
    result = handle_query("user", "1234567")
    assert result is None
