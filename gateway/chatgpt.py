from app import app
import json
from flask import request, jsonify
import utils.globals as globals
from utils.globals import *
from utils.tools import *



# 加载刷新历史
@app.route('/refresh_history', methods=['GET'])
@admin_required
def get_refresh_history():
    return jsonify({
        "status": "success",
        "history": globals.refresh_history
    }), 200

# 加载失败Refresh Token
@app.route('/get_failed_tokens')
@admin_required
def get_failed_tokens():
    try:
        return jsonify(globals.failed_tokens), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in failed_tokens.json"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# 加载Refresh Token
@app.route('/get_tokens')
@admin_required
def get_tokens():
    try:
        return jsonify(globals.chatToken), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in tokens.json"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 添加新账号
@app.route('/api/tokens', methods=['POST'])
@admin_required
def create_tokens():
    data = request.get_json()
    
    # 检查账号是否已存在
    if any(token['email'] == data['email'] for token in globals.chatToken):
        return jsonify({'success': False, 'message': '该账号已存在'}), 400
    
    new_token = {
        'email': data['email'],
        'refresh_token': data['ReToken'],
        'access_token': data['AcToken'],
        'status': True,
        'type':"/static/gpt.png",
        'PLUS': data['PLUS']
    }
    
    globals.chatToken.append(new_token)
    save_retoken(globals.chatToken)
    
    return jsonify({'success': True, 'message': '用户创建成功'})

# 更新账号信息
@app.route('/api/tokens/<email>', methods=['PUT'])
@admin_required
def update_token(email):
    data = request.get_json()
    
    token_index = next((i for i, token in enumerate(globals.chatToken) if token['email'] == email), None)
    if token_index is None:
        return jsonify({'success': False, 'message': '账号不存在'}), 400

    # 如果提供了邮箱，则更新邮箱
    new_email = data.get('email')
    if new_email:
        # 检查是否已有重复的邮箱
        if any(token['email'] == new_email for i, token in enumerate(globals.chatToken) if i != token_index):
            return jsonify({'success': False, 'message': '邮箱已存在'}), 400
        globals.chatToken[token_index]['email'] = new_email
        
    # 如果提供了ReToken，则更新ReToken
    if data.get('ReToken'):
        globals.chatToken[token_index]['refresh_token'] = data['ReToken']
    else:
        globals.chatToken[token_index]['refresh_token'] = ''

    # 如果提供了AcToken，则更新AcToken
    if data.get('AcToken'):
        globals.chatToken[token_index]['access_token'] = data['AcToken']
        globals.chatToken[token_index]['status'] = True
        for i, user in enumerate(globals.users):
            if user['bind_email'] == email:
                globals.users[i]['bind_token'] = data['AcToken']
                set_seedmap(globals.users[i]['id'],data['AcToken'])
        save_users(globals.users)
    else:
        globals.chatToken[token_index]['access_token'] = ''
        for i, user in enumerate(globals.users):
            if user['bind_email'] == email:
                globals.users[i]['bind_token'] = ''
                del_seedmap(globals.users[i]['id'])
        save_users(globals.users)
        
    
    if data.get('PLUS'):
        globals.chatToken[token_index]['PLUS'] = data['PLUS']
        
    save_retoken(globals.chatToken)
    return jsonify({'success': True, 'message': '账号更新成功'})

# 删除账号
@app.route('/api/tokens/<email>', methods=['DELETE'])
@admin_required
def delete_token(email):
    
    # 过滤掉要删除的账号
    updated_email = [token for token in globals.chatToken if token['email'] != email]
    
    if len(updated_email) == len(globals.chatToken):
        return jsonify({'success': False, 'message': '账号不存在'}), 404

    for i, user in enumerate(globals.users):
        if user['bind_email'] == email:
            globals.users[i]['bind_email'] = ''
            globals.users[i]['bind_token'] = ''
            del_seedmap(globals.users[i]['id'])
    save_users(globals.users)
    globals.chatToken=updated_email
    save_retoken(globals.chatToken)
    return jsonify({'success': True, 'message': '账号删除成功'})
