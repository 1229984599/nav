FROM moxiaoying/python-nginx:1.0.0
#WORKDIR /app
COPY /admin /usr/share/nginx/html/admin
COPY /home /usr/share/nginx/html/home
# 复制Nginx配置文件到镜像中
COPY ./nginx.conf /etc/nginx/nginx.conf
#
# CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8010"]
# 暴露端口
EXPOSE 80
# 启动 Nginx 和后端服务
 CMD ["sh", "-c", "nginx -g 'daemon off;'"]
