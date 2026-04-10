# 网页版部署指南

## 方式一：Render.com（免费托管，推荐）

### 步骤

1. **注册 Render 账号**
   - 访问 https://render.com
   - 点击 "Get Started" 注册（支持 GitHub 登录）

2. **上传代码到 GitHub**
   ```bash
   # 在本地初始化 Git
   cd wechat-web
   git init
   git add .
   git commit -m "Initial commit"
   
   # 创建 GitHub 仓库后推送
   git remote add origin https://github.com/你的用户名/wechat-web.git
   git push -u origin main
   ```

3. **在 Render 创建 Web Service**
   - 登录 Render Dashboard
   - 点击 "New +" → "Web Service"
   - 连接你的 GitHub 仓库
   - 选择 wechat-web 仓库

4. **配置部署**
   - **Name**: wechat-web（或任意名称）
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Instance Type**: Free

5. **点击 "Create Web Service"**
   - 等待几分钟部署完成
   - 部署成功后会得到一个 URL，如：`https://wechat-web.onrender.com`

---

## 方式二：Railway.app（免费额度）

### 步骤

1. **注册 Railway 账号**
   - 访问 https://railway.app
   - 使用 GitHub 登录

2. **新建项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择 wechat-web 仓库

3. **自动部署**
   - Railway 会自动检测 Python 项目
   - 自动安装依赖并部署
   - 部署成功后得到 URL

---

## 方式三：PythonAnywhere（免费）

### 步骤

1. **注册账号**
   - 访问 https://www.pythonanywhere.com
   - 注册免费账号

2. **上传代码**
   - 进入 "Files" 页面
   - 上传 wechat-web 目录下所有文件

3. **创建 Web App**
   - 进入 "Web" 页面
   - 点击 "Add a new web app"
   - 选择 Python 版本（3.10）
   - 选择 Flask 框架
   - 设置代码路径

4. **配置 WSGI**
   ```python
   import sys
   sys.path.append('/home/你的用户名/wechat-web')
   from app import app as application
   ```

5. **重启 Web App**
   - 点击 "Reload" 按钮

---

## 方式四：自己的云服务器

如果你有云服务器（阿里云、腾讯云等）：

```bash
# 1. 上传代码
scp -r wechat-web root@你的服务器IP:/root/

# 2. SSH 登录服务器
ssh root@你的服务器IP

# 3. 安装依赖
cd /root/wechat-web
pip install -r requirements.txt

# 4. 使用 Gunicorn 运行（推荐）
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 5. 使用 Nginx 反向代理（可选）
# 配置 Nginx 将 80 端口代理到 5000 端口
```

---

## 注意事项

1. **凭证安全**
   - 生产环境建议将 AppID 和 AppSecret 设置为环境变量
   - 不要将 config.json 提交到公开仓库

2. **端口配置**
   - Render/Railway 会自动分配端口
   - 代码已支持从环境变量读取 PORT

3. **文件上传**
   - 免费平台的临时文件存储有限制
   - 建议后续接入云存储（如阿里云 OSS）

---

## 推荐选择

| 平台 | 免费额度 | 速度 | 易用性 |
|------|---------|------|--------|
| Render | 750小时/月 | 快 | ⭐⭐⭐⭐⭐ |
| Railway | $5/月额度 | 快 | ⭐⭐⭐⭐ |
| PythonAnywhere | 有限 | 中 | ⭐⭐⭐ |

**推荐使用 Render.com**，免费、稳定、易用。
