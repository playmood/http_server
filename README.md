just for graduation project.

# 运行环境
- Ubuntu 16.04
- MySQL 5.7.32

# 建库创表添数据
```
// 建立yourdb库
create database yourdb;

// 创建user表
USE yourdb;
CREATE TABLE user(
    username char(50) NULL,
    passwd char(50) NULL
)ENGINE=InnoDB;

// 添加数据
INSERT INTO user(username, passwd) VALUES('name', 'passwd');
```
# 初始化工作
- 修改main.c中数据库信息
```
// 修改服务器数据库的登录名和密码
// 修改上述创建的yourdb库名
connPool->init("localhost", "root", "root", "yourdb", 3306, 8);
```
- 修改http_conn.cpp中的root路径
```
// 修改为root文件夹所在路径
const char* doc_root="/home/playmood/http_server/root";
```
- make生成server
```
make server
```
- 在指定端口运行server
```
./server port
```
- 浏览器端访问ip:port即可