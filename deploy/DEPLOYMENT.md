# TreeHole 服务器部署指南(传统方式)

> **推荐**: 如果你是开源项目部署,建议使用 [Git + GitHub Actions 自动部署](GIT-DEPLOYMENT.md)

## 📋 部署准备

### 服务器要求
- Ubuntu 20.04+ / Debian 10+
- Python 3.9+
- Node.js 22+
- 至少 512MB RAM
- 公网IP地址

### 本地准备
在本地电脑上,将项目打包并上传到服务器:

```bash
# 在本地项目目录
tar -czf treehole.tar.gz --exclude='node_modules' --exclude='venv' --exclude='__pycache__' --exclude='*.pyc' --exclude='.git' .

# 上传到服务器 (替换为你的服务器IP)
scp treehole.tar.gz user@你的服务器IP:/home/user/
```

## 🚀 服务器端部署步骤

### 1. 登录服务器
```bash
ssh user@你的服务器IP
```

### 2. 安装依赖

#### 安装 Python 和 pip
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

#### 安装 Node.js 22+
```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
```

#### 安装其他工具
```bash
sudo apt install -y nginx certbot python3-certbot-nginx
```

### 3. 解压项目
```bash
cd /home/user
tar -xzf treehole.tar.gz
sudo mv TreeHole /opt/treehole
cd /opt/treehole
```

### 4. 配置环境变量

编辑 `deploy/production.env` 文件:

```bash
nano deploy/production.env
```

**重要**: 将配置文件中的域名改为你的服务器IP:

```bash
# 如果没有域名,直接使用IP地址
CORS_ORIGINS=http://你的服务器IP

# 注意:生产环境前端使用nginx代理,API地址为相对路径
# VITE_API_BASE_URL=/api (在src/.env.production中配置)
```

示例:
```bash
CORS_ORIGINS=http://123.57.82.112
```

注意:前端构建时会使用 `src/.env.production` 文件中的配置:

```env
VITE_API_BASE_URL=/api
```

### 5. 配置防火墙

```bash
# 允许SSH
sudo ufw allow 22/tcp

# 允许HTTP和HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 启用防火墙
sudo ufw enable

# 查看状态
sudo ufw status
```

**注意**: 如果使用nginx反向代理,不需要开放5173和8000端口

### 6. 启动服务

#### 方法一: 使用启动脚本(推荐测试时使用)
```bash
chmod +x deploy/start-production.sh
chmod +x deploy/stop-production.sh
./deploy/start-production.sh
```

#### 方法二: 使用systemd(推荐生产环境)

**配置后端服务**:
```bash
# 复制service文件
sudo cp deploy/treehole-backend.service /etc/systemd/system/

# 创建运行用户
sudo useradd -r -s /bin/false www-data 2>/dev/null || true

# 设置权限
sudo chown -R www-data:www-data /opt/treehole
sudo chmod -R 755 /opt/treehole

# 安装后端依赖
cd /opt/treehole/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable treehole-backend
sudo systemctl start treehole-backend

# 查看状态
sudo systemctl status treehole-backend
```

**配置前端(使用nginx)**:

创建nginx配置:
```bash
sudo nano /etc/nginx/sites-available/treehole
```

添加以下内容(修改`server_name`为你的服务器IP或域名):
```nginx
server {
    listen 80;
    server_name 你的服务器IP;  # 例如: 123.57.82.112

    # 前端静态文件
    location / {
        root /opt/treehole/src/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API文档代理(可选)
    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

启用配置:
```bash
# 创建符号链接
sudo ln -s /etc/nginx/sites-available/treehole /etc/nginx/sites-enabled/

# 删除默认配置(如果存在)
sudo rm -f /etc/nginx/sites-enabled/default

# 构建前端(会使用.env.production配置)
cd /opt/treehole/src
npm install
npm run build

# 测试nginx配置
sudo nginx -t

# 重启nginx
sudo systemctl restart nginx
```

### 7. 访问应用

现在你可以通过以下地址访问:

- **前端**: `http://你的服务器IP` (使用nginx)
- **后端API**: `http://你的服务器IP/api/` (通过nginx代理)
- **API文档**: `http://你的服务器IP/docs` (通过nginx代理)

**验证部署**:

```bash
# 检查后端健康状态
curl http://localhost:8000/ping

# 应该返回: {"status":"ok","message":"服务正常运行"}
```

在浏览器访问 `http://你的服务器IP`,尝试发布一条留言验证功能是否正常。

## 🔐 可选: 配置HTTPS(使用Let's Encrypt)

如果你有域名,可以免费申请HTTPS证书:

```bash
# 替换为你的域名
sudo certbot --nginx -d yourdomain.com

# 自动续期
sudo certbot renew --dry-run
```

## 📊 管理命令

### 查看服务状态
```bash
# 后端服务(systemd)
sudo systemctl status treehole-backend

# 重启后端
sudo systemctl restart treehole-backend

# 停止后端
sudo systemctl stop treehole-backend

# 查看后端日志
sudo journalctl -u treehole-backend -f
# 或
tail -f /opt/treehole/backend/backend.log
```

### 查看端口占用
```bash
sudo netstat -tlnp | grep -E '8000|5173'
```

## 🔍 故障排查

### 1. 检查服务是否运行
```bash
curl http://localhost:8000/ping
```

### 2. 查看后端日志
```bash
tail -f /opt/treehole/backend/backend.log
```

### 3. 检查防火墙
```bash
sudo ufw status
```

### 4. 检查nginx错误日志
```bash
sudo tail -f /var/log/nginx/error.log
```

### 5. 常见问题

**问题1**: 无法从外网访问
- 检查防火墙是否开放端口: `sudo ufw status`
- 检查云服务商安全组规则(阿里云/腾讯云/AWS等)

**问题2**: CORS错误

- 确认后端环境变量中的 `CORS_ORIGINS` 包含你的访问地址
- 重启后端服务: `sudo systemctl restart treehole-backend`

**问题3**: 前端无法连接后端("Failed to fetch"错误)

- 检查前端 `src/.env.production` 文件中 `VITE_API_BASE_URL=/api`
- 重新构建前端: `cd /opt/treehole/src && npm run build`
- 确认后端服务正在运行
- 检查nginx配置中 `/api/` 的代理设置
- 查看浏览器控制台(F12)的网络请求

## 📝 更新部署

当需要更新代码时:

```bash
# 1. 上传新代码
scp treehole.tar.gz user@你的服务器IP:/home/user/

# 2. 在服务器上解压
cd /home/user
tar -xzf treehole.tar.gz
sudo cp -r TreeHole/* /opt/treehole/

# 3. 重启服务
sudo systemctl restart treehole-backend
sudo systemctl restart nginx

# 或者如果使用启动脚本
cd /opt/treehole
./deploy/stop-production.sh
./deploy/start-production.sh
```

## 🔒 安全建议

1. **修改默认端口**: 避免使用默认端口
2. **配置HTTPS**: 生产环境强烈建议使用HTTPS
3. **定期更新**: 保持系统和依赖包更新
4. **备份数据库**: 定期备份 `treehole.db` 文件
5. **限制访问**: 使用防火墙限制访问来源IP
6. **监控日志**: 定期检查访问日志

## 📞 技术支持

如遇问题,请检查:
- 后端日志: `/opt/treehole/backend/backend.log`
- nginx日志: `/var/log/nginx/`
- systemd日志: `sudo journalctl -u treehole-backend`
