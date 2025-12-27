# 使用轻量级 Python 基础镜像（锁定 bookworm 以避免 t64 混用）
FROM python:3.11-slim-bookworm AS base

ARG DEBIAN_FRONTEND=noninteractive
ARG DEBIAN_MIRROR=mirrors.aliyun.com

ENV TZ=Asia/Shanghai \
    LANG=zh_CN.UTF-8 \
    LC_ALL=zh_CN.UTF-8 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright \
    PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple \
    PIP_TIMEOUT=60

RUN set -eux; \
        if [ -f /etc/apt/sources.list ]; then \
            sed -i "s@deb.debian.org@${DEBIAN_MIRROR}@g" /etc/apt/sources.list; \
            sed -i "s@security.debian.org@${DEBIAN_MIRROR}@g" /etc/apt/sources.list; \
        else \
            printf 'deb http://%s/debian bookworm main contrib non-free non-free-firmware\n' "${DEBIAN_MIRROR}" > /etc/apt/sources.list; \
            printf 'deb http://%s/debian bookworm-updates main contrib non-free non-free-firmware\n' "${DEBIAN_MIRROR}" >> /etc/apt/sources.list; \
            printf 'deb http://%s/debian-security bookworm-security main contrib non-free non-free-firmware\n' "${DEBIAN_MIRROR}" >> /etc/apt/sources.list; \
        fi; \
        if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
            sed -i "s@deb.debian.org@${DEBIAN_MIRROR}@g" /etc/apt/sources.list.d/debian.sources; \
            sed -i "s@security.debian.org@${DEBIAN_MIRROR}@g" /etc/apt/sources.list.d/debian.sources; \
        fi; \
        apt-get update; \
    apt-get install -y --no-install-recommends \
        ca-certificates curl \
        locales tzdata \
        libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
        libasound2 libpangocairo-1.0-0 libpango-1.0-0 libcairo2 libatspi2.0-0 libgtk-3-0 libdrm2 libxkbcommon0 \
        libxshmfence1 libxfixes3 libxext6 libxi6 libxtst6 libglib2.0-0 libx11-6 libx11-xcb1 libxcb1 libxss1 \
        sqlite3 \
    ; \
    rm -rf /var/lib/apt/lists/*; \
    sed -i 's/# zh_CN.UTF-8 UTF-8/zh_CN.UTF-8 UTF-8/' /etc/locale.gen; \
    locale-gen

# ------- Builder stage -------
FROM base AS builder
WORKDIR /app

# 创建并激活虚拟环境（避免 PEP 668 系统级 pip 限制）
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 安装 Python 依赖与浏览器
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    set -eux; \
    pip install --no-cache-dir --only-binary=:all: --no-binary=jsonpath -r requirements.txt; \
    python -m playwright install chromium

# 复制应用代码
COPY app/ ./app/

# ------- Runtime stage -------
FROM base AS runtime
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 创建非root用户（提前创建以便 COPY --chown 使用）
RUN useradd -m -s /bin/bash appuser && \
    chown appuser:appuser /app

# Copy venv and browsers from builder
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder --chown=appuser:appuser /ms-playwright /ms-playwright
# 仅为应用目录设置归属，避免对庞大的浏览器目录进行递归 chown
COPY --from=builder --chown=appuser:appuser /app/app /app/app

USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查（依赖 curl）
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# 启动命令
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
