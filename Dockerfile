# ============================================
# 阶段一：构建前端页面 - Home
# ============================================
FROM node:20-alpine AS home-builder
WORKDIR /build
COPY home/package.json home/pnpm-lock.yaml ./
RUN corepack enable && corepack prepare pnpm@latest --activate \
    && pnpm install --frozen-lockfile
COPY home .
RUN pnpm build


# ============================================
# 阶段二：构建前端页面 - Admin
# ============================================
FROM node:20-alpine AS admin-builder
WORKDIR /build
COPY admin/package.json admin/pnpm-lock.yaml admin/pnpm-workspace.yaml ./
COPY admin/packages ./packages
RUN corepack enable && corepack prepare pnpm@latest --activate \
    && pnpm install --frozen-lockfile
COPY admin .
RUN pnpm build


# ============================================
# 阶段三：使用 uv 编译 Python 依赖
# ============================================
FROM alpine:3.21 AS py-deps

# 从官方镜像复制 uv 二进制
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 安装编译工具链
RUN apk add --no-cache \
    python3 python3-dev \
    gcc g++ musl-dev libffi-dev \
    libxml2-dev libxslt-dev \
    postgresql-dev mariadb-connector-c-dev

WORKDIR /deps
COPY api/pyproject.toml .

# uv 安装依赖到独立目录，编译工具链不进入最终镜像
RUN uv pip install --no-cache --python=$(which python3) \
    --prefix=/deps/install \
    -r pyproject.toml \
    supervisor \
    -i https://pypi.tuna.tsinghua.edu.cn/simple


# ============================================
# 阶段四：最终运行镜像 (纯 Alpine)
# ============================================
FROM alpine:3.21

LABEL maintainer="moxiaoying <768091671@qq.com>"

# 安装最小运行时依赖
RUN apk add --no-cache \
    python3 \
    nginx \
    libxml2 libxslt \
    libpq mariadb-connector-c \
    tini tzdata \
    && mkdir -p /var/www/html /var/log/supervisor /run/nginx

WORKDIR /app

# 复制 Python 依赖（编译工具链不进入最终镜像）
COPY --from=py-deps /deps/install /usr

# 复制前端构建产物
COPY --from=home-builder /build/dist /var/www/html/home
COPY --from=admin-builder /build/dist /var/www/html/admin

# 复制后端代码
COPY api /app

# 复制配置文件
COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisord.conf /etc/supervisord.conf

EXPOSE 80

# tini (PID 1): 信号转发 + 僵尸进程回收
# supervisord: nginx + uvicorn 双进程守护，崩溃自动重启
ENTRYPOINT ["tini", "--"]
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
