from app import app
from flask import redirect, url_for, session
from utils.globals import *
from utils.tools import *



# 主页路由
@app.route('/')
@login_required
def index():
    
    if session.get('logged_in'):
        session.clear()
    return redirect(url_for('login'))
