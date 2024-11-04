from app import app
from flask import render_template, request, jsonify
import utils.globals as globals
from utils.globals import *
from utils.tools import *






# GPT 主页路由
@app.route('/chatgpt', methods=['GET', 'POST'])
@admin_required
def chatgpt():

    if request.method == 'GET':
        # 加载并显示 chatToken.json 文件中的内容
        return render_template('GPT.html', retokens=globals.chatToken)

    if request.method == 'POST':
        # 获取更新后的 retoken 数据
        globals.chatToken = request.json.get('retokens')
        
        # 如果数据格式有效，保存到文件
        if globals.chatToken:
            save_retoken(globals.chatToken)
            return jsonify({"status": "success", "message": "chatToken.json 已更新！"}), 200
        else:
            return jsonify({"status": "error", "message": "无效的数据格式！"}), 400