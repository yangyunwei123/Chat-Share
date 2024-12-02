from app import app
from flask import render_template, request, redirect, url_for, session, flash
import utils.globals as globals
from utils.globals import *
from utils.tools import *
from werkzeug.security import check_password_hash
from gateway.index import *


# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        loginTarget = request.form['login_target']
        user = next((user for user in globals.users if user['username'] == username), None)
        
        if user and check_password_hash(user['password'], password):
            # 登录成功，存储用户信息到session
            session['logged_in'] = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            flash('登录成功！', 'success')
            
            # 如果是管理员，跳转到管理页面，否则跳转到ChatGPT共享页面
            if user['role'] == 'admin' and loginTarget == 'manage':
                return redirect(url_for('chatgpt'))
            elif user['role'] == 'user' and loginTarget == 'manage':
                flash('你没有管理员权限。', 'danger')
            elif loginTarget == 'gpt':
                logurl = getoauth(session.get('user_id'))
                session.clear()
                return redirect(logurl)
            elif loginTarget == 'claude':
                logurl = get_claude_login_url(user['bind_claude_token'],session.get('user_id'))
                if logurl == None:
                    flash('你没有此权限。', 'danger')
                else:
                    session.clear()
                    return redirect(logurl)
        else:
            flash('用户名或密码错误，请重试。', 'danger')
    
    return render_template('login.html')

# 登出路由
@app.route('/logout')
def logout():
    session.clear()
    flash('已成功登出。', 'success')
    return redirect(url_for('login'))


