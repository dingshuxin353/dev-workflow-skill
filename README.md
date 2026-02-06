# Dev Workflow Skill (Worktree 版)

> 面向不熟悉开发流程的团队：你提需求，AI 按规划、设计、开发、测试的完整流程推进，最后你只需验收成品。

## ⚠️ 版本互斥说明（必读）

本仓库是 **Worktree 版本**。它与 Branch 版本在命令层面相同（`@planner` / `@pm` / `@dev` / `@qa`），但底层 Git 工作方式不同。

- 两个版本在同一个项目中 **只能二选一**
- 不要同时安装两套 Skill
- 如果你不想使用 worktree，请改用 Branch 仓库

## 这个版本适合谁

- 你希望开发、测试并行隔离，减少相互干扰
- 你接受维护 `main/develop/test` 三个代码目录
- 你项目涉及复杂调试，想保留稳定的测试工作副本

## 核心能力

- **四角色协作**：Planner（规划）、PM（设计）、Dev（研发）、QA（测试）
- **Worktree 隔离**：`app-main`、`app-develop`、`app-test` 并行
- **状态闭环**：`planning → developing → testing → reviewing → done`
- **缺陷分流**：代码问题走 `@dev 修复`，设计问题走 `@pm 补充设计`
- **验收收口**：验收通过后合并到主分支并更新状态

## 工作区标准结构（避免歧义）

> 重点：`CLAUDE.md`、`.claude/`、`docs/` 是工作区资产，不进代码仓库。

```text
<project-root>/
├── CLAUDE.md                 # 工作区规则（不进 git）
├── .claude/                  # 本地 skill 安装目录（不进 git）
│   └── skills/
├── docs/                     # PRD/用例/测试报告（不进 git）
├── .workflow-status.json     # 流程状态（不进 git）
├── app-main/                 # 主代码仓库（main/master）
├── app-develop/              # worktree: develop
└── app-test/                 # worktree: test
```

## Git 分支结构

```text
main/master  - 生产分支，仅接受来自 test 的合并
develop      - 开发分支，日常开发
test         - 测试分支，接受来自 develop 的合并
```

## 安装

### 1) 安装 skill

```bash
# 在你的工作区中（非代码仓库内）
mkdir -p .claude/skills
cp -r /path/to/dev-flow-worktree/skills/* .claude/skills/
```

### 2) 放置规则文件

```bash
cp /path/to/dev-flow-worktree/CLAUDE.md <project-root>/CLAUDE.md
```

### 3) 初始化流程目录

```bash
cd <project-root>
mkdir -p docs/prd docs/test-cases docs/test-reports
```

### 4) 初始化 worktree（独立文档）

Worktree 初始化命令已拆分到独立文档，请按该文档执行：

- `guides/worktree-init.md`

## 使用流程

```bash
# 1. 规划与排期
@planner

# 2. 需求设计与测试用例
@pm

# 3. 开发实现
@dev

# 4. 测试与报告
@qa

# 5. 验收通过
验收通过
```

## 状态机

状态保存在 `<project-root>/.workflow-status.json`：

```text
planning → developing → testing → reviewing → done
               ↑            │
               └── fixing ──┘
                     │
               ↑     │
               └─────┘ (设计缺陷补充)
```

## 产物说明

所有文档都落在 `<project-root>/docs/`（不进代码仓库）：

- `docs/roadmap.md`
- `docs/sprint-plan.md`
- `docs/prd/*.md`
- `docs/test-cases/*.md`
- `docs/test-reports/*.md`

## FAQ

### Q1: 为什么 docs 不放在代码仓库里？

A: 流程文档是“工作区协作资产”，和业务代码生命周期不同。分离后能减少代码仓库噪音，也避免误提交。

### Q2: 和 Branch 版本能一起用吗？

A: 不能。两个版本命令一样但底层流转不同，在同一项目里会互相覆盖流程上下文。

### Q3: 初始化 worktree 命令在哪里？

A: 见独立文档 `guides/worktree-init.md`。

## License

MIT
