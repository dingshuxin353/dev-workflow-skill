# Dev Workflow Skill

产品规划、产品设计、研发、测试四角色协作的自动化工作流 Skill。

## 功能

```
规划 → @planner → 路线图/排期 → @pm → PRD/测试用例 → @dev → 开发 → @qa → 测试 → 验收 → 上线
                                                        ↑              │
                                                        └── Bug修复 ←──┘
```

## 四个 Skill

| Skill | 触发词 | 职责 |
|-------|--------|------|
| planner | `@planner`, `规划` | 产品路线图、迭代排期 |
| pm | `@pm`, `新需求` | PRD设计、测试用例 |
| dev | `@dev`, `修复` | 代码开发、Bug修复 |
| qa | `@qa`, `重测` | 测试执行、报告生成 |

## 安装

```bash
# 复制skill文件夹到全局目录
cp -r skills/planner ~/.claude/skills/
cp -r skills/pm ~/.claude/skills/
cp -r skills/dev ~/.claude/skills/
cp -r skills/qa ~/.claude/skills/
```

## 使用

### 1. 在目标项目中添加规则

将 `CLAUDE.md` 复制到你的项目根目录。

### 2. 初始化文档目录

```bash
mkdir -p docs/prd docs/test-cases docs/test-reports
```

### 3. 初始化 Git Worktree

```bash
# 自动检测主分支（main或master）
DEFAULT_BRANCH=$(git branch --show-current)

git branch develop $DEFAULT_BRANCH 2>/dev/null || true
git branch test $DEFAULT_BRANCH 2>/dev/null || true
git worktree add ../$(basename $(pwd))-develop develop
git worktree add ../$(basename $(pwd))-test test
```

### 4. 开始使用

```bash
# 产品规划：制定路线图和排期
@planner

# 产品设计：根据排期或直接需求生成PRD
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
    ├── planner/
    │   └── SKILL.md       # 产品规划Skill
    ├── pm/
    │   └── SKILL.md       # 产品设计Skill
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
