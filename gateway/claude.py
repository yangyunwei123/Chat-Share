from app import app
import json
from flask import request, jsonify
import utils.globals as globals
from utils.globals import *
from utils.tools import *

# 加载Claude Token
@app.route('/get_Claude')
@admin_required
def get_Claude():
    try:
        return jsonify(globals.cluadeToken), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in tokens.json"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 添加新账号
@app.route('/api/Claude', methods=['POST'])
@admin_required
def create_Claude():
    data = request.get_json()
    
    # 检查账号是否已存在
    if any(token['email'] == data['email'] for token in globals.cluadeToken):
        return jsonify({'success': False, 'message': '该账号已存在'}), 400
    
    new_token = {
        'email': data['email'],
        'skToken': data['SkToken'],
        'status': True,
        'type':"/static/claude.png",
        'PLUS': data['PLUS']
    }
    
    globals.cluadeToken.append(new_token)
    save_cltoken(globals.cluadeToken)
    
    return jsonify({'success': True, 'message': '用户创建成功'})

# 更新账号信息
@app.route('/api/Claude/<email>', methods=['PUT'])
@admin_required
def update_Claude(email):
    data = request.get_json()
    
    token_index = next((i for i, token in enumerate(globals.cluadeToken) if token['email'] == email), None)
    if token_index is None:
        return jsonify({'success': False, 'message': '账号不存在'}), 400

    
    # 如果提供了邮箱，则更新邮箱
    if data.get('email'):
        globals.cluadeToken[token_index]['email'] = data['email']
    
    # 如果提供了ReToken，则更新ReToken
    if data.get('SkToken'):
        globals.cluadeToken[token_index]['skToken'] = data['SkToken']
        globals.cluadeToken[token_index]['status'] = True
    
    if data.get('PLUS'):
        globals.cluadeToken[token_index]['PLUS'] = data['PLUS']
        
    save_cltoken(globals.cluadeToken)
    return jsonify({'success': True, 'message': '账号更新成功'})

# 删除用户
@app.route('/api/Claude/<email>', methods=['DELETE'])
@admin_required
def delete_Claude(email):
    
    # 过滤掉要删除的用户
    updated_email = [token for token in globals.cluadeToken if token['email'] != email]
    
    if len(updated_email) == len(globals.cluadeToken):
        return jsonify({'success': False, 'message': '账号不存在'}), 404
    globals.cluadeToken = updated_email
    save_cltoken(globals.cluadeToken)
    return jsonify({'success': True, 'message': '账号删除成功'})