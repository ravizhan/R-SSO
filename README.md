# R-SSO 单点登陆系统

![](https://img.shields.io/github/license/ravizhan/R-SSO?style=for-the-badge)
![](https://img.shields.io/github/forks/ravizhan/R-SSO?style=for-the-badge)
![](https://img.shields.io/github/stars/ravizhan/R-SSO?style=for-the-badge)
![](https://img.shields.io/github/languages/top/ravizhan/R-SSO?style=for-the-badge)
![](https://img.shields.io/github/languages/count/ravizhan/R-SSO?style=for-the-badge)
![](https://img.shields.io/github/commit-activity/m/ravizhan/R-SSO?style=for-the-badge)


# WHAT 这是什么(介绍)
这是基于python FastApi框架开发的一款**单点登录**系统。

可以帮助你方便快捷地搭建一套属于自己的SSO。
# WHY 为什么用(优势)
- 集合了目前主流的验证方式:`OAuth2`, ~~`OIDC`~~
- 持续的更新(摸鱼)
- 完善的文档
- 友好的界面
# HOW 怎么用(用法)

## 搭建

### 数据库
将`sql`文件夹下的表结构文件导入到MySql数据库中

### 后端
首先下载本仓库,并安装好相关依赖.
```
git clone https://github.com/ravizhan/R-SSO
cd R-SSO
pip3 install -r ./requerement.txt
```

编辑 `config.yaml` ,对照注释 修改配置,并保存.

最后启动即可
```
python3 ./main.py
```

### 前端
将static文件夹下所有文件,放入您的网站根目录中.

编辑网站配置文件,加入反向代理配置(以Nginx为例)
```
location /api/
{
    proxy_pass http://127.0.0.1:8000/api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header REMOTE-HOST $remote_addr;
}
```
保存并重启/重载Nginx
## 接入

流程图👇
![流程图](https://files.wanpoo.top/webstatic/f68f8b76337b5/未命名文件.svg)

> 未完待续

# 声明
本程序使用**GPLv3协议**授权, 请自觉遵守.

本人不赞成也不会对其进行商业化, **商用的将不会提供技术支持**.