---
name: qa
description: 测试经理Skill，负责集成测试、回归测试和生成测试报告。当用户提到"开始测试"、"测试"、"@qa"、"验证功能"、"重测"时使用此skill。测试通过后引导用户验收，验收通过则合并到main/master分支。
---

# 测试经理 Skill

负责集成测试、回归测试和生成测试报告。

## 分支说明

主分支可能是 `main` 或 `master`，使用前先检测：
```bash
DEFAULT_BRANCH=$(git branch | grep -E '^\*?\s*(main|master)$' | head -1 | tr -d '* ')
```

## 工作模式

### 模式一：首次测试

触发：`@qa` 或 `开始测试`

1. 读取PRD和测试用例
2. 切换到test worktree，拉取最新代码
3. 执行所有测试用例
4. 生成测试报告

### 模式二：重新测试

触发：`@qa 重测`

1. 拉取最新代码
2. 验证已修复的Bug
3. 执行回归测试
4. 更新测试报告

## 测试报告

保存位置：`docs/test-reports/{feature-name}-{date}.md`

```markdown
# {功能名称} 测试报告

## 测试概要
- 测试时间：
- 测试环境：
- 测试版本：

## 测试结果汇总
| 指标 | 数值 |
|------|------|
| 总用例数 | |
| 通过数 | |
| 失败数 | |
| 通过率 | |

## Bug列表
| Bug ID | 描述 | 严重程度 | 状态 |
|--------|------|----------|------|

## 测试结论
□ 通过，建议发布
□ 不通过，需修复后重测
```

## 结果处理

**测试通过**：
1. 更新状态为 `reviewing`
2. 提示用户验收
3. 用户输入"验收通过"后，合并test到main/master

**测试不通过**：
1. 保持状态为 `testing`
2. 更新 `test_report_path`
3. 提示调用 `@dev 修复`

## 验收通过流程

```bash
# 检测主分支名称
DEFAULT_BRANCH=$(git branch | grep -E '^\*?\s*(main|master)$' | head -1 | tr -d '* ')

git checkout $DEFAULT_BRANCH
git merge test --no-ff -m "feat: merge {feature} from test"
git tag v{version}
```

更新状态为 `done`。
