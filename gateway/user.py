from app import app
from flask import render_template, request, jsonify
import uuid
import utils.globals as globals
from utils.globals import *
from utils.tools import *
from werkzeug.security import generate_password_hash







@app.route('/user')
@admin_required
def user_management():
    return render_template('user_management.html')



# 获取所有用户
@app.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    # 返回用户列表时不包含密码信息
    return jsonify([{k: v for k, v in user.items() if k != 'password' and k != 'bind_token'} for user in globals.users])

# 创建新用户
@app.route('/api/users', methods=['POST'])
@admin_required
def create_user():
    data = request.get_json()
    
    # 检查用户名是否已存在
    if any(user['username'] == data['username'] for user in globals.users):
        return jsonify({'success': False, 'message': '用户名已存在'}), 400
    
    new_user = {
        'id': str(uuid.uuid4()),
        'username': data['username'],
        'password': generate_password_hash(data['password']),
        'role': data['role'],
        'bind_token': '',
        'bind_email': ''
    }
    
    globals.users.append(new_user)
    save_users(globals.users)
    
    return jsonify({'success': True, 'message': '用户创建成功'})

# 更新用户信息
@app.route('/api/users/<user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    data = request.get_json()
    
    user_index = next((i for i, user in enumerate(globals.users) if user['id'] == user_id), None)
    if user_index is None:
        return jsonify({'success': False, 'message': '用户不存在'}), 404
    
    # 检查用户名是否与其他用户冲突
    if any(user['username'] == data['username'] and user['id'] != user_id for user in globals.users):
        return jsonify({'success': False, 'message': '用户名已存在'}), 400
    
    # 更新用户信息
    globals.users[user_index]['username'] = data['username']
    globals.users[user_index]['role'] = data['role']
    
    # 如果提供了新密码，则更新密码
    if data.get('password'):
        globals.users[user_index]['password'] = generate_password_hash(data['password'])
    
    save_users(globals.users)
    return jsonify({'success': True, 'message': '用户更新成功'})

# 绑定ChatGPT账号
@app.route('/api/bind/<user_id>', methods=['PUT'])
@admin_required
def bind_account(user_id):
    data = request.get_json()
    user_index = next((i for i, user in enumerate(globals.users) if user['id'] == user_id), None)
    token_index = next((i for i, token in enumerate(globals.chatToken) if token['email'] == data['email']), None)
    res = set_seedmap(user_id,globals.chatToken[token_index]['access_token'])
    if res == 200:
        globals.users[user_index]['bind_email'] = data['email']
        globals.users[user_index]['bind_token'] = globals.chatToken[token_index]['access_token']
        save_users(globals.users)
        return jsonify({'success': True, 'message': '账号绑定成功'})
    else:
        return jsonify({'success': False, 'message': '账号绑定失败'})

# 解绑ChatGPT账号
@app.route('/api/del_bind/<user_id>', methods=['DELETE'])
@admin_required
def del_bind_account(user_id):
    res = del_seedmap(user_id)
    if res == 200:
        user_index = next((i for i, user in enumerate(globals.users) if user['id'] == user_id), None)
        globals.users[user_index]['bind_email'] = ''
        globals.users[user_index]['bind_token'] = ''
        save_users(globals.users)
        return jsonify({'success': True, 'message': '账号解绑成功'})
    else:
        return jsonify({'success': False, 'message': '账号解绑失败'})


# 获取全部ChatGPT账号的email
@app.route('/api/all_email', methods=['GET'])
@admin_required
def all_email():
    # 返回账号的全部email
    return jsonify([token['email'] for token in globals.chatToken if 'email' in token])

# 删除用户
@app.route('/api/users/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):

    # 过滤掉要删除的用户
    updated_users = [user for user in globals.users if user['id'] != user_id]
    
    user = next((user for user in globals.users if user['id'] == user_id), None)
    
    if len(updated_users) == len(globals.users):
        return jsonify({'success': False, 'message': '用户不存在'}), 404
    
    globals.users = updated_users
    save_users(globals.users)
    if user['bind_token'] != '':
        del_seedmap(user_id)
    return jsonify({'success': True, 'message': '用户删除成功'})