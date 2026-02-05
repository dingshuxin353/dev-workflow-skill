# Dev Workflow 规则

## Git 分支结构

```
main     - 生产分支，只接受来自test的合并
develop  - 开发分支，日常开发
test     - 测试分支，接受来自develop的合并
```

## Worktree 初始化

首次使用时执行：
```bash
git branch develop main 2>/dev/null || true
git branch test main 2>/dev/null || true
git worktree add ../$(basename $(pwd))-develop develop
git worktree add ../$(basename $(pwd))-test test
```

## 文档目录

```
docs/
├── prd/           # PRD文档 ({feature-name}.md)
├── test-cases/    # 测试用例 ({feature-name}.md)
└── test-reports/  # 测试报告 ({feature-name}-{date}.md)
```

## 状态管理

状态文件：`.workflow-status.json`

流转：`planning → developing → testing → reviewing → done`

## 命令

| 命令 | 说明 |
|------|------|
| `@pm 新需求：...` | 需求分析，生成PRD |
| `@dev` | 开始开发 |
| `@dev 修复` | 修复Bug |
| `@qa` | 开始测试 |
| `@qa 重测` | 重新测试 |
| `验收通过` | 合并到main |
