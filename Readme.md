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
docker run -p 9000:80 --env DATABASE_URI=sqlite://data/data.db --name nav registry.cn-chengdu.aliyuncs.com/moxiaoying/nav:master 
```
### Docker-compose
```shell
version: '1.0.0'
services:
    nav:
        container_name: nav
        image: registry.cn-chengdu.aliyuncs.com/moxiaoying/nav:master
        environment:
        # 时区
        - TZ=Asia/Shanghai
        - DATABASE_URI=sqlite://data/data.db
        # - DATABASE_URI=mysql://myuser:mypass@db.host:3306/somedb
        # 映射配置文件
        ports:
            - "9000:80"
        restart: unless-stopped

```
> 默认账号:admin 密码:admin
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




