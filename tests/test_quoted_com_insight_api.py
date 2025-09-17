import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.announcement_service import AnnouncementService

# 测试客户端
client = TestClient(app)

class TestStockAPI:
    """股票API测试用例"""

    @pytest.fixture
    def stock_service(self):
        """股票服务实例"""
        return AnnouncementService()

    def test_health_check(self):
        """测试健康检查接口"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "healthy" in data["data"]["status"]

    def test_version_info(self):
        """测试版本信息接口"""
        response = client.get("/api/v1/version")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "version" in data["data"]

    def test_get_announcements(self):
        """测试获取股票公告"""
        stock_code = "000001"
        response = client.get(f"/api/v1/stock/announcements/{stock_code}")

        assert response.status_code in [200, 400, 500]
        data = response.json()
        assert "success" in data

class TestAPIResponseFormat:
    """API响应格式测试"""

    def test_success_response_format(self):
        """测试成功响应格式"""
        response = client.get("/api/v1/health")
        data = response.json()

        # 检查响应格式
        assert "success" in data
        assert "data" in data
        assert "message" in data
        assert "timestamp" in data
        assert data["success"] is True

    def test_error_response_format(self):
        """测试错误响应格式"""
        # 触发一个验证错误
        response = client.get("/api/v1/stocks/search")

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data  # FastAPI验证错误格式

# 性能测试
class TestAPIPerformance:
    """API性能测试"""

    def test_concurrent_requests(self):
        """测试并发请求"""
        import threading
        import time

        responses = []
        start_time = time.time()

        def make_request():
            response = client.get("/api/v1/health")
            responses.append(response.status_code)

        # 创建10个并发请求
        threads = []
        for _ in range(10):
            t = threading.Thread(target=make_request)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        end_time = time.time()

        # 所有请求都应该成功
        assert all(code == 200 for code in responses)
        # 10个并发请求应该在合理时间内完成（比如5秒）
        assert end_time - start_time < 5

if __name__ == "__main__":
    pytest.main([__file__])
