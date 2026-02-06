# Worktree 初始化指南

本指南用于初始化 Dev Workflow 的 Worktree 版本。

## 1. 前置条件

- 已在 `<project-root>/app-main` 初始化业务代码仓库
- 主分支为 `main` 或 `master`

## 2. 创建分支

在 `app-main` 仓库中执行：

```bash
cd <project-root>/app-main

DEFAULT_BRANCH=$(git branch --show-current)
git branch develop $DEFAULT_BRANCH 2>/dev/null || true
git branch test $DEFAULT_BRANCH 2>/dev/null || true
```

## 3. 创建 worktree 工作目录

继续在 `app-main` 仓库中执行：

```bash
git worktree add ../app-develop develop
git worktree add ../app-test test
```

初始化后目录应为：

```text
<project-root>/
├── app-main/
├── app-develop/
└── app-test/
```

## 4. 准备流程文档目录

在工作区根目录执行：

```bash
cd <project-root>
mkdir -p docs/prd docs/test-cases docs/test-reports
```

## 5. 常见检查

- 检查 worktree：`git -C <project-root>/app-main worktree list`
- 检查分支：`git -C <project-root>/app-main branch`
- 检查目录：`ls -la <project-root>`
