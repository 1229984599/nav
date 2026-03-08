# ============================================
# Stage 1: build frontend - Home
# ============================================
FROM node:20-alpine AS home-builder
WORKDIR /build
COPY home/package.json home/pnpm-lock.yaml ./
RUN corepack enable && corepack prepare pnpm@9 --activate \
    && pnpm install --frozen-lockfile
COPY home .
RUN pnpm build


# ============================================
# Stage 2: build frontend - Admin
# ============================================
FROM node:20-alpine AS admin-builder
WORKDIR /build
COPY admin/package.json admin/pnpm-lock.yaml admin/pnpm-workspace.yaml ./
COPY admin/packages ./packages
RUN corepack enable && corepack prepare pnpm@9 --activate \
    && pnpm install --frozen-lockfile
COPY admin .
ENV VITE_BASE_URL=/admin/
RUN pnpm build


# ============================================
# Stage 3: build Python dependencies via uv
# ============================================
FROM alpine:3.21 AS py-deps

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN apk add --no-cache \
    python3 python3-dev \
    gcc g++ musl-dev libffi-dev \
    libxml2-dev libxslt-dev \
    postgresql-dev mariadb-connector-c-dev

WORKDIR /deps
COPY api/pyproject.toml .

RUN uv pip install --no-cache --python=$(which python3) \
    --prefix=/deps/install \
    -r pyproject.toml \
    supervisor \
    -i https://pypi.tuna.tsinghua.edu.cn/simple


# ============================================
# Stage 4: runtime image (pure Alpine)
# ============================================
FROM alpine:3.21

LABEL maintainer="moxiaoying <768091671@qq.com>"

RUN apk add --no-cache \
    python3 \
    nginx \
    libxml2 libxslt \
    libpq mariadb-connector-c \
    tini tzdata \
    && mkdir -p /var/www/html /var/log/supervisor /run/nginx

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NGINX_PORT=80

COPY --from=py-deps /deps/install /usr

COPY --from=home-builder /build/dist /var/www/html/home
COPY --from=admin-builder /build/dist /var/www/html/admin

COPY api /app
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

COPY nginx.conf /etc/nginx/nginx.conf.template
COPY supervisord.conf /etc/supervisord.conf

EXPOSE 80

ENTRYPOINT ["tini", "--"]
CMD ["/usr/local/bin/docker-entrypoint.sh", "supervisord", "-c", "/etc/supervisord.conf"]
