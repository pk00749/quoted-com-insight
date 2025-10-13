# 使用Python 3.12官方镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 环境变量：Python、时区、中文本地化、Playwright浏览器路径
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Shanghai \
    LANG=zh_CN.UTF-8 \
    LC_ALL=zh_CN.UTF-8 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# 安装系统依赖：
# - curl: 健康检查
# - locales/tzdata: 本地化与时区
# - fonts-noto-cjk: 中文字体
# - Playwright 运行依赖（Chromium 所需库）
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
    locales tzdata \
    fonts-noto-cjk \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
    libasound2 libpangocairo-1.0-0 libpango-1.0-0 libcairo2 libatspi2.0-0 libgtk-3-0 libdrm2 libxkbcommon0 \
    libxshmfence1 libxfixes3 libxext6 libxi6 libxtst6 libglib2.0-0 libx11-6 libx11-xcb1 libxcb1 libxss1 \
    && rm -rf /var/lib/apt/lists/*

# 生成中文本地化
RUN sed -i 's/# zh_CN.UTF-8 UTF-8/zh_CN.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

# 复制并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 预安装 Playwright 浏览器与系统依赖（Chromium），并准备浏览器缓存目录
RUN python -m playwright install --with-deps chromium && \
    mkdir -p /ms-playwright

# 复制应用代码
COPY app/ ./app/

# 创建非root用户并赋权（确保Playwright浏览器与应用目录可写）
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app /ms-playwright
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查（依赖 curl）
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# 启动命令
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
