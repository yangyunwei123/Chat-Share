from app import app
from flask import jsonify
import utils.globals as globals
from utils.globals import *
from utils.tools import *





# 一键同步网关seedmap
@app.route('/api/syc', methods=['GET'])
@admin_required
def syc_seedmap():
    del_seedmap("clear")

    for user in globals.users:
        if user['bind_email'] != '' and user['bind_token'] != '':
            set_seedmap(user['id'],user['bind_token'])
    return jsonify({'success': True, 'message': '同步成功'})