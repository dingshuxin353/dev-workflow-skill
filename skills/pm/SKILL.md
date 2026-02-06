---
name: pm
description: 产品设计 Skill，负责需求分析、PRD 编写和测试用例设计。当用户提到"新需求"、"写PRD"、"产品设计"、"@pm"、"需求分析"、"补充设计"时使用此 skill。适用于 Dev Workflow 的 Worktree 版。
---

# 产品设计 Skill（Worktree 版）

负责需求分析、PRD 编写和测试用例设计。

## 路径约定

- 工作区根目录：`<project-root>`
- 文档目录：`<project-root>/docs/`
- 状态文件：`<project-root>/.workflow-status.json`
- 测试报告目录：`<project-root>/docs/test-reports/`

## 输入来源

1. 从排期获取：读取 `docs/sprint-plan.md`
2. 直接输入：用户直接描述需求
3. 从测试报告获取：读取设计缺陷列表

## 工作模式

### 模式一：新需求设计

触发：`@pm` 或 `新需求`

1. 获取需求（排期或直接输入）
2. 分析需求，提取功能点
3. 生成 PRD 和测试用例
4. 更新状态为 `planning`
5. 用户确认后流转到 `developing`

### 模式二：补充设计

触发：`@pm 补充设计`

1. 读取 `.workflow-status.json` 中的 `test_report_path`
2. 提取“设计缺陷列表”
3. 在 PRD 中补充缺陷对应方案
4. 更新测试用例
5. 状态保持 `testing`，提示调用 `@dev`

## 输出规范

### PRD

- 路径：`<project-root>/docs/prd/{feature-name}.md`
- 命名：kebab-case（例如 `user-login.md`）

建议包含：

1. 需求背景
2. 目标用户
3. 功能描述
4. 用户故事
5. 功能清单
6. 接口设计（如需）
7. 非功能需求
8. 验收标准
9. 开发任务清单
10. 补充设计（若有）

### 测试用例

- 路径：`<project-root>/docs/test-cases/{feature-name}.md`
- 覆盖：正常流程、边界条件、异常场景

## 协作流转

- 新需求设计完成：提示 `@dev`
- 补充设计完成：提示 `@dev` 实现后 `@qa 重测`
