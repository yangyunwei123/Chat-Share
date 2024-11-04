## 项目介绍  
基于原项目地址https://github.com/Bear-biscuit/OAIFree_Share修改而来

基于LQ的chat2api项目，搭建一个共享站，方便给自己的小伙伴们使用  
项目地址https://github.com/lanqian528/chat2api

## 配置项  
在docker-compose.yml中配置三个环境变量

```
secret_key最好复杂一点  
authorization应当和chat2api的环境变量authorization设置的值相同  
domain_chatgpt是chat2api的站点地址，需要替换成自己的项目地址  
```

### 直接部署

```bash
git clone https://github.com/h88782481/chat-share
cd chat-share
pip install -r requirements.txt
python app.py
```

### Docker 部署

您需要安装 Docker 和 Docker Compose。

```bash
docker run -d \
  --name chat-share \
  -p 5100:5100 \
  -e SECRET_KEY=your_admin_secret_key \
  -e AUTHORIZATION=your_authorization \
  -e DOMAIN_CHATGPT=http://127.0.0.1:5005 \
  ghcr.io/h88782481/chat-share:latest
```

### (推荐) Docker Compose 部署

创建一个新的目录，例如 chat-share，并进入该目录：

```bash
mkdir chat-share
cd chat-share
```

在此目录中下载库中的 docker-compose.yml 文件：

```bash
wget https://raw.githubusercontent.com/h88782481/Chat-Share/main/docker-compose.yml
```

修改 docker-compose-warp.yml 文件中的环境变量，保存后：

```bash
docker-compose up -d
```

## 页面预览  

### 登录页  
默认管理员账户
```
账号：admin
密码：password
```
请登录后在用户管理中更改用户名和密码 

![image](https://github.com/user-attachments/assets/2541f8d0-eb76-42fb-8ec7-24199fc93372)


## License

MIT License
