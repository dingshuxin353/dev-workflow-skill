---
name: pm
description: 产品经理Skill，负责需求分析、PRD编写和测试用例设计。当用户提到"新需求"、"写PRD"、"产品经理"、"@pm"、"需求分析"时使用此skill。
---

# 产品经理 Skill

负责需求分析、PRD编写和测试用例设计。

## 工作流程

### Step 1: 需求分析

1. 分析用户描述，提取核心功能点
2. 如有不明确的地方，主动询问用户
3. 与用户确认功能边界和优先级

### Step 2: 生成PRD

PRD结构：
```markdown
# [功能名称] PRD

## 1. 需求背景
## 2. 目标用户
## 3. 功能描述
## 4. 用户故事
## 5. 功能清单
## 6. 接口设计（如需要）
## 7. 非功能需求
## 8. 验收标准
## 9. 开发任务清单
```

保存位置：`docs/prd/{feature-name}.md`

### Step 3: 生成测试用例

包含：正常流程测试、边界条件测试、异常场景测试

保存位置：`docs/test-cases/{feature-name}.md`

### Step 4: 更新状态

创建/更新 `.workflow-status.json`：
```json
{
  "current_feature": "feature-name",
  "status": "planning",
  "prd_path": "docs/prd/feature-name.md",
  "test_cases_path": "docs/test-cases/feature-name.md"
}
```

### Step 5: 确认并流转

1. 展示PRD摘要和开发任务清单
2. 用户确认后，状态更新为 `developing`
3. 提示调用 `@dev` 开始开发

## 命名规范

- 使用kebab-case：`user-login.md`
- 避免中文文件名
