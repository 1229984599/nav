## 哈哈导航
### 开发目的
看上了一为导航的界面，但是需要收费（还不便宜）。六零导航也很喜欢，不过作者目前不打算更新二级菜单和页面描述功能，所有就自己搞一个了。

### Docker部署
> DATABASE_URI为数据库配置

#### DATABASE_URI配置参考
sqlite: `sqlite://data/data.db`

postgres: `psycopg://postgres:pass@db.host:5432/somedb`

mysql: `mysql://myuser:mypass@db.host:3306/somedb`


```shell
docker run -e NGINX_PORT=${NGINX_PORT:-80} -p ${NAV_PORT:-9000}:${NGINX_PORT:-80} --env DATABASE_URI=sqlite://data/data.db --name nav ghcr.io/1229984599/nav:latest
```
> `NGINX_PORT` support requires an image built from this source (or a released image tag that contains this feature).
### Docker-compose
```shell
services:
  nav:
    container_name: nav
    image: ghcr.io/1229984599/nav:latest
    environment:
      - TZ=Asia/Shanghai
      - NGINX_PORT=${NAV_CONTAINER_PORT:-80}
      # 数据库配置（三选一）
      # SQLite（默认）
      - DATABASE_URI=sqlite:///app/data/data.db
      # MySQL
      # - DATABASE_URI=mysql://user:password@db-host:3306/nav
      # PostgreSQL
      # - DATABASE_URI=postgres://user:password@db-host:5432/nav
    ports:
      - "${NAV_PORT:-9000}:${NAV_CONTAINER_PORT:-80}"
    volumes:
      - ./data:/app/data
    restart: unless-stopped


```
> 默认账号:admin 密码:admina
### 项目截图
#### 前端页面
![img.png](img/home.png)
#### 移动端
![img.png](img/mobile.png)
#### 后台页面
![img.png](img/admin.png)
#### 前后端添加链接时都支持自动爬取网站信息
> 注意：后面颜色选择只对图标起作用

![img.png](img/addLink.png)




