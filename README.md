# Dev Workflow Skill

一套基于 Claude Code 的四角色协作工作流 Skill，实现产品规划、设计、研发、测试的自动化闭环。

## 特性

- **四角色分工**：Planner（规划）、PM（设计）、Dev（研发）、QA（测试）
- **Git Worktree 隔离**：develop、test 分支独立工作目录，互不干扰
- **状态自动流转**：planning → developing → testing → reviewing → done
- **Bug 修复闭环**：测试发现 Bug → 开发修复 → 重新测试
- **设计缺陷反馈**：测试发现设计问题 → PM 补充设计 → 开发实现 → 重新测试
- **自动化验收**：测试通过后更新 README，合并代码到主分支

## 工作流程

<img width="4817" height="1429" alt="微信图片_20260205193827_35048_14 (1)" src="https://github.com/user-attachments/assets/72f76e5b-d247-4445-ba01-6106b0e68725" />


## 四个 Skill

| Skill | 触发词 | 职责 | 输出 |
|-------|--------|------|------|
| **planner** | `@planner`, `规划` | 产品路线图、迭代排期 | `docs/roadmap.md`, `docs/sprint-plan.md` |
| **pm** | `@pm`, `新需求`, `补充设计` | PRD设计、测试用例、设计补充 | `docs/prd/*.md`, `docs/test-cases/*.md` |
| **dev** | `@dev`, `修复` | 代码开发、单元测试、Bug修复 | 代码实现 |
| **qa** | `@qa`, `重测` | 集成测试、测试报告、验收引导 | `docs/test-reports/*.md` |

## 安装

### 方式一：复制到全局目录（推荐）

```bash
# 克隆仓库
git clone https://github.com/your-username/dev-workflow-skill.git
cd dev-workflow-skill

# 复制 skill 文件夹到 Claude Code 全局目录
cp -r skills/planner ~/.claude/skills/
cp -r skills/pm ~/.claude/skills/
cp -r skills/dev ~/.claude/skills/
cp -r skills/qa ~/.claude/skills/
```

### 方式二：项目级安装

将 `skills/` 目录复制到你的项目中：

```bash
cp -r skills/ your-project/.claude/skills/
```

## 使用指南

### Step 1: 配置目标项目

将 `CLAUDE.md` 复制到你的项目根目录：

```bash
cp CLAUDE.md your-project/
```

### Step 2: 初始化文档目录

```bash
cd your-project
mkdir -p docs/prd docs/test-cases docs/test-reports
```

### Step 3: 初始化 Git Worktree

```bash
# 自动检测主分支（main 或 master）
DEFAULT_BRANCH=$(git branch --show-current)

# 创建 develop 和 test 分支
git branch develop $DEFAULT_BRANCH 2>/dev/null || true
git branch test $DEFAULT_BRANCH 2>/dev/null || true

# 创建 worktree（独立工作目录）
git worktree add ../$(basename $(pwd))-develop develop
git worktree add ../$(basename $(pwd))-test test
```

### Step 4: 开始工作流

```bash
# 1. 产品规划：制定路线图和迭代排期
@planner

# 2. 产品设计：根据排期生成 PRD 和测试用例
@pm

# 3. 研发开发：实现功能代码
@dev

# 4. 测试验证：执行测试并生成报告
@qa

# 5. 验收通过后自动合并代码
验收通过
```

## 详细使用场景

### 场景一：新功能开发

```bash
# 直接描述需求，跳过规划阶段
@pm 新需求：实现用户登录功能，支持邮箱和手机号登录

# PM 生成 PRD 和测试用例后
@dev

# 开发完成后
@qa

# 测试通过，用户验收
验收通过
```

### 场景二：Bug 修复

```bash
# 测试发现 Bug 后，查看测试报告
@dev 修复

# 修复完成后重新测试
@qa 重测
```

### 场景三：设计缺陷补充

```bash
# 测试发现设计缺陷（PRD 未覆盖的场景）
@pm 补充设计

# PM 补充 PRD 后，开发实现
@dev

# 重新测试
@qa 重测
```

### 场景四：完整迭代流程

```bash
# 1. 规划本迭代要做的功能
@planner

# 2. 选择排期中的需求进行设计
@pm

# 3. 开发
@dev

# 4. 测试
@qa

# 5. 如有问题，循环修复
@dev 修复  # Bug
@pm 补充设计  # 设计缺陷

# 6. 验收上线
验收通过
```

## 状态流转

工作流状态保存在 `.workflow-status.json` 文件中：

```
planning → developing → testing → reviewing → done
               ↑            │
               └── fixing ──┘
                     │
               ↑     │
               └─────┘ (设计缺陷补充)
```

| 状态 | 说明 | 下一步 |
|------|------|--------|
| `planning` | PRD 设计中 | `@dev` 开始开发 |
| `developing` | 开发中 | `@qa` 开始测试 |
| `testing` | 测试中 | 验收 或 `@dev 修复` |
| `reviewing` | 待验收 | `验收通过` |
| `done` | 已完成 | - |

## 项目结构

```
dev-workflow-skill/
├── README.md                 # 本文档
├── CLAUDE.md                 # 项目规则（复制到目标项目）
├── .gitignore
└── skills/
    ├── planner/
    │   └── SKILL.md          # 产品规划 Skill
    ├── pm/
    │   └── SKILL.md          # 产品设计 Skill
    ├── dev/
    │   └── SKILL.md          # 研发经理 Skill
    └── qa/
        └── SKILL.md          # 测试经理 Skill
```

## Git 分支策略

| 分支 | 用途 | Worktree 目录 |
|------|------|---------------|
| `main`/`master` | 生产代码 | `project/` |
| `develop` | 开发分支 | `project-develop/` |
| `test` | 测试分支 | `project-test/` |

## 测试报告说明

测试报告包含以下关键信息：

- **测试结果汇总**：通过率、失败用例
- **Bug 列表**：代码层面的问题，需 `@dev 修复`
- **设计缺陷列表**：PRD 层面的问题，需 `@pm 补充设计`
- **验收使用说明**：环境配置、必填项、操作步骤

## FAQ

### Q: main 和 master 分支如何兼容？

所有 Skill 都会自动检测主分支名称：

```bash
DEFAULT_BRANCH=$(git branch | grep -E '^\*?\s*(main|master)$' | head -1 | tr -d '* ')
```

### Q: 如何跳过规划阶段？

直接使用 `@pm 新需求：xxx` 描述需求即可。

### Q: Bug 和设计缺陷有什么区别？

- **Bug**：代码未按 PRD 实现，或程序错误 → `@dev 修复`
- **设计缺陷**：PRD 未覆盖的场景，或交互不合理 → `@pm 补充设计`

### Q: 验收通过后会做什么？

1. 更新 README.md（面向 GitHub 用户的使用说明）
2. 提交更新
3. 合并 test 分支到 main/master
4. 更新状态为 done

## License

MIT
