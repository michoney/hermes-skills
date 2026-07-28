---
name: darwin
description: 进化 Skill — 达尔文 Skill。自动发现 Skill 缺陷，触发 skill_manage patch/edit，推动 Skill 系统自我迭代。
author: 超哥
version: 0.1.0
tags: [evolution, self-improve, skill-management, meta]
---

# Darwin Skill（达尔文）

> 适者生存，进化不止。让 Skill 系统从每次使用中学习，自动修正和完善。

## 定位

Skill 使用反馈 → 缺陷识别 → 自动 patch → 系统进化

## 触发条件

- 一个 Skill 被调用后产生了**错误、遗漏、或用户纠正**
- 用户说"darwin""达尔文""进化""skill 有问题"
- Agent 自我检测发现某个 Skill 的 SKILL.md 过时/不准/不完整
- 任务完成后的复盘：某 Skill 步骤有 bug

## 工作流程

1. **触发检测** — 识别"哪个 Skill"出了"什么问题"
2. **缺陷分析** — 分类缺陷类型：
   - 步骤缺失（漏了某个步骤）
   - 命令过时（命令/参数已变更）
   - 边界错误（特殊场景没覆盖）
   - 描述不准（实际行为与文档不符）
3. **生成 patch** — 用 skill_manage(action='patch') 修复
4. **验证** — 再次触发该 Skill，确认修复有效
5. **记录进化** — 在 SKILL.md 底部追加进化日志

## 缺陷类型对照

| 类型 | 典型信号 | 修复方式 |
|------|----------|----------|
| 步骤缺失 | 用户说"还没完""漏了一步" | patch SKILL.md 补步骤 |
| 命令过时 | 命令报错 / 路径不对 | patch 更新命令/路径 |
| 边界错误 | 特殊输入崩了 | patch 加边界处理 |
| 描述不准 | 实际与文档不符 | patch 修正描述 |
| 依赖变更 | npm/package 版本升级 | patch 更新依赖说明 |

## 进化日志模板

追加在 SKILL.md 末尾：

```markdown
## 进化日志
- {YYYY-MM-DD}: {修复了什么}（触发源：{来源}）
```

## 依赖

- skill_manage: 执行 patch/edit
- 用户纠正或任务失败记录

## 注意事项

- **不**在 Darwin 自身触发时修改 Darwin（避免无限递归）
- 每次 patch 前先 `skill_view` 确认当前版本
- 重要修复需向用户报告变更内容
