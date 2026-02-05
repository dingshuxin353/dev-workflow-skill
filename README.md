# Dev Workflow Skill

研发流程协作技能组 - 产品、研发、测试三角色协作的自动化工作流

## 概述

本项目包含三个协作Skill，实现从需求到上线的全流程自动化：

```
需求 → PM Skill → PRD/测试用例 → Dev Skill → 代码开发 → QA Skill → 测试验收 → 上线
```

## 三个角色

| 角色 | Skill | 触发词 | 工作分支 |
|------|-------|--------|----------|
| 产品经理 | pm | `@pm`, `新需求`, `写PRD` | main |
| 研发经理 | dev | `@dev`, `开始开发`, `修复Bug` | develop |
| 测试经理 | qa | `@qa`, `开始测试`, `重测` | test |

## 工作流程

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  需求    │────▶│ PM Skill│────▶│Dev Skill│────▶│QA Skill │
│         │     │  (PRD)  │     │ (开发)   │     │ (测试)  │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
                                      ↑              │
                                      │   Bug修复    │
                                      └──────────────┘
                                                     │
                                                     ▼
                                              ┌─────────┐
                                              │用户验收  │
                                              │合并main │
                                              └─────────┘
```

## 状态流转

```
planning → developing → testing → reviewing → done
                ↑           │
                │   (Bug)   │
                └───────────┘
```

## Git Worktree 结构

```
workspace/
├── project/              # main分支 (生产)
├── project-develop/      # develop分支 (开发)
└── project-test/         # test分支 (测试)
```

## 快速开始

### 1. 初始化Worktree

首次使用时，需要初始化Git Worktree：

```bash
# 在项目根目录执行
git branch develop main
git branch test main
git worktree add ../$(basename $(pwd))-develop develop
git worktree add ../$(basename $(pwd))-test test
```

### 2. 使用流程

```bash
# 1. 产品经理：分析需求，生成PRD
@pm 新需求：实现用户登录功能

# 2. 研发经理：开始开发
@dev

# 3. 测试经理：开始测试
@qa

# 4. 如有Bug，修复后重测
@dev 修复
@qa 重测

# 5. 用户验收通过
验收通过
```

## 项目结构

```
dev-workflow-skill/
├── README.md
├── CLAUDE.md                 # Claude Code规则
├── .workflow-status.json     # 流程状态文件
├── src/
│   ├── __init__.py
│   ├── workflow_status.py    # 状态管理
│   ├── git_manager.py        # Git操作
│   ├── worktree_manager.py   # Worktree管理
│   └── utils.py              # 工具函数
├── skills/
│   ├── pm.md                 # PM Skill定义
│   ├── dev.md                # Dev Skill定义
│   └── qa.md                 # QA Skill定义
├── templates/
│   ├── prd_template.md
│   ├── test_case_template.md
│   └── test_report_template.md
├── docs/
│   ├── prd/                  # PRD文档
│   ├── test-cases/           # 测试用例
│   └── test-reports/         # 测试报告
└── tests/
```

## 命令速查

| 命令 | 说明 | 状态要求 |
|------|------|----------|
| `@pm 新需求：...` | 开始需求分析 | 空/done |
| `@dev` | 开始开发 | developing |
| `@dev 修复` | 修复Bug | testing |
| `@qa` | 开始测试 | testing |
| `@qa 重测` | 重新测试 | testing |
| `@status` | 查看当前状态 | 任意 |
| `验收通过` | 确认验收并发布 | reviewing |

## 开发状态

- [x] PRD设计
- [x] CLAUDE.md规则
- [x] 核心代码模块
- [x] Skill定义文件
- [x] 文档模板
- [ ] 集成测试
- [ ] 使用文档

## 相关文档

- [PRD文档](../PRD/dev-workflow-skill/PRD.md)

## License

MIT
