import json
import requests
from flask import redirect, url_for, session, flash
from functools import wraps
import utils.configs as configs
import utils.globals as globals
from utils.globals import *
from utils.tools import *


# 刷新 access_token 的主函数
def refresh_access_tokens():
    globals.failed_tokens = []
    # 遍历 refresh_token 列表
    for token_info in globals.chatToken:
        email = token_info['email']
        refresh_token = token_info['refresh_token']

        # 如果 refresh_token 为空，跳过这一行
        if not refresh_token:
            continue

        try:
            
            # 使用 POST 请求通过 refresh_token 获取 access_token
            url = "https://auth0.openai.com/oauth/token"
            headers = {"Content-Type": "application/json"}
            data = {
                "redirect_uri": "com.openai.chat://auth0.openai.com/ios/com.openai.chat/callback",
                "grant_type": "refresh_token",
                "client_id": "pdlLIX2Y72MIl2rhLhTE9VV9bN905kBh",
                "refresh_token": refresh_token
            }
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response_data = response.json()

            access_token = response_data.get("access_token")
            if access_token:  # 如果成功获取到 access_token
                # 更新 access_token 和状态为 True
                for i, user in enumerate(globals.users):
                    if user['bind_email'] == email:
                        globals.users[i]['bind_token'] = access_token
                        set_seedmap(globals.users[i]['id'],access_token)
                save_users(globals.users)
                token_info['access_token'] = access_token
                token_info['status'] = True
            else:
                # 如果获取失败，设置状态为 False
                token_info['status'] = False
                globals.failed_tokens.append(token_info)
        
        except Exception as e:
            # 捕获请求错误并记录失败的 token，状态为 False
            token_info['status'] = False
            globals.failed_tokens.append(token_info)

    # 保存更新后的 retoken 数据
    save_retoken(globals.chatToken)

    # 如果有失败的 token，记录到 failed_tokens.json
    save_failed_tokens(globals.failed_tokens)

    return globals.chatToken



# 获取登陆链接
def getoauth(seed_token):
    domain = configs.domain_chatgpt
    
    url = f'{domain}/?token={seed_token}'
    try:
        return url
    except requests.RequestException as e:
        return None

# 验证是否登录的装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('请先登录。', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 验证是否为管理员的装饰器
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('请先登录。', 'warning')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('需要管理员权限。', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# 设置网关seedmap
def set_seedmap(user_id,token):
    
    domain = configs.domain_chatgpt
    
    url = f'{domain}/seedtoken'
    headers = {
        "Authorization": f"Bearer {configs.authorization}",
        "Content-Type": "application/json"
    }
    data = {
        "seed": user_id,
        "token": token,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.status_code


# 删除网关seedmap
def del_seedmap(user_id):
    
    domain = configs.domain_chatgpt
    
    url = f'{domain}/seedtoken'
    headers = {
        "Authorization": f"Bearer {configs.authorization}",
        "Content-Type": "application/json"
    }
    data = {
        "seed": user_id
    }
    response = requests.delete(url, headers=headers, data=json.dumps(data))
    return response.status_code