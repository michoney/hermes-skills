---
name: cangjie
description: 长文本蒸馏 — 仓颉 Skill。将书、视频、播客等长内容压缩为结构化知识条目，存入 Obsidian vault。
author: 超哥
version: 0.1.0
tags: [distill, long-form, summarization, knowledge-capture]
---

# Cangjie Skill（仓颉）

> 仓颉造字，万物可记。将长文本/视频/播客蒸馏为结构化知识。

## 定位

长内容 → 精炼知识卡片 → 存入 Obsidian vault

## 触发条件

- 用户发了一段长文本（>500字），或明确说"蒸馏""总结成知识""存笔记"
- 用户提供视频/播客链接，要求提取知识点
- 用户说"cangjie""仓颉""长文本蒸馏"

## 工作流程

1. **接收输入** — 识别输入类型：纯文本 / YouTube 链接 / 播客链接 / 文件路径
2. **提取原文** — 文本直接取；视频调用 YouTube transcript；播客调 TTS/转写
3. **蒸馏** — 按模板提取：
   - 核心观点（≤5条）
   - 关键术语/人名/时间
   - 可操作要点
   - 关联链接
4. **写入 vault** — 生成 `.md` 文件，存入 Obsidian vault（路径见记忆）
5. **返回卡片** — 向用户展示知识卡片摘要 + vault 路径

## 输出模板

```markdown
# {标题}

> 来源：{原始链接/文件名}
> 日期：{YYYY-MM-DD}

## 核心观点
- 

## 关键信息

## 可操作要点
- 

## 关联
- 

---
_由 Cangjie Skill 蒸馏 | {YYYY-MM-DD}_
```

## 依赖

- Obsidian vault 路径: `~/Documents/Obsidian Vault`（记忆）
- YouTube transcript: `youtube-content` skill
- TTS/语音: 系统 tts tool

## 注意事项

- 超过 5000 字的长文建议分段处理
- 视频链接优先用 YouTube transcript 而非逐帧分析
- 蒸馏产物必须实际写入 vault，不能只返回文本
