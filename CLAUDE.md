# Dev Workflow Skill - Claude Code 规则

## 项目概述

本项目是一个三角色协作的研发流程Skill，包含产品经理(PM)、研发经理(Dev)、测试经理(QA)三个角色。

## Git Worktree 规则

### 分支结构
```
main     - 生产分支，只接受来自test的合并
develop  - 开发分支，日常开发在此进行
test     - 测试分支，接受来自develop的合并
```

### Worktree 初始化
当用户首次使用本Skill时，需要检查并初始化worktree：
```bash
# 检查是否已有worktree
git worktree list

# 如果没有，创建develop和test分支的worktree
git branch develop main 2>/dev/null || true
git branch test main 2>/dev/null || true
git worktree add ../$(basename $(pwd))-develop develop
git worktree add ../$(basename $(pwd))-test test
```

### 分支保护规则
- **禁止**直接在main分支上开发
- **禁止**跳过test直接从develop合并到main
- 所有代码必须经过test分支测试后才能合并到main

## 文档存放规则

### 目录结构
```
docs/
├── prd/                    # PRD文档
│   └── {feature-name}.md   # 以功能名命名
├── test-cases/             # 测试用例
│   └── {feature-name}.md   # 与PRD同名
└── test-reports/           # 测试报告
    └── {feature-name}-{date}.md  # 功能名+日期
```

### 命名规范
- 功能名使用kebab-case（如：user-login, order-management）
- 日期格式：YYYYMMDD
- 示例：`user-login.md`, `user-login-20260205.md`

## 流程状态管理

### 状态文件
在项目根目录维护 `.workflow-status.json` 文件：
```json
{
  "current_feature": "user-login",
  "status": "testing",  // planning | developing | testing | reviewing | done
  "prd_path": "docs/prd/user-login.md",
  "test_cases_path": "docs/test-cases/user-login.md",
  "created_at": "2026-02-05T10:00:00Z",
  "updated_at": "2026-02-05T12:00:00Z"
}
```

### 状态流转
```
planning → developing → testing → reviewing → done
    ↑          ↓           ↓
    └──────────┴───────────┘  (如有问题可回退)
```

## Skill 调用规则

### PM Skill (产品经理)
**触发条件**：
- 用户说"新需求"、"写PRD"、"@pm"等
- 当前状态为空或done

**职责**：
1. 分析用户需求
2. 生成PRD文档到 `docs/prd/`
3. 生成测试用例到 `docs/test-cases/`
4. 更新状态为 `planning`
5. 询问用户确认后，状态变为 `developing`

**输出**：
- PRD文档
- 测试用例文档
- 开发任务清单

### Dev Skill (研发经理)
**触发条件**：
- 用户说"开始开发"、"@dev"等
- 当前状态为 `developing`

**职责**：
1. 读取PRD和任务清单
2. 切换到develop worktree
3. 进行代码开发
4. 编写单元测试
5. 提交代码到develop分支
6. 合并develop到test分支
7. 更新状态为 `testing`

**代码规范**：
- 遵循项目现有代码风格
- commit message使用Conventional Commits格式
- 每个功能点独立commit

### QA Skill (测试经理)
**触发条件**：
- 用户说"开始测试"、"@qa"等
- 当前状态为 `testing`

**职责**：
1. 读取PRD和测试用例
2. 切换到test worktree
3. 执行测试用例
4. 生成测试报告到 `docs/test-reports/`
5. 如果通过，更新状态为 `reviewing`
6. 如果失败，通知研发修复

## 验收与发布规则

### 验收流程
1. QA测试通过后，提示用户验收
2. 用户确认"验收通过"后：
   - 合并test分支到main分支
   - 打版本tag（如有需要）
   - 更新状态为 `done`
   - 清理feature分支（可选）

### 合并命令
```bash
# 在main worktree执行
git checkout main
git merge test --no-ff -m "feat: merge {feature-name} from test"
git tag v{version} -m "{feature-name} release"
```

## Commit Message 规范

使用 Conventional Commits 格式：
```
<type>(<scope>): <subject>

<body>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Type**：
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `test`: 测试相关
- `refactor`: 重构
- `chore`: 其他

## 错误处理

### Worktree冲突
如果遇到worktree冲突：
1. 先尝试 `git stash` 保存当前更改
2. 解决冲突后 `git stash pop`
3. 如果无法解决，提示用户手动处理

### 状态不一致
如果状态文件与实际不符：
1. 检查各分支的最新提交
2. 检查文档是否存在
3. 根据实际情况修正状态文件

## 快捷命令

| 命令 | 说明 |
|------|------|
| `@pm 新需求：...` | 开始需求分析 |
| `@dev` | 开始开发 |
| `@qa` | 开始测试 |
| `@status` | 查看当前状态 |
| `验收通过` | 确认验收并发布 |
