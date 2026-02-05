# 快速开始

## 实际需要的文件

这个Skill的核心只有 **4个文件**：

```
需要复制的文件：
├── skills/
│   ├── pm.md      # 产品经理Skill定义
│   ├── dev.md     # 研发经理Skill定义
│   └── qa.md      # 测试经理Skill定义
└── CLAUDE.md      # 项目规则（复制到目标项目）
```

`src/` 目录下的Python代码是**可选的参考实现**，Claude Code会直接使用内置工具（Bash、Read、Write）执行操作，不需要这些代码。

---

## 一分钟安装

### 全局安装（推荐）

```bash
# 1. 复制skill文件到全局目录
mkdir -p ~/.claude/skills
cp skills/*.md ~/.claude/skills/

# 完成！现在所有项目都可以使用 @pm @dev @qa 了
```

### 在目标项目中使用

```bash
# 2. 进入你的项目
cd /path/to/your-project

# 3. 复制CLAUDE.md（或将内容合并到现有的）
cp /path/to/dev-workflow-skill/CLAUDE.md ./

# 4. 创建文档目录
mkdir -p docs/prd docs/test-cases docs/test-reports

# 5. 初始化Git Worktree（首次）
git branch develop main 2>/dev/null || true
git branch test main 2>/dev/null || true
git worktree add ../$(basename $(pwd))-develop develop
git worktree add ../$(basename $(pwd))-test test

# 6. 开始使用
claude
# 然后输入: @pm 新需求：xxx
```

---

## 最简安装

如果你只想快速试用，甚至可以只复制skill文件：

```bash
# 只需要这一步
cp skills/*.md ~/.claude/skills/
```

然后在任何项目中使用 `@pm`、`@dev`、`@qa` 命令。

Skill会自动：
- 创建 `docs/` 目录结构
- 创建 `.workflow-status.json` 状态文件
- 引导你初始化Git Worktree（如果需要）

---

## 文件作用说明

| 文件 | 必须? | 作用 |
|------|-------|------|
| `skills/*.md` | ✅ 必须 | Skill定义，告诉Claude如何工作 |
| `CLAUDE.md` | 推荐 | 项目规则，确保一致性 |
| `templates/*.md` | 可选 | 文档模板参考 |
| `src/*.py` | 可选 | 参考实现，Claude不直接使用 |
