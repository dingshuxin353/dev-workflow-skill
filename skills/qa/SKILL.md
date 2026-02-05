---
name: qa
description: 测试经理Skill，负责集成测试、回归测试和生成测试报告。当用户提到"开始测试"、"测试"、"@qa"、"验证功能"、"重测"时使用此skill。测试通过后引导用户验收，验收通过则更新README并合并到main/master分支。
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
3. 用户输入"验收通过"后，执行发布流程

**测试不通过**：
1. 保持状态为 `testing`
2. 更新 `test_report_path`
3. 提示调用 `@dev 修复`

## 验收通过流程

当用户确认"验收通过"后，执行以下步骤：

### Step 1: 更新README

读取当前README.md，根据新功能更新使用说明：

```markdown
## 功能更新

### {feature-name}
{功能描述，面向GitHub用户的使用说明}

**使用方法**：
{使用示例}
```

确保README内容：
- 面向GitHub用户（外部用户）
- 说明新功能的用途
- 提供使用示例
- 语言简洁清晰

### Step 2: 提交README更新

```bash
git add README.md
git commit -m "docs: update README for {feature-name}"
```

### Step 3: 合并到主分支

```bash
# 检测主分支名称
DEFAULT_BRANCH=$(git branch | grep -E '^\*?\s*(main|master)$' | head -1 | tr -d '* ')

git checkout $DEFAULT_BRANCH
git merge test --no-ff -m "feat: merge {feature-name} from test"
```

### Step 4: 打版本标签（可选）

```bash
git tag v{version} -m "{feature-name} release"
```

### Step 5: 更新状态

更新 `.workflow-status.json` 状态为 `done`。

## 完整验收流程示例

```
用户: 验收通过

QA Skill:
  ✅ 验收确认

  正在更新README文档...

  📝 README已更新，新增以下内容：
  - 功能说明：用户登录
  - 使用方法示例

  提交: docs: update README for user-login

  正在执行发布流程...

  1. ✅ 合并test分支到main分支
  2. ✅ 创建版本标签: v1.0.0
  3. ✅ 更新状态为done

  🎉 发布完成！

  【发布信息】
  - 功能: user-login
  - 版本: v1.0.0
  - 时间: 2026-02-05 17:38:00

  如有新需求，可调用 @planner 或 @pm 开始新的迭代
```
