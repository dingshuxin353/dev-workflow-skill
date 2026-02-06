---
name: planner
description: 产品规划 Skill，负责规划产品方向、版本路线图和迭代排期。当用户提到"产品规划"、"版本排期"、"迭代计划"、"@planner"、"规划"、"roadmap"时使用此 skill。适用于 Dev Workflow 的 Worktree 版。
---

# 产品规划 Skill（Worktree 版）

负责规划产品整体方向、迭代节奏和版本排期。

## 路径约定

- 工作区根目录：`<project-root>`
- 文档输出目录：`<project-root>/docs/`
- 状态文件：`<project-root>/.workflow-status.json`

## 工作流程

### Step 1: 了解产品背景

1. 了解产品定位和目标用户
2. 了解当前产品状态和已有功能
3. 收集用户需求和反馈

### Step 2: 制定产品路线图

输出 `<project-root>/docs/roadmap.md`。

建议结构：

```markdown
# 产品路线图

## 产品愿景
{vision}

## 当前版本
v{current_version}

## 版本规划

### v{next_version} - {版本主题}
- 目标：{目标描述}
- 预计周期：{时间范围}
- 核心功能：
  - [ ] 功能1
  - [ ] 功能2
```

### Step 3: 输出迭代排期

输出 `<project-root>/docs/sprint-plan.md`。

建议结构：

```markdown
# 迭代排期

## 当前迭代
- 迭代周期：{start_date} - {end_date}
- 迭代目标：{goal}

## 需求列表
| 优先级 | 需求 | 状态 | 负责人 |
|--------|------|------|--------|
| P0 | {需求1} | 待开发 | - |
| P1 | {需求2} | 待开发 | - |
```

### Step 4: 需求优先级排序

按以下维度评估：

- 价值：用户价值 / 商业价值
- 成本：开发成本 / 时间成本
- 风险：技术风险 / 依赖风险
- 紧急度：时间敏感性

优先级：

- P0：必须做，阻塞性需求
- P1：应该做，核心功能
- P2：可以做，体验优化
- P3：待定，未来考虑

## 协作流转

- 输出排期后，提示调用 `@pm` 进入需求设计
- 排期文档供 `pm/dev/qa` 参考
