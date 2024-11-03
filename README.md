## 项目介绍  
原项目地址https://github.com/Bear-biscuit/OAIFree_Share

基于LG的chat2api项目，搭建一个共享站，方便给自己的小伙伴们使用  

## 配置项  
### config.json
secret_key最好复杂一点  
authorization应当和chat2api的环境变量authorization设置的值相同
domain_chatgpt是chat2api的站点地址，需要替换成自己的项目地址  
```
{
    "secret_key":"your_admin_secret_key",
    "authorization":"your_authorization",
    "domain_chatgpt":"http://127.0.0.1:5005",  注意地址最后不要加/
}
```
## 页面预览  

### 登录页  
默认管理员账户
```
账号：admin
密码：password
```
请登录后在用户管理中更改用户名和密码  

## Linux部署 

###  更新服务器并安装依赖
首先更新系统并安装一些必要的工具：

```
sudo apt update
sudo apt upgrade -y
```
### 安装 Python 及其依赖
安装 Python3 和 pip： 确保系统中安装了 Python3 和 pip（Python 的包管理工具）

```
sudo apt install python3 python3-pip python3-venv -y
```
### 设置虚拟环境
创建虚拟环境： 为了避免与系统的 Python 环境冲突，建议使用虚拟环境

```
python3 -m venv venv
```
激活虚拟环境：

```
source venv/bin/activate
```
### 安装 Flask 和项目依赖
```
pip install flask requests werkzeug gunicorn
```

### 运行 Flask 应用程序
使用 gunicorn 来运行
```
gunicorn -w 1 -b 0.0.0.0:8000 app:app
```
-w 1：使用 1 个 worker 进程
-b 0.0.0.0:8000：监听所有接口上的 8000 端口

## 测试应用
打开浏览器，访问 http://127.0.0.1:8000 或  http://your-ip:8000 ，如果一切顺利，你应该就可以看到登录页了

## Windows部署  

## 安装 Python
访问 [Python](https://www.python.org/downloads/) 官方网站，下载适合你系统的 Python安装包
安装时勾选 “Add Python to PATH” 选项，以便全局使用 python 命令
验证 Python 安装： 打开 命令提示符 (Command Prompt)，输入：

```
python --version
```
确保显示的是 Python 3.x 版本

## 安装 pip
pip 通常会与 Python 一起安装，确保安装后可用：

```
pip --version
```
如果 pip 没有安装，可以通过以下命令安装：

```
python -m ensurepip --upgrade
```

## 设置 Python 虚拟环境
创建虚拟环境： 在项目目录中，运行以下命令创建虚拟环境：

```
python -m venv venv
```
激活虚拟环境： 
```
venv\Scripts\activate
```
激活后，你的命令提示符前面应该会显示 (venv)。

### 安装 Flask 和项目依赖
```
pip install flask requests werkzeug waitress
```
### 运行 Flask 应用程序
使用 Waitress 运行 Flask 应用：

```
waitress-serve --listen=0.0.0.0:8000 app:app
```
参数说明：

--listen=0.0.0.0:8000：让 Waitress 监听所有网络接口上的端口 8000。

## 测试应用
打开浏览器，访问 http://127.0.0.1:8000 或  http://your-ip:8000 ，如果一切顺利，你应该就可以看到登录页了
