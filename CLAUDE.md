# Dev Workflow 规则

## Git 分支结构

```
main/master  - 生产分支，只接受来自test的合并
develop      - 开发分支，日常开发
test         - 测试分支，接受来自develop的合并
```

注：主分支可能是 `main` 或 `master`，根据项目实际情况确定。

## Worktree 初始化

首次使用时执行：
```bash
# 检测主分支名称
DEFAULT_BRANCH=$(git branch --show-current)

# 创建分支和worktree
git branch develop $DEFAULT_BRANCH 2>/dev/null || true
git branch test $DEFAULT_BRANCH 2>/dev/null || true
git worktree add ../$(basename $(pwd))-develop develop
git worktree add ../$(basename $(pwd))-test test
```

## 文档目录

```
docs/
├── roadmap.md         # 产品路线图
├── sprint-plan.md     # 迭代排期
├── prd/               # PRD文档 ({feature-name}.md)
├── test-cases/        # 测试用例 ({feature-name}.md)
└── test-reports/      # 测试报告 ({feature-name}-{date}.md)
```

## 状态管理

状态文件：`.workflow-status.json`

流转：`planning → developing → testing → reviewing → done`

## 命令

| 命令 | 说明 |
|------|------|
| `@planner` | 产品规划，输出路线图和排期 |
| `@pm 新需求：...` | 产品设计，生成PRD |
| `@dev` | 开始开发 |
| `@dev 修复` | 修复Bug |
| `@qa` | 开始测试 |
| `@qa 重测` | 重新测试 |
| `验收通过` | 合并到主分支 |
