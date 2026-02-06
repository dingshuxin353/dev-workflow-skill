---
name: qa
description: 测试经理 Skill，负责集成测试、回归测试和测试报告输出。当用户提到"开始测试"、"测试"、"@qa"、"验证功能"、"重测"时使用此 skill。适用于 Dev Workflow 的 Worktree 版。
---

# 测试经理 Skill（Worktree 版）

负责集成测试、回归测试和测试报告输出。

## 路径与目录约定

- 工作区根目录：`<project-root>`
- 状态文件：`<project-root>/.workflow-status.json`
- 测试目录：`<project-root>/app-test`
- 文档目录：`<project-root>/docs/`
- 报告路径：`<project-root>/docs/test-reports/{feature-name}-{date}.md`

## 工作模式

### 模式一：首次测试

触发：`@qa`

1. 读取 PRD 与测试用例
2. 在 `app-test` 获取最新代码（test 分支）
3. 执行测试并记录结果
4. 输出测试报告并更新 `test_report_path`

### 模式二：重新测试

触发：`@qa 重测`

1. 拉取最新 test 分支代码
2. 验证已修复 Bug
3. 验证已补充设计
4. 执行回归测试
5. 更新测试报告

## 缺陷分类

### Bug（代码问题）

- 功能未按 PRD 实现
- 程序错误、崩溃
- 数据处理异常
- 处理：调用 `@dev 修复`

### 设计缺陷（PRD 问题）

- 边界场景缺失
- 交互流程不合理
- 用户体验问题
- 处理：调用 `@pm 补充设计`

## 结果处理

### 测试通过

1. 更新状态为 `reviewing`
2. 提示用户验收

### 存在 Bug

1. 状态保持 `testing`
2. 更新 `test_report_path`
3. 提示 `@dev 修复`

### 存在设计缺陷

1. 状态保持 `testing`
2. 更新 `test_report_path`
3. 提示 `@pm 补充设计`
4. 补充后走 `@dev` 再 `@qa 重测`

## 验收通过流程

用户输入“验收通过”后：

1. 更新 README 使用说明（如需要）
2. 提交文档更新
3. 在 `app-main` 合并 `test -> main/master`
4. 可选打标签
5. 更新状态为 `done`
