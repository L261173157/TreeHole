# 手动Git更新部署指南

本指南适用于:本地开发 → 推送到GitHub → 手动在服务器拉取更新(不覆盖数据库)

---

## 📋 前提条件

1. ✅ 服务器已经通过 `git-deploy.sh` 完成首次部署
2. ✅ 数据库文件位于 `/opt/treehole/backend/treehole.db`
3. ✅ 服务器可以从GitHub拉取代码

---

## 🔄 完整更新流程

### 第一步: 本地开发和测试

#### 1.1 本地启动服务进行开发

**Windows**:
```bash
# 启动后端和前端
start.bat
```

**Linux/Mac**:
```bash
# 添加执行权限(首次)
chmod +x start.sh

# 启动
./start.sh
```

#### 1.2 开发完成后测试功能

访问 http://localhost:5173 测试:
- ✅ 发布留言功能正常
- ✅ 点赞/点踩功能正常
- ✅ 回复功能正常
- ✅ 页面显示正常

#### 1.3 提交代码到本地Git

```bash
# 查看修改状态
git status

# 添加修改的文件
git add .

# 提交代码(使用清晰的提交信息)
git commit -m "feat: 添加XXX功能"
# 或
git commit -m "fix: 修复XXX问题"
```

**提交信息规范**:
- `feat:` - 新功能
- `fix:` - 修复bug
- `docs:` - 文档更新
- `style:` - 代码格式调整
- `refactor:` - 代码重构
- `test:` - 测试相关
- `chore:` - 构建/工具变更

---

### 第二步: 推送到GitHub

```bash
# 推送到GitHub主分支
git push origin main
```

如果遇到冲突,先拉取最新代码:
```bash
# 拉取远程最新代码
git pull origin main --rebase

# 解决冲突后
git add .
git commit -m "resolve: 解决合并冲突"
git push origin main
```

---

### 第三步: 服务器上拉取更新

#### 3.1 SSH登录服务器

```bash
ssh root@123.57.82.112
# 或使用你的用户名
# ssh user@123.57.82.112
```

#### 3.2 备份数据库(重要!)

在更新前**务必备份**数据库:

```bash
# 进入项目目录
cd /opt/treehole

# 备份数据库(带时间戳)
sudo cp backend/treehole.db backend/treehole.db.backup.$(date +%Y%m%d_%H%M%S)

# 验证备份
ls -lh backend/treehole.db.backup.*

# 输出示例:
# -rw-r--r-- 1 root root 256K Dec 31 10:30 backend/treehole.db.backup.20251231_103000
```

**自动备份脚本** (可选):
```bash
# 创建备份脚本
cat > /opt/treehole/deploy/backup-db.sh << 'EOF'
#!/bin/bash
cd /opt/treehole
BACKUP_FILE="backend/treehole.db.backup.$(date +%Y%m%d_%H%M%S)"
cp backend/treehole.db "$BACKUP_FILE"
echo "数据库已备份至: $BACKUP_FILE"
ls -lh "$BACKUP_FILE"

# 只保留最近7天的备份
find backend/treehole.db.backup.* -mtime +7 -delete
EOF

chmod +x /opt/treehole/deploy/backup-db.sh

# 使用备份脚本
/opt/treehole/deploy/backup-db.sh
```

#### 3.3 查看当前状态

```bash
# 查看Git状态
git status

# 查看当前分支
git branch

# 查看远程更新
git fetch origin
git log HEAD..origin/main --oneline
```

#### 3.4 拉取代码更新

```bash
# 方法一: 直接拉取(推荐,如果没有本地修改)
git pull origin main

# 方法二: 先拉取再合并(更安全)
git fetch origin
git merge origin/main

# 方法三: 使用rebase(保持提交历史整洁)
git pull --rebase origin main
```

#### 3.5 检查更新内容

```bash
# 查看更新了哪些文件
git diff HEAD@{1} HEAD --name-only

# 查看最近的提交
git log --oneline -5
```

---

### 第四步: 安装依赖和构建

#### 4.1 更新后端依赖(如有变更)

检查 `backend/requirements.txt` 是否有更新:

```bash
# 查看requirements.txt是否被修改
git diff HEAD@{1} HEAD backend/requirements.txt

# 如果有更新,安装新依赖
cd /opt/treehole/backend
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

#### 4.2 更新前端依赖和构建

**每次前端代码更新后都需要重新构建**:

```bash
cd /opt/treehole/src

# 安装新依赖(如有)
npm install

# 构建生产版本(会使用.env.production配置)
npm run build

# 验证构建输出
ls -lh dist/
```

---

### 第五步: 重启服务

#### 5.1 重启后端服务

```bash
# 使用systemd重启
sudo systemctl restart treehole-backend

# 查看启动状态
sudo systemctl status treehole-backend

# 查看最新日志
sudo journalctl -u treehole-backend -n 50 --no-pager

# 或实时查看日志
sudo journalctl -u treehole-backend -f
```

#### 5.2 重启nginx(前端已更新时)

```bash
# 测试nginx配置
sudo nginx -t

# 重启nginx
sudo systemctl restart nginx

# 查看nginx状态
sudo systemctl status nginx
```

---

### 第六步: 验证更新

#### 6.1 在服务器上检查

```bash
# 检查后端健康状态
curl http://localhost:8000/ping

# 应返回: {"status":"ok","message":"服务正常运行"}

# 检查后端日志
sudo journalctl -u treehole-backend -n 20 --no-pager
```

#### 6.2 在浏览器中测试

访问: http://123.57.82.112

**测试项**:
- ✅ 页面能否正常加载
- ✅ 能否发布新留言
- ✅ 能否看到之前的留言(数据库未丢失)
- ✅ 点赞/点踩功能正常
- ✅ 回复功能正常
- ✅ 没有JavaScript错误(按F12查看控制台)

---

## 🛡️ 数据库保护机制

### .gitignore已保护数据库

项目已配置 `.gitignore` 防止数据库被提交:

```bash
# 查看backend目录下的.gitignore配置
cat backend/.gitignore

# 应该包含:
# treehole.db
# treehole.db.backup.*
# *.db
```

### 验证数据库未被Git跟踪

```bash
# 在服务器上检查
cd /opt/treehole
git status

# 正常情况下应该看不到treehole.db
# 如果看到,说明需要添加到.gitignore
```

---

## 🔧 常见场景处理

### 场景1: 只修改了前端代码

```bash
# 服务器上操作
cd /opt/treehole
git pull origin main
cd src
npm run build
sudo systemctl restart nginx
```

### 场景2: 只修改了后端代码

```bash
# 服务器上操作
cd /opt/treehole
git pull origin main
sudo systemctl restart treehole-backend
```

### 场景3: 前后端都有修改

```bash
# 服务器上操作
cd /opt/treehole

# 1. 备份数据库
/opt/treehole/deploy/backup-db.sh

# 2. 拉取代码
git pull origin main

# 3. 更新后端依赖(如有)
cd backend
source venv/bin/activate
pip install -r requirements.txt
deactivate

# 4. 重启后端
sudo systemctl restart treehole-backend

# 5. 构建前端
cd ../src
npm run build

# 6. 重启nginx
sudo systemctl restart nginx
```

### 场景4: 依赖包有更新

```bash
# 后端依赖更新
cd /opt/treehole/backend
source venv/bin/activate
pip install --upgrade -r requirements.txt
deactivate

# 前端依赖更新
cd /opt/treehole/src
npm install
npm run build
```

### 场景5: 拉取时遇到冲突

```bash
# 服务器上操作
cd /opt/treehole

# 查看冲突
git pull origin main
# 如果提示冲突

# 方案一: 放弃本地修改,使用远程代码
git reset --hard origin/main

# 方案二: 保留本地配置文件
# 先备份配置
cp backend/config.py backend/config.py.local
cp src/.env.production src/.env.production.local

# 拉取远程代码
git fetch origin
git reset --hard origin/main

# 恢复配置文件
mv backend/config.py.local backend/config.py
mv src/.env.production.local src/.env.production
```

---

## 🚨 故障排查

### 问题1: 更新后服务无法启动

**检查步骤**:

```bash
# 1. 查看后端服务状态
sudo systemctl status treehole-backend

# 2. 查看详细错误日志
sudo journalctl -u treehole-backend -n 100 --no-pager

# 3. 检查Python语法错误
cd /opt/treehole/backend
source venv/bin/activate
python -m py_compile main.py
deactivate

# 4. 尝试手动启动查看错误
cd /opt/treehole/backend
source venv/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8000
```

**解决方案**:
- 如果是代码错误,回滚到上一个版本
- 如果是依赖问题,重新安装依赖
- 如果是数据库问题,从备份恢复

### 问题2: 前端页面空白或报错

**检查步骤**:

```bash
# 1. 检查前端构建是否成功
ls -lh /opt/treehole/src/dist/

# 2. 检查nginx配置
sudo nginx -t

# 3. 查看nginx错误日志
sudo tail -f /var/log/nginx/error.log
```

**解决方案**:
```bash
# 重新构建前端
cd /opt/treehole/src
rm -rf dist/ node_modules/.vite
npm run build

# 重启nginx
sudo systemctl restart nginx
```

### 问题3: 数据库数据丢失

**恢复数据库**:

```bash
# 1. 停止后端服务
sudo systemctl stop treehole-backend

# 2. 查看备份文件
ls -lht /opt/treehole/backend/treehole.db.backup.* | head -5

# 3. 恢复最近的备份
sudo cp /opt/treehole/backend/treehole.db.backup.20251231_103000 \
        /opt/treehole/backend/treehole.db

# 4. 重启服务
sudo systemctl start treehole-backend
```

### 问题4: Git pull失败

**错误**: `Permission denied (publickey)`

**解决方案**:

```bash
# 方法一: 使用HTTPS代替SSH
cd /opt/treehole
git remote set-url origin https://github.com/L261173157/TreeHole.git
git pull origin main

# 方法二: 配置SSH密钥
# 在服务器上生成SSH密钥
ssh-keygen -t ed25519 -C "server@treehole"

# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 将公钥添加到GitHub账户的SSH keys中
# 然后重新拉取
git pull origin main
```

---

## 📊 一键更新脚本(可选)

创建便捷的更新脚本:

```bash
sudo nano /opt/treehole/deploy/manual-update.sh
```

内容:

```bash
#!/bin/bash

# TreeHole 手动更新脚本
# 用法: sudo bash deploy/manual-update.sh

set -e

echo "========================================"
echo "   TreeHole 手动更新脚本"
echo "========================================"
echo ""

PROJECT_DIR="/opt/treehole"
cd $PROJECT_DIR

# 1. 备份数据库
echo "📦 [1/6] 备份数据库..."
BACKUP_FILE="backend/treehole.db.backup.$(date +%Y%m%d_%H%M%S)"
cp backend/treehole.db "$BACKUP_FILE"
echo "✅ 数据库已备份至: $BACKUP_FILE"
echo ""

# 2. 拉取代码
echo "📥 [2/6] 拉取最新代码..."
git pull origin main
echo "✅ 代码已更新"
echo ""

# 3. 更新后端依赖
echo "📦 [3/6] 检查后端依赖..."
cd backend
source venv/bin/activate
pip install -r requirements.txt --quiet
deactivate
cd ..
echo "✅ 后端依赖已更新"
echo ""

# 4. 重启后端
echo "🔄 [4/6] 重启后端服务..."
sudo systemctl restart treehole-backend
sleep 3
sudo systemctl is-active --quiet treehole-backend && echo "✅ 后端服务已重启" || echo "❌ 后端服务启动失败!"
echo ""

# 5. 构建前端
echo "🔨 [5/6] 构建前端..."
cd src
npm run build --quiet
cd ..
echo "✅ 前端构建完成"
echo ""

# 6. 重启nginx
echo "🔄 [6/6] 重启nginx..."
sudo systemctl restart nginx
sudo systemctl is-active --quiet nginx && echo "✅ nginx已重启" || echo "❌ nginx启动失败!"
echo ""

# 7. 验证
echo "🔍 验证服务状态..."
if curl -s http://localhost:8000/ping | grep -q "ok"; then
    echo "✅ 后端服务正常"
else
    echo "❌ 后端服务异常"
    exit 1
fi

echo ""
echo "========================================"
echo "  更新完成!"
echo "========================================"
echo ""
echo "访问地址: http://123.57.82.112"
echo "数据库备份: $BACKUP_FILE"
echo ""
```

使用脚本:

```bash
# 添加执行权限
sudo chmod +x /opt/treehole/deploy/manual-update.sh

# 运行更新
sudo bash /opt/treehole/deploy/manual-update.sh
```

---

## 📝 更新检查清单

在每次更新前,确认以下事项:

- [ ] 本地功能已测试通过
- [ ] 代码已提交到Git
- [ ] 代码已推送到GitHub
- [ ] 服务器数据库已备份
- [ ] 查看本次更新涉及的文件
- [ ] 拉取代码无冲突
- [ ] 后端服务重启成功
- [ ] 前端重新构建(如有修改)
- [ ] 浏览器验证功能正常
- [ ] 数据完整性验证(旧留言还在)

---

## 🎯 最佳实践

1. **定期备份数据库**
   - 每次更新前必备份
   - 保留最近7天的备份

2. **使用Git分支**
   - main分支保持稳定
   - 开发使用feature分支
   - 测试通过后再合并到main

3. **小步快跑**
   - 频繁小更新优于大版本更新
   - 每次更新后立即验证

4. **查看提交日志**
   - 更新前查看 `git log`
   - 了解本次更新的内容

5. **测试环境优先**
   - 先在本地测试
   - 确认无问题再部署到生产环境

---

## 📞 需要帮助?

遇到问题时,检查以下日志:

- **后端日志**: `sudo journalctl -u treehole-backend -f`
- **nginx日志**: `sudo tail -f /var/log/nginx/error.log`
- **Git状态**: `git status` 和 `git log`
