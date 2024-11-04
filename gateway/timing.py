from app import app
from datetime import datetime, timedelta
import time
import threading
from flask import request, jsonify
import utils.globals as globals
from utils.globals import *
from utils.tools import *









def is_main_process():
    import os
    return os.environ.get('WERKZEUG_RUN_MAIN') != 'true'

current_timer = None
timer_lock = threading.Lock()

def schedule_next_refresh():
    if not is_main_process():
        print("在 reloader 进程中，跳过定时器设置")
        return
        
    global current_timer
    
    with timer_lock:
        if globals.auto_refresh_config['auto_refresh_enabled']:
            if current_timer:
                current_timer.cancel()
                
            next_refresh = datetime.now() + timedelta(days=globals.auto_refresh_config['refresh_interval_days'])
            globals.auto_refresh_config['next_refresh_time'] = next_refresh.isoformat()
            save_auto_refresh_config(globals.auto_refresh_config)

            current_timer = threading.Timer(
                (next_refresh - datetime.now()).total_seconds(), 
                auto_refresh_tokens
            )
            current_timer.start()

def auto_refresh_tokens():

    print('开始自动刷新')
    new_access_tokens = refresh_access_tokens()

    # 更新刷新历史
    update_refresh_history(len(new_access_tokens))

    # 添加延时，确保两次刷新之间有足够间隔
    time.sleep(2)  # 等待1秒

    # 刷新完成后，调度下一次刷新
    schedule_next_refresh()

# 更新刷新历史
def update_refresh_history(token_count):

    globals.refresh_history.append({
        "timestamp": datetime.now().isoformat(),
        "token_count": token_count
    })

    # 保留最近的 5 条记录
    globals.refresh_history = globals.refresh_history[-5:]

    save_refresh_history(globals.refresh_history)

# 设定定时任务
@app.route('/set_auto_refresh', methods=['POST'])
@admin_required
def set_auto_refresh():
    data = request.json

    # 取消现有的定时任务
    globals.auto_refresh_config['auto_refresh_enabled'] = data['enabled']
    globals.auto_refresh_config['refresh_interval_days'] = data['interval']
    save_auto_refresh_config(globals.auto_refresh_config)

    if globals.auto_refresh_config['auto_refresh_enabled']:
        schedule_next_refresh()

    return jsonify({"status": "success", "message": "自动刷新设置已更新"})

# 加载定时任务配置信息
@app.route('/get_auto_refresh_config', methods=['GET'])
def get_auto_refresh_config():
    return jsonify(globals.auto_refresh_config)

# 在应用启动时调用这个函数
def init_auto_refresh():
    if not is_main_process():
        print("在 reloader 进程中，跳过定时器初始化")
        return
        
    print(f"在主进程中初始化自动刷新, 当前时间: {datetime.now()}")

    if globals.auto_refresh_config['auto_refresh_enabled'] and globals.auto_refresh_config['next_refresh_time']:
        next_refresh = datetime.fromisoformat(globals.auto_refresh_config['next_refresh_time'])
        
        if next_refresh > datetime.now():
            delay_seconds = (next_refresh - datetime.now()).total_seconds()
            print(f"设置初始定时器, 延迟秒数: {delay_seconds}")
            
            global current_timer
            with timer_lock:
                current_timer = threading.Timer(delay_seconds, auto_refresh_tokens)
                current_timer.start()
        else:
            schedule_next_refresh()

# 在应用启动时调用
init_auto_refresh()

# 手动刷新access token
@app.route('/refresh_tokens', methods=['POST'])
@admin_required
def refresh_tokens():
    try:
        # 调用刷新 access_token 的函数
        new_access_tokens = refresh_access_tokens()
        update_refresh_history(len(new_access_tokens))
        
        return jsonify({
            "status": "success",
            "access_tokens": new_access_tokens
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
