# 使用 Ubuntu 24.04 作为基础镜像，仅支持 Ubuntu
FROM ubuntu:24.04

# 设置工作目录
WORKDIR /app

# 环境变量：非交互安装、时区、中文本地化、Playwright 与 PIP 国内加速
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Shanghai \
    LANG=zh_CN.UTF-8 \
    LC_ALL=zh_CN.UTF-8 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright \
    PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple \
    PIP_TIMEOUT=60

# 配置国内 Ubuntu APT 镜像（默认清华镜像，可通过 --build-arg UBUNTU_MIRROR_HOST=xxx 覆盖）
ARG UBUNTU_MIRROR_HOST=mirrors.tuna.tsinghua.edu.cn

RUN set -eux \
    && sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        curl ca-certificates \
        locales tzdata \
        fonts-noto-cjk \
        python3 python3-pip python3-venv \
        libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
        libasound2t64 libpangocairo-1.0-0 libpango-1.0-0 libcairo2 libatspi2.0-0 libgtk-3-0 libdrm2 libxkbcommon0 \
        libxshmfence1 libxfixes3 libxext6 libxi6 libxtst6 libglib2.0-0 libx11-6 libx11-xcb1 libxcb1 libxss1 \
    && rm -rf /var/lib/apt/lists/*

# 创建并激活虚拟环境（避免 PEP 668 系统级 pip 限制）
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 复制并安装Python依赖（预下载 wheels 离线安装，prefer-binary；在 venv 中执行）
COPY requirements.txt .
RUN set -eux \
    && pip install -r requirements.txt \
    && python -m playwright install chromium \
    && mkdir -p /ms-playwright \
    && sed -i 's/# zh_CN.UTF-8 UTF-8/zh_CN.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen

# 复制应用代码
COPY app/ ./app/

# 创建非root用户并赋权（确保Playwright浏览器与应用目录可写）
RUN useradd -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app /ms-playwright
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查（依赖 curl）
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# 启动命令
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
