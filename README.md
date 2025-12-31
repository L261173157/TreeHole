# TreeHole 🌳

<div align="center">
  <h3>匿名留言板 - 匿名分享你的心声</h3>
  <p>一个简单、现代化的匿名留言板应用</p>
</div>

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.9+-yellow)
![Node](https://img.shields.io/badge/node-18+-green)
![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/TreeHole?style=social)

[![CI/CD](https://github.com/YOUR_USERNAME/TreeHole/actions/workflows/deploy.yml/badge.svg)](https://github.com/YOUR_USERNAME/TreeHole/actions)

---

## ✨ 功能特性

- 🎭 **匿名留言** - 无需注册即可发布留言
- 💬 **留言回复** - 支持对留言进行回复,可展开/收起
- 📝 **字数限制** - 每条留言最多140字符
- 👍 **互动功能** - 支持点赞和点踩
- 🔄 **自动刷新** - 前端每30秒自动获取最新留言
- 📱 **响应式设计** - 适配桌面和移动设备
- ⚡ **实时更新** - 即时查看留言互动结果
- 🔒 **安全防护** - XSS攻击防护,CORS配置

## 🛠️ 技术栈

### 后端
- **框架**: FastAPI 0.104.1 - 高性能异步Web框架
- **数据库**: SQLite + SQLAlchemy 2.0.23 - ORM框架
- **数据验证**: Pydantic 2.10.0 - 支持Python 3.13
- **配置管理**: Pydantic Settings 2.6.0
- **服务器**: Uvicorn 0.24.0 - ASGI服务器
- **测试**: pytest 7.4.3 + pytest-asyncio 0.21.1
- **速率限制**: slowapi 0.1.9

### 前端
- **框架**: Vue 3 - 渐进式JavaScript框架
- **构建工具**: Vite 5.0.0 - 下一代前端构建工具
- **UI组件库**: Element Plus - Vue 3组件库
- **HTTP客户端**: Fetch API
- **代码规范**: ESLint + Prettier

## 📦 项目结构

```
TreeHole/
├── backend/               # 后端代码
│   ├── main.py          # FastAPI应用入口
│   ├── crud.py          # 数据库CRUD操作
│   ├── models.py        # 数据库模型
│   ├── schemas.py       # Pydantic数据模型
│   ├── database.py      # 数据库连接
│   ├── logger.py        # 日志配置
│   ├── config.py        # 配置管理
│   ├── requirements.txt # Python依赖
│   ├── pyproject.toml   # 项目配置
│   └── tests/           # 后端测试
│
├── src/                 # 前端代码
│   ├── src/
│   │   ├── components/  # Vue组件
│   │   ├── config/      # API配置
│   │   └── utils/       # 工具函数
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js   # Vite配置
│   ├── nginx.conf       # Nginx配置示例
│   └── tests/           # 前端测试
│
├── start.bat            # Windows启动脚本
├── start.sh             # Linux/Mac启动脚本
├── stop.bat             # Windows停止脚本
├── stop.sh              # Linux/Mac停止脚本
├── .env.example         # 环境变量模板
├── .gitignore          # Git忽略规则
├── LICENSE             # MIT许可证
└── README.md           # 项目文档
```

## 🚀 快速开始

### 方式一:使用启动脚本(推荐)

项目提供了便捷的启动脚本,可以自动完成环境配置和服务启动。

#### Windows

```bash
# 双击运行或在命令行中执行
start.bat
```

#### Linux/Mac

```bash
# 添加执行权限
chmod +x start.sh

# 运行启动脚本
./start.sh
```

启动脚本会自动:
- 检查 Python 和 Node.js 是否安装
- 创建 Python 虚拟环境
- 安装后端和前端依赖
- 启动后端和前端服务

**停止服务**:
```bash
# Windows
stop.bat

# Linux/Mac
./stop.sh
```

### 方式二:手动启动

如果你需要更多控制,可以选择手动启动。

#### 前置要求

确保你的系统已安装以下软件:

- **Python**: 3.9 或更高版本 ([下载地址](https://www.python.org/downloads/))
- **Node.js**: 18 或更高版本 ([下载地址](https://nodejs.org/))
- **npm**: 随 Node.js 一起安装,或使用 yarn/pnpm

检查版本:
```bash
python --version  # 应该显示 Python 3.9+
node --version    # 应该显示 v18+
npm --version     # 应该显示 9+
```

#### 2. 后端设置

##### 2.1 创建虚拟环境

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

激活成功后,命令行前缀会显示 `(venv)`

#### 2.2 安装依赖

```bash
# 确保在虚拟环境中,然后安装依赖
pip install -r requirements.txt
```

如果安装速度慢,可以使用国内镜像源:
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 2.3 配置环境变量(可选)

```bash
# 复制环境变量模板
cp ../.env.example ../.env

# 编辑 .env 文件设置你的配置
# Windows: notepad ../.env
# Linux/Mac: nano ../.env 或 vim ../.env
```

默认配置即可正常运行,如需自定义请参考下方 [配置说明](#⚙️-配置说明)

#### 2.4 启动后端服务器

```bash
# 确保已激活虚拟环境 (命令行前缀应有 (venv))
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**参数说明**:
- `--reload`: 热重载,代码修改后自动重启(开发环境)
- `--host 0.0.0.0`: 允许外部访问
- `--port 8000`: 指定端口

**启动成功标志**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

#### 2.5 访问后端服务

- **API根地址**: http://127.0.0.1:8000
- **Swagger UI文档**: http://127.0.0.1:8000/docs
- **ReDoc文档**: http://127.0.0.1:8000/redoc
- **健康检查**: http://127.0.0.1:8000/ping

#### 3. 前端设置

##### 3.1 安装依赖

打开**新的终端窗口**(保持后端运行):

```bash
# 进入前端目录
cd src

# 安装依赖
npm install
```

如果安装速度慢,可以使用国内镜像:
```bash
npm install --registry=https://registry.npmmirror.com
```

#### 3.2 配置环境变量(可选)

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
# Windows: notepad .env
# Linux/Mac: nano .env 或 vim .env
```

默认配置会连接到 `http://127.0.0.1:8000`,通常无需修改。

#### 3.3 启动开发服务器

```bash
npm run dev
```

**启动成功标志**:
```
  VITE v5.0.0  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

#### 3.4 访问前端应用

在浏览器中打开: **http://localhost:5173**

#### 4. 验证安装

1. 打开浏览器访问 http://localhost:5173
2. 尝试发布一条留言
3. 检查留言是否成功显示
4. 尝试点赞/点踩功能
5. 等待30秒观察自动刷新功能

如果一切正常,恭喜你!🎉 应用已成功运行。

## 📦 生产环境部署

> **提示**: 开发环境建议使用项目提供的启动脚本(`start.bat`/`start.sh`)

### 🚀 推荐部署方式

#### 方式一: Git + GitHub Actions 自动部署 (推荐开源项目)

适合开源项目或团队协作,支持自动化CI/CD流程。

**快速开始**:

1. **推送代码到GitHub**:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/TreeHole.git
git push -u origin main
```

2. **服务器首次部署**:

```bash
ssh user@your-server
sudo bash deploy/git-deploy.sh main
```

3. **配置GitHub Actions自动部署**:
   - 在GitHub仓库设置中添加Secrets (SSH私钥、服务器IP等)
   - 推送代码自动触发部署

详细文档: [Git部署指南](deploy/GIT-DEPLOYMENT.md)

#### 方式二:传统服务器部署

#### 后端部署

```bash
# 1. 上传代码到服务器
git clone <repository-url> /opt/treehole
cd /opt/treehole/backend

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 安装生产服务器
pip install gunicorn

# 5. 配置环境变量
cp /opt/treehole/.env.example /opt/treehole/.env
nano /opt/treehole/.env  # 编辑配置

# 6. 启动服务(使用 Gunicorn)
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

#### 前端部署

```bash
# 1. 构建生产版本
cd /opt/treehole/src
npm run build

# 2. 安装并配置 Nginx
sudo apt install nginx  # Ubuntu/Debian
# sudo yum install nginx  # CentOS/RHEL

# 3. 配置 Nginx
sudo nano /etc/nginx/sites-available/treehole
```

Nginx 配置示例:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /opt/treehole/src/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# 4. 启用配置
sudo ln -s /etc/nginx/sites-available/treehole /etc/nginx/sites-enabled/
sudo nginx -t  # 测试配置
sudo systemctl restart nginx

# 5. 配置 SSL (推荐使用 Let's Encrypt)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

#### 使用 Systemd 管理后端服务

创建服务文件:

```bash
sudo nano /etc/systemd/system/treehole-backend.service
```

内容:

```ini
[Unit]
Description=TreeHole Backend
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/opt/treehole/backend
Environment="PATH=/opt/treehole/backend/venv/bin"
ExecStart=/opt/treehole/backend/venv/bin/gunicorn \
    main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile /var/log/treehole/access.log \
    --error-logfile /var/log/treehole/error.log
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务:

```bash
# 创建日志目录
sudo mkdir -p /var/log/treehole
sudo chown www-data:www-data /var/log/treehole

# 启动并启用服务
sudo systemctl daemon-reload
sudo systemctl start treehole-backend
sudo systemctl enable treehole-backend

# 检查状态
sudo systemctl status treehole-backend
```

### 方案二:云平台部署

#### 部署到 Vercel (前端)

```bash
# 1. 安装 Vercel CLI
npm i -g vercel

# 2. 登录
vercel login

# 3. 部署
cd src
vercel
```

#### 部署到 Railway/Render (后端)

1. Fork 项目到 GitHub
2. 在 Railway/Render 创建新项目
3. 连接 GitHub 仓库
4. 选择后端目录 `/backend`
5. 配置环境变量
6. 部署完成

### 方案三:使用 PM2 部署

```bash
# 1. 安装 PM2
npm install -g pm2

# 2. 后端部署
cd /opt/treehole/backend
pm2 start "source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000" \
  --name treehole-backend \
  --interpreter python3

# 3. 前端构建
cd /opt/treehole/src
npm run build

# 4. 使用 serve 运行前端
npm install -g serve
pm2 start "serve -s dist -l 3000" --name treehole-frontend

# 5. 保存 PM2 配置
pm2 save
pm2 startup  # 跟随系统启动
```

### 常见问题排查

#### 端口被占用

```bash
# 查看端口占用
# Linux/Mac:
lsof -i :8000
netstat -tunlp | grep 8000

# Windows:
netstat -ano | findstr :8000

# 杀死进程
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows
```

#### 权限问题

```bash
# 确保文件权限正确
sudo chown -R www-data:www-data /opt/treehole
chmod -R 755 /opt/treehole
```

#### 依赖安装失败

```bash
# 清除缓存重新安装
pip cache purge
pip install -r requirements.txt --no-cache-dir

# 或使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### CORS 错误

检查后端 `.env` 文件中的 `CORS_ORIGINS` 配置:

```env
CORS_ORIGINS=http://localhost:5173,http://your-domain.com,https://your-domain.com
```

## ⚙️ 配置说明

### 环境变量

项目支持通过环境变量进行配置。创建`.env`文件(参考`.env.example`):

**后端配置**:
```env
# 数据库URL
DATABASE_URL=sqlite:///./treehole.db

# API服务器
API_HOST=0.0.0.0
API_PORT=8000

# CORS配置(多个源用逗号分隔)
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# 业务配置
MAX_CONTENT_LENGTH=140
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100

# 日志级别
LOG_LEVEL=INFO
```

**前端配置**:
```env
# API基础URL
VITE_API_BASE_URL=http://127.0.0.1:8000

# 请求超时(毫秒)
VITE_API_TIMEOUT=10000

# 留言最大长度
VITE_MAX_LENGTH=140

# 自动刷新间隔(毫秒)
VITE_REFRESH_INTERVAL=30000
```

## 📖 API文档

### 端点列表

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/` | 根路径,欢迎信息 |
| GET | `/ping` | 健康检查 |
| POST | `/messages/` | 创建新留言 |
| GET | `/messages/` | 获取留言列表(支持分页) |
| GET | `/messages/{id}` | 获取单条留言详情 |
| POST | `/messages/{id}/like` | 点赞留言 |
| POST | `/messages/{id}/dislike` | 点踩留言 |

### 请求/响应示例

**创建留言**:
```bash
curl -X POST "http://127.0.0.1:8000/messages/" \
  -H "Content-Type: application/json" \
  -d '{"content": "这是我的第一条留言"}'
```

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "content": "这是我的第一条留言",
    "timestamp": "2025-12-30T10:30:00",
    "like_count": 0,
    "dislike_count": 0,
    "parent_id": null
  }
}
```

更多详情请访问: http://127.0.0.1:8000/docs

## 🧪 测试

### 后端测试

```bash
cd backend
pytest
pytest --cov=. tests/  # 带覆盖率
```

### 前端测试

```bash
cd src
npm run test
```

## 📝 开发规范

### 代码风格

- **后端**: 使用 `black` 进行代码格式化
  ```bash
  cd backend
  black .
  ```

- **前端**: 使用 ESLint 和 Prettier
  ```bash
  cd src
  npm run lint
  npm run format
  ```

### 提交规范

使用 Conventional Commits 格式:
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构代码
- `test`: 添加测试
- `chore`: 构建/工具变动

## 🔒 安全说明

当前版本已实现的安全措施:

- ✅ CORS配置(可通过环境变量设置)
- ✅ 输入验证(前端和后端双重验证)
- ✅ XSS防护(HTML标签转义)
- ✅ 环境变量管理(.env文件不提交到Git)
- ✅ .gitignore配置(保护敏感信息)

**待实现的安全措施**:
- ⏳ 速率限制(防止DDoS和垃圾信息)
- ⏳ CSRF保护
- ⏳ 用户认证/授权
- ⏳ HTTPS强制

## 🐛 已知问题

1. SQLite 数据库在高并发下性能有限,生产环境建议使用 MySQL/PostgreSQL
2. 没有用户认证,无法防止刷票
3. 点赞/点踩没有次数限制

## 🗺️ 未来计划

- [ ] 添加用户认证系统
- [ ] 实现速率限制和防刷机制
- [ ] 添加管理员功能(审核、删除留言)
- [ ] 实现WebSocket实时更新
- [ ] 添加邮件通知功能
- [ ] 支持多语言(国际化)
- [ ] 添加数据统计和可视化
- [ ] CI/CD流水线
- [ ] 单元测试覆盖率提升到80%+

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交Issue和Pull Request!

## 📮 联系方式

如有问题,请提交Issue或联系项目维护者。

---

<div align="center">
  <p>Made with ❤️ by TreeHole Team</p>
</div>
