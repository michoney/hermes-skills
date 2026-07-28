# Hermes Skills

Hermes Agent 自定义技能集，中国神话 + 科学史双线命名体系。

## 三大技能

| 技能 | 中文名 | 定位 | 一句话 |
|------|--------|------|--------|
| **Cangjie** | 仓颉 | 长文本蒸馏 | 把书、视频、播客压成知识卡片 |
| **Nuwa** | 女娲 | 人物蒸馏 | 把人物信息建成结构化档案 |
| **Darwin** | 达尔文 | 进化 | Skill 系统自动修复自我迭代 |

## 部署

将各目录 `SKILL.md` 复制到 `~/.hermes/skills/ai-agent-generator/` 对应目录即可：

```bash
cp cangjie/SKILL.md ~/.hermes/skills/ai-agent-generator/cangjie/SKILL.md
cp nuwa/SKILL.md ~/.hermes/skills/ai-agent-generator/nuwa/SKILL.md
cp darwin/SKILL.md ~/.hermes/skills/ai-agent-generator/darwin/SKILL.md
```

或通过 Hermes Agent 直接安装：

```
技能安装路径: ~/.hermes/skills/ai-agent-generator/{cangjie,nuwa,darwin}
```

## 触发方式

- **Cangjie**: 发长文本、视频/播客链接，或说"蒸馏""仓颉"
- **Nuwa**: 发人物信息、说"建档""女娲"
- **Darwin**: 某个 Skill 出问题自动触发修正

## 技术栈

- Hermes Agent (Nous Research)
- Obsidian Vault (`~/Documents/Obsidian Vault`)
- 中国神话 + 达尔文进化论 双线命名
