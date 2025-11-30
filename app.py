from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# 存储在线用户信息
online_users = {}
# 存储聊天记录
chat_history = []

# 读取配置文件
def load_config():
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"servers": [{"name": "本地服务器", "url": "http://127.0.0.1:5000"}]}

@app.route('/')
def index():
    config = load_config()
    return render_template('index.html', servers=config['servers'])

@app.route('/check_nickname', methods=['POST'])
def check_nickname():
    nickname = request.json.get('nickname')
    is_valid = nickname not in online_users
    return jsonify({'valid': is_valid})

@socketio.on('connect')
def handle_connect():
    logger.info('客户端已连接: %s', request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    for nickname, sid in online_users.items():
        if sid == request.sid:
            del online_users[nickname]
            emit('user_left', {'nickname': nickname, 'users': list(online_users.keys())}, broadcast=True)
            logger.info('%s 已断开连接', nickname)
            break

@socketio.on('login')
def handle_login(data):
    nickname = data['nickname']
    online_users[nickname] = request.sid
    join_room('chat_room')
    
    # 发送历史消息给新用户
    emit('chat_history', {'history': chat_history})
    
    # 广播新用户加入
    emit('user_joined', {'nickname': nickname, 'users': list(online_users.keys())}, broadcast=True)
    logger.info('%s 已登录', nickname)

@socketio.on('send_message')
def handle_message(data):
    nickname = data['nickname']
    message = data['message']
    timestamp = data['timestamp']
    
    # 处理特殊命令
    message_type = 'normal'
    command_data = None
    display_message = message
    
    if message.startswith('@电影') and len(message.split()) > 1:
        message_type = 'movie'
        movie_url = message.split(' ', 1)[1]
        # 使用解析地址对URL进行处理
        parsed_url = 'https://jx.m3u8.tv/jiexi/?url=' + movie_url
        command_data = {'url': parsed_url}
        # 修改显示消息为更友好的格式
        display_message = f'分享了一个电影链接: {movie_url}'
    elif message.startswith('@川小农'):
        message_type = 'ai'
        prompt = message.split(' ', 1)[1] if len(message.split()) > 1 else ''
        command_data = {'prompt': prompt, 'response': '您好，我是川小农AI助手，目前功能正在开发中。'}
    
    message_data = {
        'nickname': nickname,
        'message': display_message,
        'timestamp': timestamp,
        'type': message_type,
        'command_data': command_data
    }
    
    # 保存聊天记录（限制100条）
    chat_history.append(message_data)
    if len(chat_history) > 100:
        chat_history.pop(0)
    
    # 广播消息
    emit('new_message', message_data, room='chat_room')
    logger.info('消息已广播 - 发送者: %s, 类型: %s', nickname, message_type)

@socketio.on('logout')
def handle_logout(data):
    nickname = data['nickname']
    if nickname in online_users:
        del online_users[nickname]
        leave_room('chat_room')
        emit('user_left', {'nickname': nickname, 'users': list(online_users.keys())}, broadcast=True)
        logger.info('%s 已退出', nickname)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)