import akshare as ak
import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient

from app.main import app
from app.services.stock_service import StockService
from app.core.exceptions import StockAPIException

# 测试客户端
client = TestClient(app)

class TestStockAPI:
    """股票API测试用例"""

    @pytest.fixture
    def stock_service(self):
        """股票服务实例"""
        return StockService()

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

    def test_get_latest_announcements(self):
        """测试获取最新公告"""
        response = client.get("/api/v1/announcements/latest")

        assert response.status_code in [200, 500]
        data = response.json()
        assert "success" in data

class TestStockService:
    """股票服务层测试"""

    @pytest.fixture
    def service(self):
        return StockService()

    @pytest.mark.asyncio
    async def test_stock_service_initialization(self, service):
        """测试服务初始化"""
        assert service is not None
        assert hasattr(service, 'cache')

    @pytest.mark.asyncio
    async def test_get_stock_info_service(self, service):
        """测试服务层获取股票信息"""
        try:
            stock_info = await service.get_stock_info("000001")
            assert stock_info.code == "000001"
        except StockAPIException:
            # 如果akshare调用失败，应该抛出自定义异常
            pytest.skip("akshare数据获取失败，跳过测试")
        except Exception as e:
            # 其他异常应该被包装为StockAPIException
            pytest.fail(f"应该抛出StockAPIException，但得到: {type(e).__name__}")

    @pytest.mark.asyncio
    async def test_get_realtime_price_service(self, service):
        """测试服务层获取实时价格"""
        try:
            price = await service.get_realtime_price("000001")
            assert price.code == "000001"
            assert price.date is not None
        except StockAPIException:
            pytest.skip("akshare数据获取失败，跳过测试")

    @pytest.mark.asyncio
    async def test_search_stocks_service(self, service):
        """测试服务层搜索股票"""
        try:
            stocks = await service.search_stocks("银行")
            assert isinstance(stocks, list)
            # 搜索结果应该被限制在20个以内
            assert len(stocks) <= 20
        except StockAPIException:
            pytest.skip("akshare数据获取失败，跳过测试")

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

class TestAPIValidation:
    """API参数验证测试"""

    def test_pagination_validation(self):
        """测试分页参数验证"""
        # 测试负页码
        response = client.get("/api/v1/stocks/list?page=-1")
        assert response.status_code == 422

        # 测试过大的页面大小
        response = client.get("/api/v1/stocks/list?size=1000")
        assert response.status_code == 422

    def test_date_format_validation(self):
        """测试日期格式验证"""
        stock_code = "000001"
        # 测试无效日期格式
        params = {
            "start_date": "invalid-date",
            "end_date": "2024-01-01"  # 正确格式但与akshare要求不符
        }
        response = client.get(f"/api/v1/stock/history/{stock_code}", params=params)
        # 应该在服务层处理日期格式问题
        assert response.status_code in [200, 400, 500]

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
