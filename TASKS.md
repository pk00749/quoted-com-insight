# 股票公告信息API服务 - 开发任务清单

## 项目概述
基于 FastAPI + AKShare 开发的股票公告信息API服务，专注于提供A股市场的公告数据查询和AI智能总结功能。

## 任务状态说明
- ✅ 已完成
- 🚧 进行中
- ❌ 待开发
- 🔄 需要重构

---

## 任务1: 获取股票公告列表API

**接口**: `GET /api/v1/announcements/{stock_code}`

### 📋 需求描述
- 获取单个股票过去10天的公告信息
- 使用 AKShare 的 `stock_notice_report` 接口
- 返回完整的公告对象列表（不获取正文内容）

### 🎯 期望功能
- 输入：股票代码（如：000001）
- 输出：公告基本信息列表（标题、类别、日期、链接等）
- 时间范围：过去10天
- 数据源：巨潮资讯网（通过AKShare）

### 📤 响应格式
```json
{
    "success": true,
    "data": {
        "announcements": [
            {
                "stock_code": "000001",
                "stock_name": "平安银行",
                "title": "关于召开2024年第三次临时股东大会的通知",
                "category": "临时股东大会",
                "publish_date": "2024-09-17",
                "url": "http://static.cninfo.com.cn/finalpage/..."
            }
        ],
        "total": 1,
        "page": 1,
        "size": 20
    },
    "message": "获取公告成功"
}
```

### 💻 技术实现要点
- 移除现有的 `date` 参数，改为自动获取过去10天
- 使用 `ak.stock_notice_report(symbol='全部', date=日期)` 并按股票代码筛选
- 循环获取过去10天的数��并合并
- **仅返回公告基本信息，不获取URL正文内容**

### ⚠️ 注意事项
- 需要处理AKShare接口可能的异常
- 某些日期可能没有公告数据
- 需要去重处理相同的公告

### 📊 当前状态
✅ **已完成** - 已支持自动获取过去10天公告数据，去重处理，异常处理已实现

---

## 任务2: AI智能总结公告API

**接口**: `POST /api/v1/announcements/summarize`

### 📋 需求描述
- 基于股票代码获取过去10天的公告数据
- **访问每个公告的URL链接，获取正文内容**
- 使用百炼大模型 Qwen3 对每个公告进行智能总结
- 将所有公告的总结再次汇总为最终的 content

### 🎯 期望功能
- 输入：股票代码
- 处理流程：
  1. 调用任务1接口获取公告列表
  2. **逐个访问每个公告的URL，解析获取正文内容**
  3. 对每个公告正文调用LLM总结成一句话
  4. 将所有单句总结再次调用LLM汇总为最终content（500字内）

### 📤 响应格式
```json
{
    "success": true,
    "data": {
        "summary": "【AI总结功能预留】针对股票：000001的公告总结",
        "content": "基于该股票过去10天的公告内容深度分析：公告1总结句+公告2总结句+...，综合分析得出最终投资观点和关键信息汇总。",
        "word_count": 485,
        "model_info": {
            "model": "qwen3",
            "provider": "百炼大模型",
            "status": "接口预留"
        }
    },
    "message": "AI总结完成（当前为预留接口）"
}
```

### 💻 技术实现要点
- **与任务1的关键区别**：需要访问URL链接并获取网页正文内容
- 调用任务1的接口获取公告列表
- **网页内容获取与解析** - 推荐技术方案：
  
  **方案1: requests + beautifulsoup4 - 基础方案** ✅
  ```python
  import requests
  from bs4 import BeautifulSoup
  
  def extract_web_content(url: str) -> str:
      response = requests.get(url, timeout=30)
      soup = BeautifulSoup(response.content, 'html.parser')
      # 移除脚本和样式标签
      for script in soup(["script", "style"]):
          script.decompose()
      return soup.get_text(strip=True)
  ```
  - **优势**: 简单易用、社区支持好
  - **适用**: 大部分普通网页
  
  **方案2: httpx + selectolax - 高性能方案** ⭐ 推荐
  ```python
  import httpx
  from selectolax.parser import HTMLParser
  
  async def extract_web_content(url: str) -> str:
      async with httpx.AsyncClient() as client:
          response = await client.get(url, timeout=30)
          tree = HTMLParser(response.text)
          # 移除不需要的元素
          for tag in tree.css('script, style, nav, header, footer'):
              tag.decompose()
          return tree.body.text(strip=True) if tree.body else ""
  ```
  - **优势**: 异步支持、解析速度快5-10倍、内存效率高
  - **适用**: 高并发场景、大量URL处理
  
  **方案3: playwright - 重量级方案**
  ```python
  from playwright.async_api import async_playwright
  
  async def extract_web_content(url: str) -> str:
      async with async_playwright() as p:
          browser = await p.chromium.launch()
          page = await browser.new_page()
          await page.goto(url)
          content = await page.inner_text('body')
          await browser.close()
          return content
  ```
  - **优势**: 处理JavaScript渲染、反爬虫能力强
  - **适用**: 复杂SPA页面、有反爬虫机制的网站
  - **缺点**: 资源消耗大、启动慢
  
  **推荐组合方案**:
  ```python
  import httpx
  from selectolax.parser import HTMLParser
  import requests
  from bs4 import BeautifulSoup
  
  async def extract_announcement_content(self, url: str) -> str:
      try:
          # 首选：httpx + selectolax (高性能异步)
          async with httpx.AsyncClient(timeout=30) as client:
              response = await client.get(url)
              tree = HTMLParser(response.text)
              
              # 尝试提取主要内容区域
              content_selectors = [
                  '.content', '.article-content', '.main-content',
                  '#content', 'main', 'article', '.post-content'
              ]
              
              for selector in content_selectors:
                  content_node = tree.css_first(selector)
                  if content_node:
                      return content_node.text(strip=True)
              
              # 退化到全文提取
              for tag in tree.css('script, style, nav, header, footer'):
                  tag.decompose()
              return tree.body.text(strip=True) if tree.body else ""
              
      except Exception as e:
          # 备选方案：requests + beautifulsoup (兼容性好)
          try:
              response = requests.get(url, timeout=30)
              soup = BeautifulSoup(response.content, 'html.parser')
              
              # 尝试提取主要内容
              content_tags = soup.find(['div', 'article', 'main'], 
                                     class_=['content', 'article-content', 'main-content'])
              if content_tags:
                  return content_tags.get_text(strip=True)
              
              # 清理不需要的标签
              for script in soup(["script", "style", "nav", "header", "footer"]):
                  script.decompose()
              return soup.get_text(strip=True)
              
          except Exception as e2:
              logger.error(f"网页内容提取失败: {url}, 错误: {str(e2)}")
              return ""
  ```

- **分层LLM调用**：
  1. 第一层：每个公告网页正文 → LLM → 单句总结
  2. 第二层：所有单句总结 → LLM → 最终content（500字内）
- 集成百炼大模型API（待实现）

### 🔄 处理流程详解
```
股票代码 → 任务1接口 → 公告列表[{title, url, ...}]
    ↓
遍历每个公告URL → 访问网页 → 解析HTML提取正文 → LLM总结 → 单句摘要
    ↓
收集所有单句摘要 → 再次调用LLM → 最终content总结
```

### ⚠️ 注意事项
- **网页内容获取的技术挑战**：
  - **推荐使用httpx + selectolax**: 异步高性能，解析速度快
  - **备选requests + beautifulsoup**: 兼容性好，社区支持完善
  - **重量级playwright**: 仅在遇到JavaScript渲染或反爬虫时使用
  - 网页访问超时控制（建议30秒）
  - User-Agent设置避免被反爬虫拦截
  - 请求频率控制，避免给目标服务器造成压力
  - 处理各种HTTP状态码和异常情况
- **内容提取优化**：
  - 智能识别主要内容区域（避免导航、广告等噪音）
  - 文本清理：去除多余空格、换行符
  - 长文本截取：LLM输入Token限制处理
- **LLM调用优化**：
  - 批量调用 vs 逐个调用的性能权衡
  - Token消耗控制（网页文本可能很长，需要截取关键部分）
  - 调用失败的降级处理
- **内容质量控制**：
  - 网页文本提取质量检查（去除HTML标签、格式化）
  - 单句总结的质量检查
  - 最终总结的逻辑性和连贯性

### 📦 新增依赖包
需要在 `requirements.txt` 中添加：
```
# 推荐方案
httpx>=0.25.0          # 高性能异步HTTP客户端
selectolax>=0.3.17     # 快速HTML解析器

# 备选方案  
requests>=2.31.0       # HTTP请求库（已有）
beautifulsoup4>=4.12.0 # HTML解析库
lxml>=4.9.0           # beautifulsoup的高性能解析器

# 重量级方案（按需）
playwright>=1.40.0     # 浏览器自动化（处理JS渲染）
```
