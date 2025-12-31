# 贡献指南

感谢你对TreeHole的关注!我们欢迎各种形式的贡献。

## 🤝 如何贡献

### 报告Bug

如果你发现了bug,请:

1. 在[Issues](../../issues)中搜索是否已有相同问题
2. 如果没有,创建新的Issue,包含:
   - 清晰的标题
   - 复现步骤
   - 期望行为 vs 实际行为
   - 环境信息(OS,浏览器版本等)
   - 截图(如果相关)

### 提出新功能

1. 先在[Issues](../../issues)讨论你的想法
2. 等待维护者反馈
3. 获得批准后再开始开发

### 提交代码

#### 1. Fork仓库

点击右上角的Fork按钮

#### 2. 克隆你的Fork

```bash
git clone https://github.com/YOUR_USERNAME/TreeHole.git
cd TreeHole
```

#### 3. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

#### 4. 进行更改

- 遵循现有代码风格
- 添加必要的注释
- 更新相关文档
- 确保代码通过测试

#### 5. 提交更改

```bash
git add .
git commit -m "描述你的更改"
```

提交信息格式:
- `feat: 添加新功能`
- `fix: 修复bug`
- `docs: 更新文档`
- `style: 代码格式调整`
- `refactor: 代码重构`
- `test: 添加测试`
- `chore: 构建/工具变更`

#### 6. 推送到你的Fork

```bash
git push origin feature/your-feature-name
```

#### 7. 创建Pull Request

1. 访问你Fork的页面
2. 点击"New Pull Request"
3. 填写PR描述:
   - 说明你的更改
   - 关联相关Issue
   - 添加截图(如果适用)

## 📋 开发规范

### 代码风格

**Python (后端)**:
- 遵循PEP 8
- 使用有意义的变量名
- 函数添加docstring
- 最大行长度: 100

**JavaScript/Vue (前端)**:
- 遵循Vue.js风格指南
- 使用Composition API
- 组件名使用PascalCase
- 常量使用UPPER_SNAKE_CASE

### 提交规范

使用[Conventional Commits](https://www.conventionalcommits.org/)规范:

```
<type>(<scope>): <subject>

<body>

<footer>
```

示例:
```
feat(message): 添加留言回复功能

- 添加回复展开/收起功能
- 实现回复列表懒加载
- 优化回复交互体验

Closes #123
```

### 测试

在提交PR前,请确保:

- [ ] 本地测试通过
- [ ] 代码没有linter错误
- [ ] 新功能有相应测试
- [ ] 文档已更新

## 🔧 开发环境设置

### 后端开发

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 前端开发

```bash
cd src
npm install
npm run dev
```

## 📖 项目结构

```
TreeHole/
├── backend/              # 后端API
│   ├── main.py          # FastAPI主程序
│   ├── models.py        # 数据库模型
│   ├── schemas.py       # Pydantic模式
│   ├── crud.py          # 数据库操作
│   ├── config.py        # 配置文件
│   └── requirements.txt # Python依赖
├── src/                 # 前端
│   ├── src/
│   │   ├── components/  # Vue组件
│   │   ├── App.vue      # 主应用
│   │   └── main.js      # 入口文件
│   └── package.json     # Node依赖
├── deploy/              # 部署脚本
└── docs/                # 文档
```

## 🎯 优先事项

查看[Projects](../../projects)或[Issues](../../issues)中的标签:
- `good first issue`: 适合新手
- `help wanted`: 需要帮助
- `enhancement`: 新功能
- `bug`: 需要修复的bug

## 💬 交流方式

- GitHub Issues: 问题反馈
- GitHub Discussions: 功能讨论
- Pull Requests: 代码贡献

## ⭐ 成为贡献者

所有贡献者将被添加到项目的贡献者列表中。

## 📄 许可证

通过贡献代码,你同意你的贡献将使用[MIT许可证](LICENSE)发布。

## 🙏 致谢

感谢所有为TreeHole做出贡献的人!
