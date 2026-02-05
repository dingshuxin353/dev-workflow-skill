---
name: dev
description: 研发经理Skill，负责代码开发、单元测试和Bug修复。当用户提到"开始开发"、"研发"、"@dev"、"写代码"、"修复Bug"、"修复"时使用此skill。支持两种模式：正常开发模式和Bug修复模式。
---

# 研发经理 Skill

负责代码开发、单元测试编写和Bug修复。

## 分支说明

主分支可能是 `main` 或 `master`，使用前先检测：
```bash
git branch | grep -E '^\*?\s*(main|master)$' | head -1 | tr -d '* '
```

## 工作模式

### 模式一：正常开发

触发：`@dev` 或 `开始开发`

1. 读取PRD文档 (`.workflow-status.json` 中的 `prd_path`)
2. 切换到develop worktree
3. 按任务清单逐个开发
4. 编写单元测试
5. 提交代码：`git commit -m "feat: implement {feature}"`
6. 合并到test分支

### 模式二：Bug修复

触发：`@dev 修复`

1. 读取测试报告 (`.workflow-status.json` 中的 `test_report_path`)
2. 切换到develop worktree
3. 逐个修复Bug
4. 提交修复：`git commit -m "fix: {bug-id} - {description}"`
5. 合并到test分支

## Git操作

```bash
# 切换到develop worktree
cd {project}-develop

# 提交代码
git add {files}
git commit -m "feat: implement {feature}"

# 合并到test
git checkout test
git merge develop --no-ff
```

## 提交规范

- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `test`: 测试相关
- `refactor`: 重构

## 状态更新

开发/修复完成后，保持状态为 `testing`，提示调用 `@qa` 测试。
