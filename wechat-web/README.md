# 微信公众号文章排版发布工具 (Web 版)

一个基于 Flask 的网页版微信公众号文章排版发布工具，支持文档上传、多风格排版和一键发布到公众号草稿箱。

## ✨ 功能特性

- 📄 **文档上传**：支持 Word (.docx)、Markdown (.md)、纯文本 (.txt)
- 🎨 **多风格排版**：简约、商务、文艺、科技四种风格
- 👁️ **实时预览**：所见即所得的排版预览效果
- 🚀 **一键发布**：直接发布到公众号草稿箱
- 🌓 **深色/浅色主题**：支持主题切换
- 📱 **响应式设计**：支持手机、平板、电脑访问

## 🚀 快速启动

### 方式一：一键启动（推荐）

```bash
cd wechat-web

# 安装依赖
python install.py

# 启动服务
python app.py
```

### 方式二：手动安装

```bash
cd wechat-web

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
```

### 启动脚本

- **Linux/Mac**: `./start.sh`
- **Windows**: `start.bat`

### 访问应用

打开浏览器访问：**http://127.0.0.1:5000**

## 📖 使用教程

### 1. 配置凭证

首次使用需要配置微信公众号凭证：

1. 登录 [微信公众平台](https://mp.weixin.qq.com)
2. 进入「设置与开发」→「基本配置」
3. 获取 AppID 和 AppSecret
4. 在应用界面点击「凭证配置」按钮进行设置

或直接编辑 `config.json` 文件：

```json
{
    "appid": "你的AppID",
    "appsecret": "你的AppSecret",
    "default_style": "simple"
}
```

### 2. 上传文档

支持三种格式：
- Word 文档 (.docx)
- Markdown (.md)
- 纯文本 (.txt)

将文件拖拽到上传区域，或点击选择文件。

### 3. 编辑内容

在左侧编辑区修改标题和内容。支持 Markdown 语法：

| 语法 | 效果 |
|------|------|
| `# 标题` | 一级标题 |
| `## 标题` | 二级标题 |
| `**粗体**` | **粗体** |
| `*斜体*` | *斜体* |
| `- 项目` | 无序列表 |
| `1. 项目` | 有序列表 |
| `> 引用` | 引用块 |
| ``` ```` ``` | 代码块 |

### 4. 选择风格

| 风格 | 预览 | 适用场景 |
|------|------|----------|
| 📄 简约 | 简洁清晰 | 通知公告 |
| 💼 商务 | 专业稳重 | 行业报告 |
| 📜 文艺 | 优雅古典 | 散文随笔 |
| 💻 科技 | 深色代码 | 技术文档 |

### 5. 预览发布

1. 点击「预览排版效果」打开预览页面
2. 在预览页面可以复制 HTML 或直接发布
3. 文章会保存到公众号草稿箱

### 6. 最终发布

登录 [微信公众平台](https://mp.weixin.qq.com) → 内容与工具 → 草稿箱，编辑并发布文章。

## 📁 项目结构

```
wechat-web/
├── app.py                 # Flask 主程序
├── config.json           # 配置文件（凭证）
├── requirements.txt      # Python 依赖
├── install.py            # 依赖安装脚本
├── start.sh             # Linux/Mac 启动脚本
├── start.bat            # Windows 启动脚本
├── test_project.py      # 项目检查脚本
├── README.md            # 说明文档
│
├── core/                 # 核心模块（复用）
│   ├── __init__.py
│   └── wechat_api.py    # Web 版 API
│
├── templates/            # HTML 模板
│   ├── index.html       # 主页
│   └── preview.html     # 预览页
│
└── static/              # 静态文件
    ├── css/
    │   └── style.css    # 样式文件
    └── js/
        └── main.js      # JavaScript
```

## 🔌 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 主页 |
| `/preview` | GET | 预览页面 |
| `/api/config` | GET/POST | 获取/设置配置 |
| `/api/upload` | POST | 上传文档 |
| `/api/format` | POST | 排版文章 |
| `/api/publish` | POST | 发布到公众号 |
| `/api/styles` | GET | 获取风格列表 |
| `/api/health` | GET | 健康检查 |

## ⚙️ 核心模块

项目复用了 `wechat-assistant/core` 目录下的核心模块：

- **ArticleFormatter**: 文章排版，支持 4 种风格
- **FileParser**: 文件解析，支持 docx/md/txt
- **WeChatAPI**: 微信公众号 API 封装

## ⚠️ 注意事项

1. **凭证安全**：请妥善保管 AppID 和 AppSecret
2. **接口限制**：微信 API 有调用频率限制
3. **图片处理**：外部图片链接会被移除
4. **草稿箱**：发布后需在公众号后台手动发布

## 🛠️ 技术栈

- **后端**：Flask 2.x + Python 3
- **前端**：HTML5 + CSS3 + JavaScript
- **核心**：复用 wechat-assistant/core

## 📝 许可证

MIT License
