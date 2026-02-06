# Dev Workflow 执行规则（Worktree 版）

## 作用范围

本文件只定义流程执行规则，不包含版本说明、目录结构或初始化步骤。

## 文档产物

所有流程文档输出到 `<project-root>/docs/`：

- `docs/roadmap.md`
- `docs/sprint-plan.md`
- `docs/prd/*.md`
- `docs/test-cases/*.md`
- `docs/test-reports/*.md`

## 状态管理

状态文件：`<project-root>/.workflow-status.json`

流转：`planning → developing → testing → reviewing → done`

## 命令约定

| 命令 | 说明 |
|------|------|
| `@planner` | 产品规划，输出路线图与排期 |
| `@pm 新需求：...` | 产品设计，生成 PRD 与测试用例 |
| `@pm 补充设计` | 根据测试反馈补充 PRD |
| `@dev` | 进入开发实现 |
| `@dev 修复` | 修复测试报告中的 Bug |
| `@qa` | 开始测试并输出测试报告 |
| `@qa 重测` | 对修复项与补充设计进行重测 |
| `验收通过` | 合并到主分支并收口流程 |

## 角色协作规则

- `@planner` 完成后提示进入 `@pm`
- `@pm` 完成后提示进入 `@dev`
- `@dev` 完成后提示进入 `@qa`
- `@qa` 若发现代码问题，回流 `@dev 修复`
- `@qa` 若发现设计缺陷，回流 `@pm 补充设计` 后再 `@dev` 与 `@qa 重测`
