from app import app
from flask import redirect, url_for, session
from utils.globals import *
from utils.tools import *



# 主页路由
@app.route('/')
@login_required
def index():
    
    if session.get('logged_in'):
        if session.get('role') == 'user':
            # 获取 OAuth 登录 URL
            logurl = getoauth(session.get('user_id'))
            session.clear()
            return redirect(logurl)
        else:
            return redirect(url_for('chatgpt'))  
    
    return redirect(url_for('login'))



