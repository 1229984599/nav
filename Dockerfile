# 阶段一：构建前端页面 - Home
FROM node:slim AS home-frontend-builder
WORKDIR /app/home
COPY home /app/home
RUN npm install -g pnpm && pnpm install && pnpm build


# 阶段二：构建前端页面 - Admin
FROM node:slim AS admin-frontend-builder
WORKDIR /app/admin
COPY admin /app/admin
RUN npm install -g pnpm && pnpm install && pnpm build


# 阶段三：构建Nginx服务器
FROM moxiaoying/python-nginx:1.0.0
WORKDIR /app
COPY --from=home-frontend-builder /app/home/dist /var/www/html/home
COPY --from=admin-frontend-builder /app/admin/dist /var/www/html/admin
COPY api /app
RUN pip install -r /app/requirements.txt -i https://pypi.org/simple

# 添加Nginx配置文件
COPY ./nginx.conf /etc/nginx/nginx.conf

# 启动Nginx服务器和API
EXPOSE 80

CMD ["sh", "-c", "nginx -g 'daemon off;' & uvicorn main:app --host 0.0.0.0 --port 8000"]
