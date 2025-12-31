# TreeHole 完整部署指南

这个文档提供从零开始的完整部署流程讲解，适合所有水平的开发者。

---

## 📋 目录

- [一、部署前准备](#一部署前准备)
- [二、配置服务器环境](#二配置服务器环境)
- [三、推送代码到GitHub](#三推送代码到github)
- [四、服务器首次部署](#四服务器首次部署)
- [五、配置GitHub Actions自动部署](#五配置github-actions自动部署)
- [六、后续更新流程](#六后续更新流程)
- [七、常见问题排查](#七常见问题排查)

---

## 一、部署前准备

### 1.1 需要准备的东西

#### 必需资源：

- ✅ **一台Ubuntu服务器**（推荐20.04+）
- ✅ **服务器有公网IP**
- ✅ **可以通过SSH登录服务器**
- ✅ **本地电脑已安装Git**
- ✅ **GitHub账号**

#### 服务器最低配置：

```
CPU: 1核
内存: 512MB
硬盘: 10GB
系统: Ubuntu 20.04+ / Debian 10+
```

### 1.2 获取服务器信息

你需要知道以下信息：

```bash
服务器IP地址: 123.57.82.112
SSH端口: 通常为 22
SSH用户名: root 或 ubuntu 或其他
SSH密码或密钥
```

### 1.3 测试服务器连接

在本地电脑打开终端（CMD/Powershell/Terminal）：

```bash
# 测试SSH连接
ssh user@123.57.82.112

# 成功后会提示输入密码
# 输入密码后能登录说明连接正常
```

**连接成功后**，输入 `exit` 退出服务器，我们继续下一步。

---

## 二、配置服务器环境

### 2.1 登录服务器

```bash
ssh user@123.57.82.112
# 输入密码登录
```

### 2.2 更新系统

```bash
sudo apt update
sudo apt upgrade -y
```

### 2.3 检查Python版本

```bash
python3 --version
# 应该显示 Python 3.9 或更高版本
```

**如果没有安装Python**：

```bash
sudo apt install -y python3 python3-pip python3-venv
```

### 2.4 安装Node.js 18

```bash
# 添加NodeSource仓库
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -

# 安装Node.js
sudo apt install -y nodejs

# 验证安装
node --version  # 应显示 v18.x.x
npm --version   # 应显示 9.x.x 或更高
```

### 2.5 安装nginx（反向代理）

```bash
sudo apt install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 2.6 配置防火墙

```bash
# 允许SSH（重要！防止把自己锁在外面）
sudo ufw allow 22/tcp

# 允许HTTP
sudo ufw allow 80/tcp

# 如果直接用端口访问，也要开放
sudo ufw allow 5173/tcp  # 前端端口（可选）
sudo ufw allow 8000/tcp  # 后端端口（可选）

# 启用防火墙
sudo ufw enable

# 查看状态
sudo ufw status
```

**⚠️ 重要提示**：

如果你的服务器在云平台（阿里云/腾讯云/AWS），还需要在**云平台控制台的"安全组"**中开放端口！

- 开放端口：22（SSH）、80（HTTP）、443（HTTPS）
- 如果直接访问，还需开放：5173、8000

### 2.7 退出服务器

```bash
exit
```

---

## 三、推送代码到GitHub

### 3.1 在GitHub创建新仓库

1. 访问 https://github.com
2. 点击右上角 `+` → `New repository`
3. 填写信息：
   - **Repository name**: `TreeHole`
   - **Description**: `匿名留言板`
   - **Public**: ✅ （开源项目选择Public）
   - **不要勾选**"Add a README file"（我们已经有了）
4. 点击 `Create repository`

创建后，GitHub会显示仓库地址：
```
https://github.com/L261173157/TreeHole.git
```

### 3.2 在本地初始化Git

在本地项目目录打开终端：

**Windows**:
```bash
cd d:\linxin\OneDrive\Learn\web\TreeHole
```

**Linux/Mac**:
```bash
cd ~/TreeHole
```

检查Git状态：

```bash
# 检查是否已经是Git仓库
git status
```

如果提示 `"not a Git repository"` 或 `"fatal: not a git repository"`，则初始化：

```bash
git init
```

### 3.3 添加所有文件

```bash
git add .
```

查看状态：

```bash
git status
# 应该看到很多绿色的文件：
#   new file:   backend/main.py
#   new file:   src/src/App.vue
#   ...
```

### 3.4 创建首次提交

```bash
git commit -m "Initial commit: TreeHole匿名留言板

- 实现留言发布功能
- 实现点赞/点踩功能
- 实现留言回复功能
- 添加XSS防护
- 配置CORS安全策略
- 添加Git部署脚本"
```

### 3.5 关联远程仓库

```bash
# 添加GitHub远程仓库
git remote add origin https://github.com/L261173157/TreeHole.git
```

验证远程仓库：

```bash
git remote -v
# 应该显示：
# origin  https://github.com/L261173157/TreeHole.git (fetch)
# origin  https://github.com/L261173157/TreeHole.git (push)
```

### 3.6 推送到GitHub

```bash
git push -u origin main
```

**如果提示失败**，可能是因为默认分支是 `master`：

```bash
# 试试master分支
git branch -M master
git push -u origin master
```

或者先在GitHub设置中将默认分支改为 `main`：
- GitHub仓库 → Settings → Branches → Default branch → 改为 `main`

**成功后**，刷新GitHub页面应该能看到所有代码文件！🎉

---

## 四、服务器首次部署

### 4.1 方法一：从GitHub克隆（推荐）

**登录服务器**：

```bash
ssh user@123.57.82.112
```

**克隆代码**：

```bash
cd /opt
sudo git clone https://github.com/L261173157/TreeHole.git
cd TreeHole
```

**查看文件**：

```bash
ls -la
# 应该看到：
# backend/  deploy/  src/  README.md  ...
```

### 4.2 方法二：手动上传（如果没有GitHub）

**在本地打包**：

```bash
# 在本地项目目录
tar -czf treehole.tar.gz --exclude='node_modules' --exclude='venv' --exclude='__pycache__' --exclude='*.pyc' --exclude='.git' .
```

**上传到服务器**：

```bash
scp treehole.tar.gz user@123.57.82.112:/tmp/
```

**在服务器上解压**：

```bash
ssh user@123.57.82.112
cd /opt
sudo mkdir -p treehole
cd treehole
sudo tar -xzf /tmp/treehole.tar.gz
```

### 4.3 运行自动部署脚本

```bash
cd /opt/treehole
sudo bash deploy/git-deploy.sh main
```

### 4.4 部署过程详解

部署脚本会执行以下步骤：

#### 步骤1：检查系统

```
========================================
   TreeHole Git部署脚本
========================================

分支: main
部署目录: /opt/treehole

服务器IP: 123.57.82.112
是否使用IP地址 123.57.82.112 访问? (y/n):
```

**输入 `y` 并回车**。

#### 步骤2：安装依赖（首次运行）

```
[首次部署] 安装系统依赖...
Hit:1 http://archive.ubuntu.com/ubuntu focal InRelease
Reading package lists... Done
...
[1/7] 更新系统包...
[2/7] 安装Python和Node.js...
```

**耐心等待**，这可能需要几分钟。

#### 步骤3：配置环境

```
[3/7] 设置项目目录: /opt/treehole
[4/7] 配置环境变量...
配置生产环境配置...
```

脚本会自动创建 `deploy/production.env` 文件。

#### 步骤4：安装后端依赖

```
[5/7] 安装后端依赖...
创建 Python 虚拟环境...
Collecting fastapi
  Downloading FastAPI-0.104.1-py3-none-any.whl
...
```

#### 步骤5：构建前端

```
[6/7] 构建前端...
vite v5.0.0 building for production...
✓ 1234 modules transformed.
dist/index.html                   0.45 kB
dist/assets/index-xxxxx.css       12.34 kB
dist/assets/index-xxxxx.js        45.67 kB
```

#### 步骤6：配置nginx

```
[7/7] 配置nginx...
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

#### 步骤7：启动服务

```
重启服务...
Created symlink /etc/systemd/system/multi-user.target.wants/treehole-backend.service.
```

### 4.5 部署完成提示

成功后，你应该看到：

```
========================================
  部署完成!
========================================

访问地址:
  前端: http://123.57.82.112
  API: http://123.57.82.112/api/
  API文档: http://123.57.82.112/docs

更新部署时运行:
  sudo /opt/treehole/deploy/git-deploy.sh main
```

**恭喜！部署成功！** 🎉

### 4.6 验证部署

#### 在浏览器访问

1. **前端页面**: http://123.57.82.112
   - 应该看到"树洞"标题和留言板界面

2. **API文档**: http://123.57.82.112/docs
   - 应该看到Swagger UI界面

3. **健康检查**: http://123.57.82.112/ping
   - 应该返回JSON: `{"status":"ok","message":"服务正常运行"}`

#### 在服务器检查服务状态

```bash
# 检查后端服务
sudo systemctl status treehole-backend
```

**期望输出**：
```
● treehole-backend.service - TreeHole Backend API
     Loaded: loaded (/etc/systemd/system/treehole-backend.service; enabled)
     Active: active (running) since Mon 2025-12-31 10:00:00 CST
   Main PID: 12345 (uvicorn)
      Tasks: 2 (limit: 4915)
     Memory: 45.6M
     CGroup: /system.slice/treehole-backend.service
             ├─12345 /opt/treehole/backend/venv/bin/python3 /opt/treehole/backend/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
             └─12346 /opt/treehole/backend/venv/bin/python3 /opt/treehole/backend/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
```

关键词：
- `enabled` - 开机自启
- `active (running)` - 正在运行 ✅

```bash
# 检查nginx
sudo systemctl status nginx
```

**期望输出**：
```
● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled)
     Active: active (running) since Mon 2025-12-31 10:00:00 CST
```

#### 查看日志

```bash
# 查看后端日志（实时）
sudo journalctl -u treehole-backend -f
# 按 Ctrl+C 退出

# 查看nginx错误日志
sudo tail -f /var/log/nginx/error.log
# 按 Ctrl+C 退出

# 查看应用日志
tail -f /opt/treehole/backend/backend.log
```

#### 测试API

```bash
# 测试健康检查
curl http://localhost:8000/ping
# 期望输出: {"status":"ok","message":"服务正常运行"}

# 测试获取留言列表
curl http://localhost:8000/messages/
# 期望输出: {"code":0,"message":"success","data":[]}
```

### 4.7 修复CORS配置问题

如果前端无法连接后端（浏览器F12控制台有CORS错误）：

#### 步骤1：检查当前CORS配置

```bash
cat /opt/treehole/deploy/production.env
```

#### 步骤2：编辑配置文件

```bash
sudo nano /opt/treehole/deploy/production.env
```

#### 步骤3：修改CORS_ORIGINS

将 `YOUR_SERVER_IP` 替换为实际IP：

```bash
# 使用IP访问
CORS_ORIGINS=http://123.57.82.112:5173,http://123.57.82.112:8000

# 或使用域名（如果有）
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

#### 步骤4：保存并重启

按 `Ctrl+O` 保存，`Ctrl+X` 退出。

```bash
sudo systemctl restart treehole-backend
```

#### 步骤5：验证修复

刷新浏览器页面，打开F12控制台，查看是否还有CORS错误。

---

## 五、配置GitHub Actions自动部署

### 5.1 理解自动部署流程

```
你推送代码 → GitHub检测 → 触发Actions → SSH登录服务器 → 拉取代码 → 重启服务 → 完成
     ↓              ↓              ↓               ↓            ↓          ↓        ↓
  git push      自动触发      运行工作流       执行部署脚本   git pull   systemctl  ✅
```

### 5.2 生成SSH密钥对

#### 在本地电脑生成密钥

```bash
# 生成SSH密钥
ssh-keygen -t rsa -b 4096 -C "github-actions" -f ~/.ssh/treehole_deploy
```

**交互过程**：

```
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase):  # 直接回车，不设置密码
Enter same passphrase again:  # 直接回车
```

**生成结果**：

```
Your identification has been saved in /home/user/.ssh/treehole_deploy
Your public key has been saved in /home/user/.ssh/treehole_deploy.pub
The key fingerprint is:
SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxx github-actions
```

**生成的两个文件**：

- `treehole_deploy` - **私钥**（保密！）
- `treehole_deploy.pub` - **公钥**（添加到服务器）

### 5.3 将公钥添加到服务器

#### 方法一：使用ssh-copy-id（推荐）

```bash
ssh-copy-id -i ~/.ssh/treehole_deploy.pub user@123.57.82.112
```

**提示**：输入服务器密码

**期望输出**：

```
Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'user@123.57.82.112'"
and check to make sure that only the key(s) you wanted were added.
```

#### 方法二：手动添加

**步骤1：查看公钥内容**

```bash
cat ~/.ssh/treehole_deploy.pub
```

**复制输出的公钥**，类似：

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx github-actions
```

**步骤2：登录服务器**

```bash
ssh user@123.57.82.112
```

**步骤3：添加公钥**

```bash
# 创建.ssh目录（如果不存在）
mkdir -p ~/.ssh

# 添加公钥
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCxxxxxxxxxxx... github-actions" >> ~/.ssh/authorized_keys

# 设置正确的权限
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

**步骤4：退出服务器**

```bash
exit
```

### 5.4 测试SSH密钥登录

```bash
ssh -i ~/.ssh/treehole_deploy user@123.57.82.112
```

**成功标志**：应该能**免密登录**，不需要输入密码！

如果提示输入密码，说明密钥配置有问题，重新检查上面的步骤。

登录成功后，输入 `exit` 退出。

### 5.5 将私钥添加到GitHub

#### 步骤1：查看私钥内容

```bash
cat ~/.ssh/treehole_deploy
```

**复制完整的私钥**，包括：

```
-----BEGIN RSA PRIVATE KEY-----
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
...
-----END RSA PRIVATE KEY-----
```

**重要**：
- 必须包含 `-----BEGIN` 和 `-----END` 行
- 复制所有行，不要遗漏

#### 步骤2：在GitHub添加Secret

1. **打开GitHub仓库**
   - 访问 https://github.com/YOUR_USERNAME/TreeHole

2. **进入Settings**
   - 点击顶部的 `Settings` 标签

3. **进入Secrets页面**
   - 左侧菜单找到 `Secrets and variables`
   - 点击 `Actions`

4. **添加SSH私钥**
   - 点击 `New repository secret` 按钮
   - **Name**: `SSH_PRIVATE_KEY`
   - **Value**: 粘贴刚才复制的私钥
   - 点击 `Add secret`

5. **添加服务器IP**
   - 再次点击 `New repository secret`
   - **Name**: `SERVER_HOST`
   - **Value**: `123.57.82.112`（你的服务器IP）
   - 点击 `Add secret`

6. **添加服务器用户名**
   - 再次点击 `New repository secret`
   - **Name**: `SERVER_USER`
   - **Value**: `user`（你的SSH用户名）
   - 点击 `Add secret`

**配置完成后的Secrets列表**：

```
✅ SSH_PRIVATE_KEY     (已更新)
✅ SERVER_HOST         (已更新)
✅ SERVER_USER         (已更新)
```

### 5.6 修改GitHub Actions工作流

#### 检查工作流文件

确认项目中存在 `.github/workflows/deploy.yml` 文件。

#### 编辑工作流文件（可选）

如果需要自定义，可以编辑 `.github/workflows/deploy.yml`：

```yaml
name: Deploy to Server

on:
  push:
    branches:
      - main
      - master
  workflow_dispatch:  # 允许手动触发

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout代码
        uses: actions/checkout@v3

      - name: 配置SSH
        uses: webfactory/ssh-agent@v0.8.0
        with:
          ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}

      - name: 添加服务器到known_hosts
        run: |
          mkdir -p ~/.ssh
          ssh-keyscan -H ${{ secrets.SERVER_HOST }} >> ~/.ssh/known_hosts

      - name: 部署到服务器
        run: |
          ssh ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }} << 'ENDSSH'
            cd /opt/treehole

            # 拉取最新代码
            git fetch origin
            git pull origin main

            # 备份数据库
            cp backend/treehole.db backend/treehole.db.backup.$(date +%Y%m%d_%H%M%S)

            # 安装后端依赖
            cd backend
            source venv/bin/activate
            pip install -r requirements.txt
            deactivate

            # 构建前端
            cd ../src
            npm install
            npm run build

            # 重启服务
            sudo systemctl restart treehole-backend
          ENDSSH

      - name: 健康检查
        run: |
          sleep 5
          curl -f http://${{ secrets.SERVER_HOST }}/ping || exit 1
```

### 5.7 提交GitHub Actions配置

在本地项目目录：

```bash
git add .github/workflows/deploy.yml
git commit -m "Add GitHub Actions deployment workflow"
git push origin main
```

### 5.8 首次手动触发部署

#### 步骤1：打开GitHub Actions

1. 访问GitHub仓库
2. 点击顶部的 `Actions` 标签

#### 步骤2：选择工作流

应该能看到 `Deploy to Server` 工作流。

#### 步骤3：手动运行

1. 点击 `Deploy to Server` 进入详情页
2. 点击 `Run workflow` 按钮
3. 选择分支：`main`
4. 点击绿色按钮 `Run workflow`

#### 步骤4：查看部署日志

1. 页面会自动跳转到新的运行记录
2. 点击运行记录查看详细日志
3. 展开各个步骤查看输出

**期望的日志输出**：

```
✓ Checkout代码
✓ 配置SSH
✓ 添加服务器到known_hosts
✓ 部署到服务器
  cd /opt/treehole
  git pull origin main
  Already up to date.
  ...
✓ 健康检查
```

**等待完成**：通常需要2-5分钟。

### 5.9 验证自动部署

部署完成后：

1. **查看Actions状态**
   - 绿色勾 ✅ = 成功
   - 红色叉 ❌ = 失败（点击查看错误）

2. **测试应用**
   ```bash
   # 在浏览器访问
   http://123.57.82.112
   ```

3. **检查服务器**
   ```bash
   ssh user@123.57.82.112
   sudo systemctl status treehole-backend
   ```

---

## 六、后续更新流程

### 6.1 本地开发

修改代码，例如：

```bash
# 修改前端
nano src/src/components/MessageBoard.vue

# 修改后端
nano backend/main.py

# 添加新文件
echo "新功能" > backend/new_feature.py
```

### 6.2 本地测试

**启动后端**：

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**启动前端**（新终端）：

```bash
cd src
npm install
npm run dev
```

**测试功能**：
- 访问 http://localhost:5173
- 测试所有修改的功能
- 确保没有明显错误

### 6.3 提交更改

**查看修改**：

```bash
git status
```

**输出示例**：

```
On branch main
Changes not staged for commit:
  modified:   src/src/components/MessageBoard.vue
  modified:   backend/main.py

Untracked files:
  backend/new_feature.py
```

**添加修改**：

```bash
git add .
```

**提交**：

```bash
git commit -m "feat: 添加xxx功能

- 实现了xxx功能
- 优化了xxx体验
- 修复了xxx问题

Closes #123"
```

**提交信息规范**：

- `feat:` - 新功能
- `fix:` - 修复bug
- `docs:` - 文档更新
- `style:` - 代码格式
- `refactor:` - 重构
- `test:` - 测试
- `chore:` - 构建/工具

### 6.4 推送到GitHub

```bash
git push origin main
```

**期望输出**：

```
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Delta compression using up to 8 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (5/5), 1.23 KiB | 1.23 MiB/s, done.
Total 5 (delta 2), reused 0 (delta 0)
To https://github.com/YOUR_USERNAME/TreeHole.git
   abc123d..def456e  main -> main
```

### 6.5 自动部署触发

推送后，GitHub会自动：

1. **检测推送** - 收到代码更新
2. **触发Actions** - 运行部署工作流
3. **SSH连接** - 登录服务器
4. **拉取代码** - `git pull`
5. **安装依赖** - `pip install` / `npm install`
6. **构建前端** - `npm run build`
7. **重启服务** - `systemctl restart`
8. **健康检查** - `curl /ping`

### 6.6 查看部署进度

#### 在GitHub查看

1. **打开Actions标签**
   - 仓库页面 → `Actions`

2. **查看最新运行**
   - 应该看到最新的workflow运行记录
   - 状态指示器：
     - 🟡 运行中
     - ✅ 成功
     - ❌ 失败

3. **查看详细日志**
   - 点击运行记录
   - 展开各个步骤
   - 查看命令输出

#### 在服务器监控

```bash
ssh user@123.57.82.112

# 实时查看日志
sudo journalctl -u treehole-backend -f

# 或
tail -f /opt/treehole/backend/backend.log
```

### 6.7 验证更新

部署完成后：

1. **刷新浏览器**
   - 访问 http://123.57.82.112
   - 测试新功能
   - 检查是否正常

2. **检查API**
   ```bash
   curl http://123.57.82.112/ping
   ```

3. **查看服务状态**
   ```bash
   sudo systemctl status treehole-backend
   ```

---

## 七、常见问题排查

### 7.1 GitHub Actions失败 - SSH权限错误

**错误信息**：

```
Error: Permission denied (publickey)
```

**原因**：SSH密钥配置不正确

**解决步骤**：

#### 1. 测试SSH连接

```bash
ssh -i ~/.ssh/treehole_deploy user@123.57.82.112
```

**如果无法免密登录**：

- 重新检查 [5.3 将公钥添加到服务器](#53-将公钥添加到服务器)
- 确认公钥已添加到 `~/.ssh/authorized_keys`

#### 2. 验证GitHub Secret

```bash
# 查看私钥
cat ~/.ssh/treehole_deploy

# 确认完整
# -----BEGIN RSA PRIVATE KEY-----
# ...
# -----END RSA PRIVATE KEY-----
```

在GitHub：
- Settings → Secrets → Actions → `SSH_PRIVATE_KEY`
- 确认私钥完整且格式正确

#### 3. 重新添加Secret

如果私钥有问题：

1. 在GitHub删除旧的 `SSH_PRIVATE_KEY`
2. 重新添加，确保复制完整私钥
3. 重新触发Actions

### 7.2 推送后没有自动部署

**原因**：GitHub Actions未启用或配置错误

**解决步骤**：

#### 1. 检查工作流文件

```bash
ls -la .github/workflows/deploy.yml
```

应该存在此文件。

#### 2. 检查分支名称

```bash
git branch
```

确认是 `main` 或 `master`，与工作流文件中的 `branches` 匹配。

#### 3. 检查Actions是否启用

在GitHub：
- Settings → Actions → General
- 确保 `Actions permissions` 设置为 `Allow all actions`

#### 4. 手动触发

如果自动触发不工作，手动触发：
- Actions标签 → `Deploy to Server` → `Run workflow`

### 7.3 部署成功但无法访问

**原因**：防火墙或nginx配置问题

**解决步骤**：

#### 1. 检查防火墙

```bash
sudo ufw status
```

**期望输出**：

```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
8000/tcp                   ALLOW       Anywhere
```

**如果端口未开放**：

```bash
sudo ufw allow 80/tcp
sudo ufw allow 8000/tcp
sudo ufw reload
```

#### 2. 检查nginx状态

```bash
sudo systemctl status nginx
```

**如果未运行**：

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

#### 3. 查看nginx错误日志

```bash
sudo tail -f /var/log/nginx/error.log
```

**常见错误**：

- `connect() failed` - 后端服务未启动
- `permission denied` - 文件权限问题
- `directory index of` - 找不到index.html

#### 4. 测试nginx配置

```bash
sudo nginx -t
```

**如果有错误**：

```
nginx: [emerg] invalid number of arguments in ...
```

修复配置文件：

```bash
sudo nano /etc/nginx/sites-available/treehole
```

重启nginx：

```bash
sudo systemctl restart nginx
```

#### 5. 检查云平台安全组

如果在云平台（阿里云/腾讯云）：

1. 登录云平台控制台
2. 找到你的服务器实例
3. 进入"安全组"设置
4. 添加规则：
   - 端口：80、443
   - 协议：TCP
   - 来源：0.0.0.0/0

### 7.4 前端无法连接后端

**错误信息**（浏览器F12控制台）：

```
Access to XMLHttpRequest at 'http://123.57.82.112:8000/messages/'
from origin 'http://123.57.82.112' has been blocked by CORS policy
```

**原因**：CORS配置错误

**解决步骤**：

#### 1. 检查当前CORS配置

```bash
cat /opt/treehole/deploy/production.env
```

#### 2. 编辑配置

```bash
sudo nano /opt/treehole/deploy/production.env
```

#### 3. 修改CORS_ORIGINS

确保包含你的访问地址：

```bash
# 使用IP
CORS_ORIGINS=http://123.57.82.112:5173,http://123.57.82.112:8000

# 使用域名
CORS_ORIGINS=https://yourdomain.com,http://yourdomain.com

# 多个地址用逗号分隔
CORS_ORIGINS=http://123.57.82.112,https://yourdomain.com,http://localhost:5173
```

#### 4. 重启后端

```bash
sudo systemctl restart treehole-backend
```

#### 5. 验证修复

```bash
# 测试CORS
curl -H "Origin: http://123.57.82.112" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS \
     http://123.57.82.112:8000/messages/
```

应该返回CORS头：

```
Access-Control-Allow-Origin: http://123.57.82.112
```

### 7.5 后端服务启动失败

**错误信息**：

```bash
sudo systemctl status treehole-backend
# Failed to start TreeHole Backend
```

**解决步骤**：

#### 1. 查看详细日志

```bash
sudo journalctl -u treehole-backend -n 50
```

#### 2. 常见错误

**错误1：端口被占用**

```
[Errno 98] Address already in use
```

**解决**：

```bash
# 查找占用端口的进程
sudo lsof -i :8000

# 杀死进程
sudo kill -9 <PID>

# 重启服务
sudo systemctl restart treehole-backend
```

**错误2：依赖缺失**

```
ModuleNotFoundError: No module named 'fastapi'
```

**解决**：

```bash
cd /opt/treehole/backend
source venv/bin/activate
pip install -r requirements.txt
deactivate
sudo systemctl restart treehole-backend
```

**错误3：数据库问题**

```
sqlite3.OperationalError: unable to open database file
```

**解决**：

```bash
cd /opt/treehole/backend
sudo touch treehole.db
sudo chown www-data:www-data treehole.db
sudo chmod 644 treehole.db
sudo systemctl restart treehole-backend
```

### 7.6 前端构建失败

**错误信息**（GitHub Actions日志）：

```
ERROR: Failed to build frontend
npm ERR! code ELIFECYCLE
```

**原因**：Node版本不兼容或依赖安装失败

**解决步骤**：

#### 1. 检查Node版本

```bash
node --version
# 应该是 v18.x.x 或更高
```

#### 2. 清除缓存重新安装

```bash
cd /opt/treehole/src
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### 3. 如果是依赖问题

检查 `package.json`：

```bash
cat package.json
```

确保依赖版本正确。

### 7.7 Git拉取失败

**错误信息**：

```
error: cannot pull with rebase: You have unstaged changes
```

**解决**：

```bash
cd /opt/treehole
git status
```

**如果有未提交的修改**：

```bash
# 方案1：暂存修改
git stash
git pull origin main
git stash pop

# 方案2：放弃本地修改
git reset --hard origin/main
```

### 7.8 快速回滚

如果新版本有严重问题，快速回滚：

```bash
cd /opt/treehole

# 查看提交历史
git log --oneline -10

# 输出示例：
# abc1234 (HEAD -> main) feat: 添加新功能
# def5678 fix: 修复bug
# ghi9012 feat: 另一个功能

# 回滚到指定版本
git reset --hard def5678

# 重启服务
sudo systemctl restart treehole-backend
```

或在GitHub手动回滚：
1. 打开仓库
2. 点击 `commits`
3. 找到要回滚的版本
4. 点击 `<>` 按钮
5. 创建新分支或覆盖当前分支

---

## 📊 部署流程总览图

```
┌─────────────────────────────────────────────────────────────────┐
│                    TreeHole 部署流程图                          │
└─────────────────────────────────────────────────────────────────┘

    本地开发                     GitHub                      服务器
      │                          │                            │
      │ 1. 编写代码               │                            │
      │   - 前端Vue              │                            │
      │   - 后端FastAPI          │                            │
      │                          │                            │
      │ 2. git commit            │                            │
      │   git add .              │                            │
      │   git commit -m "..."   │                            │
      │                          │                            │
      │ 3. git push ────────────→ 4. 接收代码                  │
      │   origin main              ✓ 代码更新                  │
      │                          │                            │
      │                          │ 5. 检测推送                 │
      │                          │   ✓ 触发Actions             │
      │                          │                            │
      │                          │ 6. 运行工作流 ────────────→ 7. SSH登录
      │                          │   ✓ 配置SSH                   │
      │                          │                            │
      │                          │                            │ 8. git pull
      │                          │                            │   ✓ 拉取代码
      │                          │                            │
      │                          │                            │ 9. 安装依赖
      │                          │                            │   pip install
      │                          │                            │   npm install
      │                          │                            │
      │                          │                            │ 10. 构建
      │                          │                            │   npm run build
      │                          │                            │
      │                          │                            │ 11. 重启服务
      │                          │                            │   systemctl restart
      │                          │                            │
      │ ←────────────────────────────────────────────────── 12. 部署完成
      │                            ✓ 应用更新
      │                            ✓ 服务重启
      │                            ✓ 健康检查通过
      │
      │ 13. 测试验证
      │    - 浏览器访问
      │    - 功能测试
      │    - 日志检查
      │
      └─────────────────────────────────────────────────────→ 完成！
```

---

## 📝 部署检查清单

### 部署前检查

- [ ] 服务器可以通过SSH登录
- [ ] 服务器已安装Python 3.9+
- [ ] 服务器已安装Node.js 18+
- [ ] 防火墙已开放必要端口（22, 80, 443）
- [ ] 云平台安全组已开放端口（如适用）
- [ ] GitHub仓库已创建
- [ ] 本地已安装Git
- [ ] 可以克隆GitHub仓库

### 首次部署检查

- [ ] 代码已成功推送到GitHub
- [ ] 服务器上已克隆代码
- [ ] 部署脚本执行成功
- [ ] Python虚拟环境已创建
- [ ] 后端依赖已安装
- [ ] 前端依赖已安装
- [ ] 前端构建成功
- [ ] nginx配置正确
- [ ] systemd服务已启用
- [ ] 后端服务运行正常（`systemctl status`）
- [ ] nginx服务运行正常
- [ ] 可以通过浏览器访问前端
- [ ] 可以访问API文档
- [ ] 健康检查接口正常
- [ ] CORS配置正确（前端可连接后端）
- [ ] 数据库文件存在且权限正确

### GitHub Actions配置检查

- [ ] SSH密钥对已生成
- [ ] 公钥已添加到服务器
- [ ] 可以免密SSH登录服务器
- [ ] 私钥已添加到GitHub Secrets
- [ ] 服务器IP已添加到GitHub Secrets
- [ ] 服务器用户名已添加到GitHub Secrets
- [ ] GitHub Actions工作流文件存在
- [ ] 工作流配置正确
- [ ] 已手动触发测试部署
- [ ] 自动部署成功
- [ ] 健康检查通过

### 日常更新检查

- [ ] 本地代码已测试
- [ ] Git提交信息规范
- [ ] 代码已推送到GitHub
- [ ] GitHub Actions自动触发
- [ ] 部署日志显示成功
- [ ] 浏览器验证新功能
- [ ] 服务运行状态正常

---

## 🎯 总结

### 核心概念

TreeHole的部署流程基于Git和GitHub Actions，实现了：

1. **代码托管** - 使用GitHub管理代码版本
2. **自动化部署** - GitHub Actions自动触发部署
3. **服务运行** - 服务器运行后端和nginx
4. **公网访问** - 用户通过IP/域名访问

### 一次配置，永久使用

完成首次配置后，后续更新只需：

```bash
git add .
git commit -m "新功能"
git push
# 等待2-5分钟，自动部署完成！🎉
```

### 关键文件位置

- **本地项目**: `d:\linxin\OneDrive\Learn\web\TreeHole`
- **服务器项目**: `/opt/treehole`
- **后端服务**: `/opt/treehole/backend`
- **前端构建**: `/opt/treehole/src/dist`
- **nginx配置**: `/etc/nginx/sites-available/treehole`
- **systemd服务**: `/etc/systemd/system/treehole-backend.service`
- **环境配置**: `/opt/treehole/deploy/production.env`

### 管理命令

```bash
# 查看后端状态
sudo systemctl status treehole-backend

# 重启后端
sudo systemctl restart treehole-backend

# 查看后端日志
sudo journalctl -u treehole-backend -f

# 重启nginx
sudo systemctl restart nginx

# 查看nginx日志
sudo tail -f /var/log/nginx/error.log

# 手动更新
cd /opt/treehole
git pull
sudo systemctl restart treehole-backend

# 回滚版本
git log --oneline -10
git reset --hard <commit-hash>
sudo systemctl restart treehole-backend
```

---

## 📞 获取帮助

如果遇到问题：

1. **查看日志**
   - GitHub Actions日志
   - 服务器systemd日志
   - nginx错误日志

2. **检查配置**
   - GitHub Secrets
   - CORS配置
   - 防火墙规则

3. **查看文档**
   - 本文档的常见问题部分
   - GitHub仓库的Issues
   - FastAPI文档
   - Nginx文档

4. **提交Issue**
   - 在GitHub仓库创建Issue
   - 描述问题详细情况
   - 附上错误日志

---

**祝你部署顺利！** 🚀

如有任何问题，欢迎随时提问！
