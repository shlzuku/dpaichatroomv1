# Flask WebSocket 聊天室应用v1

一个基于Flask和WebSocket的实时聊天室应用，支持用户聊天和@电影功能。

## 功能特性

- 实时聊天功能（基于WebSocket）
- 用户加入/离开通知
- @电影功能（支持分享和播放电影链接）
- 聊天历史记录

## 技术栈

- **后端**: Python Flask
- **WebSocket**: Flask-SocketIO
- **前端**: HTML, JavaScript, CSS

## 快速开始

### 1. 安装依赖

```bash
pip install flask flask-socketio
```

### 2. 运行应用

```bash
python app.py
```

应用将在 http://localhost:5000 启动。

## @电影功能使用方法

在聊天输入框中使用以下格式分享电影：

```
@电影 电影链接
```

系统会自动解析并显示电影播放器。

## 将代码上传到GitHub（后续步骤）

### 1. 在GitHub上创建新仓库

1. 登录你的GitHub账号
2. 点击右上角的"+", 选择"New repository"
3. 填写仓库名称，选择公开/私有
4. 点击"Create repository"

### 2. 连接本地仓库到GitHub

在本地仓库目录中运行以下命令：

```bash
# 添加远程仓库（请替换为你的GitHub仓库URL）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

# 推送代码到GitHub
git push -u origin master
```

### 注意事项

- 如果遇到权限问题，请确保你的GitHub账号有正确的访问权限
- 第一次推送可能需要提供GitHub的用户名和密码（或个人访问令牌）
- 为了更好的实践，建议在推送到GitHub前从.gitignore中移除venv目录