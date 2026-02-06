---
name: dev
description: 研发经理 Skill，负责代码开发、单元测试和 Bug 修复。当用户提到"开始开发"、"研发"、"@dev"、"写代码"、"修复Bug"、"修复"时使用此 skill。适用于 Dev Workflow 的 Worktree 版。
---

# 研发经理 Skill（Worktree 版）

负责代码开发、单元测试和 Bug 修复。

## 路径与目录约定

- 工作区根目录：`<project-root>`
- 状态文件：`<project-root>/.workflow-status.json`
- PRD 路径来源：状态文件中的 `prd_path`
- 开发目录：`<project-root>/app-develop`
- 测试目录：`<project-root>/app-test`

## 分支说明

- 主分支：`main` 或 `master`
- 开发分支：`develop`
- 测试分支：`test`

## 工作模式

### 模式一：正常开发

触发：`@dev`

1. 读取状态文件中的 `prd_path`
2. 切换到 `app-develop`（develop worktree）
3. 按任务清单开发
4. 编写并运行单元测试
5. 提交代码：`feat: implement {feature}`
6. 将 develop 合并到 test（在 `app-test` 执行）
7. 更新状态为 `testing`，提示调用 `@qa`

### 模式二：Bug 修复

触发：`@dev 修复`

1. 读取状态文件中的 `test_report_path`
2. 在 `app-develop` 修复 Bug
3. 提交修复：`fix: {bug-id} - {description}`
4. 在 `app-test` 合并 develop
5. 状态保持 `testing`，提示 `@qa 重测`

## Git 操作参考

```bash
# develop worktree 开发
cd <project-root>/app-develop
git add {files}
git commit -m "feat: implement {feature}"

# test worktree 合并
cd <project-root>/app-test
git checkout test
git merge develop --no-ff
```

## 提交规范

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `test`: 测试相关
- `refactor`: 重构
