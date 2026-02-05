# Dev Workflow Skill

产品、研发、测试三角色协作的自动化工作流 Skill。

## 功能

```
需求 → @pm → PRD/测试用例 → @dev → 代码开发 → @qa → 测试 → 验收 → 上线
                                    ↑              │
                                    └── Bug修复 ←──┘
```

## 三个 Skill

| Skill | 触发词 | 职责 |
|-------|--------|------|
| pm | `@pm`, `新需求` | 生成PRD和测试用例 |
| dev | `@dev`, `修复` | 代码开发、Bug修复 |
| qa | `@qa`, `重测` | 测试执行、报告生成 |

## 安装

```bash
# 复制skill文件夹到全局目录
cp -r skills/pm ~/.claude/skills/
cp -r skills/dev ~/.claude/skills/
cp -r skills/qa ~/.claude/skills/
```

## 使用

### 1. 在目标项目中添加规则

将 `CLAUDE.md` 复制到你的项目根目录。

### 2. 初始化 Git Worktree

```bash
git branch develop main 2>/dev/null || true
git branch test main 2>/dev/null || true
git worktree add ../$(basename $(pwd))-develop develop
git worktree add ../$(basename $(pwd))-test test
```

### 3. 开始使用

```bash
# 产品经理：分析需求
@pm 新需求：实现用户登录功能

# 研发：开始开发
@dev

# 测试：开始测试
@qa

# 如有Bug
@dev 修复
@qa 重测

# 验收通过
验收通过
```

## 项目结构

```
dev-workflow-skill/
├── README.md
├── CLAUDE.md              # 项目规则（复制到目标项目）
└── skills/
    ├── pm/
    │   └── SKILL.md       # 产品经理Skill
    ├── dev/
    │   └── SKILL.md       # 研发经理Skill
    └── qa/
        └── SKILL.md       # 测试经理Skill
```

## 状态流转

```
planning → developing → testing → reviewing → done
               ↑            │
               └── fixing ──┘
```

## License

MIT
