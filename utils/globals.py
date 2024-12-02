import json
import os
from datetime import datetime, timedelta

DATA_FOLDER = "data"
AUTO_REFRESH_CONFIG = os.path.join(DATA_FOLDER, "auto_refresh_config.json")
CHAT_TOKEN = os.path.join(DATA_FOLDER, "chatToken.json")
FAILED_TOKENS = os.path.join(DATA_FOLDER, "failed_tokens.json")
REFRESH_HISTORY = os.path.join(DATA_FOLDER, "refresh_history.json")
CLAUDE_TOKEN = os.path.join(DATA_FOLDER, "claudeToken.json")
USERS = os.path.join(DATA_FOLDER, "users.json")

auto_refresh_config = {}
chatToken = []
failed_tokens = []
refresh_history = []
users = []
cluadeToken = []

# 上一级目录
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
    
# 读取 auto_refresh_config.json 文件
if os.path.exists(AUTO_REFRESH_CONFIG):
    with open(AUTO_REFRESH_CONFIG, "r") as f:
        try:
            auto_refresh_config = json.load(f)
        except:
            auto_refresh_config = {"auto_refresh_enabled": False, "refresh_interval_days": 9, "next_refresh_time": None}
else:
    auto_refresh_config = {"auto_refresh_enabled": False, "refresh_interval_days": 9, "next_refresh_time": None}

# 如果 next_refresh_time 为 None，则设置为当前时间加 9 天
if auto_refresh_config["next_refresh_time"] is None:
    next_refresh_time = datetime.now() + timedelta(days=9)
    auto_refresh_config["next_refresh_time"] = next_refresh_time.isoformat()  # 转换为 ISO 8601 格式字符串
 
    
# 读取 chatToken.json 文件
if os.path.exists(CHAT_TOKEN):
    with open(CHAT_TOKEN, "r") as f:
        try:
            chatToken = json.load(f)
        except:
            chatToken = []
else:
    chatToken = []


# 读取 claudeToken.json 文件
if os.path.exists(CLAUDE_TOKEN):
    with open(CLAUDE_TOKEN, "r") as f:
        try:
            cluadeToken = json.load(f)
        except:
            cluadeToken = []
else:
    cluadeToken = []


# 读取 failed_tokens.json 文件
if os.path.exists(FAILED_TOKENS):
    with open(FAILED_TOKENS, "r") as f:
        try:
            failed_tokens = json.load(f)
        except:
            failed_tokens = []
else:
    failed_tokens = []
    
# 读取刷新历史
if os.path.exists(REFRESH_HISTORY):
    with open(REFRESH_HISTORY, "r") as f:
        try:
            refresh_history = json.load(f)
        except:
            refresh_history = []
else:
    refresh_history = []
    
# 加载用户表
if os.path.exists(USERS):
    with open(USERS, "r", encoding="utf-8") as f:
        try:
            users = json.load(f)
        except:
            users = []
else:
    users = []

# 如果 users 为空，设置为默认用户
if not users:
    users = [
        {
            "id": "d87a64eb-3eda-4f87-9268-d79387d1dfe6",
            "username": "admin",
            "password": "pbkdf2:sha256:260000$CqvLDzNaezUTatZ2$61963529d02a0c0eb74212775872a910a1315d160c4df11da528ad3c03a5ea85",
            "role": "admin",
            "bind_token": "",
            "bind_email": "",
            "expiration_time": "",
            "bind_claude_token": "",
            "bind_claude_email": "",
            "claude_expiration_time": ""
        }
    ]

# 保存更新后的 chatToken.json 文件
def save_retoken(updated_tokens):
    with open('data/chatToken.json', 'w') as f:
        json.dump(updated_tokens, f, indent=4)
        
# 保存更新后的 claudeToken.json 文件
def save_cltoken(updated_tokens):
    with open('data/claudeToken.json', 'w') as f:
        json.dump(updated_tokens, f, indent=4)

# 写入 failed_tokens.json 文件
def save_failed_tokens(failed_tokens):
    with open('data/failed_tokens.json', 'w') as f:
        json.dump(failed_tokens, f, indent=4)

# 保存定时任务信息
def save_auto_refresh_config(config):
    with open('data/auto_refresh_config.json', 'w') as f:
        json.dump(config, f)


# 保存刷新历史
def save_refresh_history(history):
    with open('data/refresh_history.json', 'w') as f:
        json.dump(history, f, indent=4)


# 保存用户信息
def save_users(users):
    with open('data/users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

save_users(users) 