# Dev Workflow Skill

研发流程协作技能组 - 产品、研发、测试三角色协作的自动化工作流

## 概述

本项目包含三个协作Skill，实现从需求到上线的全流程自动化：

```
需求 → PM Skill → PRD/测试用例 → Dev Skill → 代码开发 → QA Skill → 测试验收 → 上线
```

## 三个角色

| 角色 | Skill | 职责 | 工作分支 |
|------|-------|------|----------|
| 产品经理 | pm-skill | PRD编写、测试用例设计 | main |
| 研发经理 | dev-skill | 代码开发、单元测试 | develop |
| 测试经理 | qa-skill | 集成测试、验收报告 | test |

## 工作流程

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  需求    │────▶│ PM Skill│────▶│Dev Skill│────▶│QA Skill │
│         │     │  (PRD)  │     │ (开发)   │     │ (测试)  │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
                                                     │
                                                     ▼
                                              ┌─────────┐
                                              │用户验收  │
                                              │合并main │
                                              └─────────┘
```

## Git Worktree 结构

```
workspace/
├── project/              # main分支 (生产)
├── project-develop/      # develop分支 (开发)
└── project-test/         # test分支 (测试)
```

## 使用方式

```bash
# 产品经理：分析需求，生成PRD
@pm 新需求：实现用户登录功能

# 研发经理：开始开发
@dev 开始开发

# 测试经理：开始测试
@qa 开始测试

# 用户验收通过
验收通过
```

## 项目结构

```
dev-workflow-skill/
├── README.md
├── src/
│   ├── pm_skill.py           # 产品经理Skill
│   ├── dev_skill.py          # 研发经理Skill
│   ├── qa_skill.py           # 测试经理Skill
│   ├── git_manager.py        # Git操作封装
│   └── worktree_manager.py   # Worktree管理
├── skills/
│   ├── pm.md                 # PM Skill定义
│   ├── dev.md                # Dev Skill定义
│   └── qa.md                 # QA Skill定义
├── templates/
│   ├── prd_template.md
│   ├── test_case_template.md
│   └── test_report_template.md
├── docs/
│   ├── prd/
│   ├── test-cases/
│   └── test-reports/
└── tests/
```

## 开发状态

- [x] PRD设计
- [ ] PM Skill实现
- [ ] Dev Skill实现
- [ ] QA Skill实现
- [ ] Git Worktree管理
- [ ] 流程集成测试

## 相关文档

- [PRD文档](../PRD/dev-workflow-skill/PRD.md)

## License

MIT
