# 阶段一：构建前端页面 - Home
FROM node:current-slim AS home-frontend-builder
WORKDIR /app/home
COPY home/package.json home/pnpm-lock.yaml /app/home/
RUN npm install -g pnpm
RUN pnpm install
COPY home /app/home
RUN pnpm build

# 阶段二：构建前端页面 - Admin
FROM node:current-slim AS admin-frontend-builder
WORKDIR /app/admin
COPY admin/package.json admin/pnpm-lock.yaml /app/admin/
RUN npm install -g pnpm
RUN pnpm install
COPY admin /app/admin
RUN pnpm build

# 阶段三：构建Nginx服务器
FROM moxiaoying/python-nginx:latest
WORKDIR /app
COPY api /app/api
RUN pip install -r /app/api/requirements.txt
COPY --from=home-frontend-builder /app/home/dist /usr/share/nginx/html/home
COPY --from=admin-frontend-builder /app/admin/dist /usr/share/nginx/html/admin
# 添加Nginx配置文件
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# 启动Nginx服务器和API
EXPOSE 80

CMD ["sh", "-c", "nginx -g 'daemon off;' & uvicorn api.run:app --host 0.0.0.0 --port 8000"]
#FROM moxiaoying/python-nginx:1.0.0
##WORKDIR /app
#COPY /admin /usr/share/nginx/html/admin
#COPY /home /usr/share/nginx/html/home
## 复制Nginx配置文件到镜像中
#COPY ./nginx.conf /etc/nginx/nginx.conf
##
## CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8010"]
## 暴露端口
#EXPOSE 80
## 启动 Nginx 和后端服务
# CMD ["sh", "-c", "nginx -g 'daemon off;'"]
