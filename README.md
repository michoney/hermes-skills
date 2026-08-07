# Hermes Skills

Hermes Agent 自定义技能集，中国神话 + 科学史双线命名体系。

## 三大技能

| 技能 | 中文名 | 定位 | 一句话 |
|------|--------|------|--------|
| **Cangjie** | 仓颉 | 长文本蒸馏 | 把书、视频、播客压成知识卡片 |
| **Nuwa** | 女娲 | 人物蒸馏 | 把人物信息建成结构化档案 |
| **Darwin** | 达尔文 | 进化 | Skill 系统自动修复自我迭代 |
| **Munger** | 芒格 | 决策建议 | 芒格风控官思维 — 逆向分析/激励映射/偏见审计，给方案反驳或建议 |
| **Munger Advisor** | 芒格建议者 | 决策建议 | 平等建议者模式 — 用芒格思维反驳或建议，不端导师架子 |
| **Gallup** | 盖洛普 | 优势识别 | 34项天赋主题识别与应用，扬长避短 |
| **Duan** | 段永平 | 经营投资 | 本分/平常心/不为清单/敢为天下后，企业价值评估 |
| **Trio** | 三视角 | 决策顾问 | 芒格(风险)+段永平(经营)+盖洛普(优势)三视角分析，超哥拍板 |
| **WeChat** | 公众号抓取 | 内容采集 | 微信公众号文章抓取 — 单篇/递归/每日定时，搜狗搜索+解跳转 |

## 部署

将各目录完整复制到 `~/.hermes/skills/` 对应目录即可（SKILL.md + references/scripts/templates 一起）：

```bash
cp -r cangjie ~/.hermes/skills/cangjie-skill
cp -r nuwa ~/.hermes/skills/nuwa-skill
cp -r darwin ~/.hermes/skills/darwin-skill
```

或通过 Hermes Agent 直接安装：

```
技能安装路径: ~/.hermes/skills/{cangjie-skill,nuwa-skill,darwin-skill,munger-risk-officer,gallup-strengths,duan-yongping,trio-advisor,wechat-article-scraper}
```

## 触发方式

- **Cangjie**: 发长文本、视频/播客链接，或说"蒸馏""仓颉"
- **Nuwa**: 发人物信息、说"建档""女娲"
- **Darwin**: 某个 Skill 出问题自动触发修正

## 技术栈

- Hermes Agent (Nous Research)
- Obsidian Vault (`~/Documents/Obsidian Vault`)
- 中国神话 + 达尔文进化论 双线命名
