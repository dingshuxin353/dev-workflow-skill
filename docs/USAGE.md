# Dev Workflow Skill 使用指南

## 安装方式

有两种安装方式：**全局安装**（所有项目可用）和**项目级安装**（仅当前项目可用）。

---

## 方式一：全局安装（推荐）

将Skill安装到用户级别的Claude配置目录，所有项目都可以使用。

### Step 1: 复制Skill定义文件

```bash
# 创建全局skills目录（如果不存在）
mkdir -p ~/.claude/skills

# 复制三个skill定义文件
cp /path/to/dev-workflow-skill/skills/pm.md ~/.claude/skills/
cp /path/to/dev-workflow-skill/skills/dev.md ~/.claude/skills/
cp /path/to/dev-workflow-skill/skills/qa.md ~/.claude/skills/
```

### Step 2: 在目标项目中添加CLAUDE.md规则

在你要使用此Skill的项目根目录创建或编辑 `CLAUDE.md`，添加以下内容：

```markdown
# 研发流程规则

## Git Worktree 配置

本项目使用Git Worktree进行多分支并行开发：
- main: 生产分支
- develop: 开发分支
- test: 测试分支

### 初始化Worktree（首次使用）
\`\`\`bash
git branch develop main 2>/dev/null || true
git branch test main 2>/dev/null || true
git worktree add ../$(basename $(pwd))-develop develop
git worktree add ../$(basename $(pwd))-test test
\`\`\`

## 文档存放规则

- PRD文档: `docs/prd/{feature-name}.md`
- 测试用例: `docs/test-cases/{feature-name}.md`
- 测试报告: `docs/test-reports/{feature-name}-{date}.md`

## 流程状态

状态文件: `.workflow-status.json`

状态流转: planning → developing → testing → reviewing → done

## 命令速查

| 命令 | 说明 |
|------|------|
| `@pm 新需求：...` | 开始需求分析 |
| `@dev` | 开始开发 |
| `@dev 修复` | 修复Bug |
| `@qa` | 开始测试 |
| `@qa 重测` | 重新测试 |
| `验收通过` | 确认验收 |
```

### Step 3: 创建必要的目录结构

```bash
# 在目标项目中创建文档目录
mkdir -p docs/prd docs/test-cases docs/test-reports
```

---

## 方式二：项目级安装

将Skill安装到特定项目，仅该项目可用。

### Step 1: 复制文件到项目

```bash
# 在目标项目根目录执行
mkdir -p .claude/skills

# 复制skill定义文件
cp /path/to/dev-workflow-skill/skills/*.md .claude/skills/

# 复制CLAUDE.md（或合并到现有的）
cp /path/to/dev-workflow-skill/CLAUDE.md ./CLAUDE.md

# 创建文档目录
mkdir -p docs/prd docs/test-cases docs/test-reports
```

### Step 2: 添加到.gitignore（可选）

```bash
# 如果不想提交状态文件
echo ".workflow-status.json" >> .gitignore
```

---

## 使用流程

### 1. 初始化Git Worktree（首次使用）

在目标项目根目录执行：

```bash
# 确保在main分支
git checkout main

# 创建develop和test分支
git branch develop main
git branch test main

# 创建worktree
git worktree add ../$(basename $(pwd))-develop develop
git worktree add ../$(basename $(pwd))-test test
```

执行后的目录结构：
```
workspace/
├── my-project/           # main分支（你的项目）
├── my-project-develop/   # develop分支
└── my-project-test/      # test分支
```

### 2. 开始使用

```bash
# 进入项目目录
cd my-project

# 启动Claude Code
claude

# 然后就可以使用了：
# @pm 新需求：实现用户登录功能
# @dev
# @qa
# 验收通过
```

---

## 完整使用示例

```
# 1. 产品经理阶段
用户: @pm 新需求：实现用户注册功能，支持邮箱注册

Claude: 📋 正在分析需求...
        PRD已生成: docs/prd/user-register.md
        测试用例已生成: docs/test-cases/user-register.md
        请确认后调用 @dev 开始开发

# 2. 开发阶段
用户: @dev

Claude: 🔧 已切换到 develop worktree
        开始开发...
        ✅ 开发完成，代码已合并到test分支
        可调用 @qa 开始测试

# 3. 测试阶段
用户: @qa

Claude: 🧪 已切换到 test worktree
        执行测试用例...
        ❌ 发现2个Bug
        请调用 @dev 修复

# 4. Bug修复
用户: @dev 修复

Claude: 🔧 进入Bug修复模式
        ✅ Bug已修复
        可调用 @qa 重测

# 5. 重新测试
用户: @qa 重测

Claude: 🧪 重新测试...
        ✅ 全部通过
        请输入"验收通过"完成发布

# 6. 验收发布
用户: 验收通过

Claude: ✅ 已合并到main分支
        🎉 发布完成！
```

---

## 目录结构说明

### Skill文件位置

```
# 全局安装
~/.claude/
└── skills/
    ├── pm.md      # 产品经理Skill
    ├── dev.md     # 研发经理Skill
    └── qa.md      # 测试经理Skill

# 项目级安装
my-project/
├── .claude/
│   └── skills/
│       ├── pm.md
│       ├── dev.md
│       └── qa.md
├── CLAUDE.md      # 项目规则
└── docs/
    ├── prd/
    ├── test-cases/
    └── test-reports/
```

### 运行时生成的文件

```
my-project/
├── .workflow-status.json    # 流程状态（自动生成）
└── docs/
    ├── prd/
    │   └── user-register.md        # PRD文档
    ├── test-cases/
    │   └── user-register.md        # 测试用例
    └── test-reports/
        └── user-register-20260205.md  # 测试报告
```

---

## 常见问题

### Q: Worktree已存在怎么办？

```bash
# 查看现有worktree
git worktree list

# 删除worktree
git worktree remove ../my-project-develop
git worktree remove ../my-project-test
```

### Q: 如何查看当前状态？

```bash
# 查看状态文件
cat .workflow-status.json

# 或在Claude中
@status
```

### Q: 如何重置流程？

```bash
# 删除状态文件即可重新开始
rm .workflow-status.json
```

### Q: 多个功能并行开发怎么办？

目前设计为单功能串行开发。如需并行开发多个功能，建议：
1. 为每个功能创建独立的feature分支
2. 分别完成后再合并

---

## 快速安装脚本

创建一个安装脚本，一键安装到全局：

```bash
#!/bin/bash
# install-dev-workflow.sh

SKILL_SOURCE="/path/to/dev-workflow-skill"
SKILL_TARGET="$HOME/.claude/skills"

# 创建目录
mkdir -p "$SKILL_TARGET"

# 复制skill文件
cp "$SKILL_SOURCE/skills/pm.md" "$SKILL_TARGET/"
cp "$SKILL_SOURCE/skills/dev.md" "$SKILL_TARGET/"
cp "$SKILL_SOURCE/skills/qa.md" "$SKILL_TARGET/"

echo "✅ Dev Workflow Skill 已安装到 $SKILL_TARGET"
echo ""
echo "使用方法："
echo "1. 在目标项目中添加CLAUDE.md规则"
echo "2. 初始化Git Worktree"
echo "3. 使用 @pm @dev @qa 命令"
```
