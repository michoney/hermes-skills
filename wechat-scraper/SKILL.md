---
name: wechat-article-scraper
description: 抓取微信公众号文章 — 单篇链接转 markdown，或从种子文章递归抓整个公众号。触发词：公众号抓取/公众号文章/微信文章下载/抓"某号"的文章/批量抓公众号。已知坑：搜狗微信收录不全+主页有验证墙，正解是文章页内同 __biz 链接递归。
version: 1.0.0
author: Agent
platforms: [macos, linux, windows]
---

# 微信公众号文章抓取

## 触发
用户要抓公众号文章：单篇（给 mp.weixin.qq.com/s/xxx 链接出 markdown），或整号（"抓天龙大义的文章"）。

## 工具（已就位，`~/Desktop/AI交互/tools/`）

- `wechat_fetcher.py <URL> [更多URL...]` 或 `wechat_fetcher.py urls.txt` — 单篇/批量，输出 `wechat_articles/<标题>.md`
- `wechat_recursive.py <种子URL> [最大篇数=50]` — 从一篇文章顺藤摸瓜抓整个公众号，状态存 `wechat_state.json`（去重+增量，重跑自动续）

两脚本都用纯 `urllib`（requests 非必需），UA 用桌面 Chrome。抓取正文前 30 分钟被反爬概率低；批量建议 `time.sleep(2)` 间隔。

## 核心方法：文章页递归（正解）

**不要**从公众号主页入手 —— `mp.weixin.qq.com/mp/profile_ext?action=home&__biz=xxx` 有验证墙（返回 2KB 验证页）。**不要**依赖搜狗微信 —— 很多号未收录（"暂无官方认证订阅号"）。

正解：**文章页 HTML 里带同公众号（同 `__biz`）的其他文章链接**，递归抓：

1. 抓文章页 → 正则提取：
   - `var biz = "MzcwMDM1NDg0OA=="` 或 URL 里的 `__biz=`
   - 同号链接两种格式：
     - `s?__biz=<biz>&mid=...&idx=...&sn=...`（可能带 `\x26amp;`/`&amp;` 实体，要 unescape）
     - `mp.weixin.qq.com/s/<短ID>`（10+ 位字母数字）
   - **必须过滤** JS 模板串 `s?__biz=${window.biz}&mid=${window.mid}...`（含 `$` 的丢弃）
2. 队列去重（seen 集合）→ 逐个抓 → 提取新链接 → 直到无新链接
3. 正文解析选择器：
   - 标题：`<h1 id="activity-name">`（内部可能套 `<span class="js_title_inner">`，要 clean）
   - 公众号：`id="js_name"` 或 `var nickname = "..."`
   - 作者：`id="js_author_name"`；时间：`var ct = "UNIX秒"` → datetime
   - 正文：`id="js_content"` 里的第一个 `</div>` 截断点；图片 `data-src` → `![](url)`
   - 标题残留标签：`clean()` 去 `<[^>]+>` 后再用

## 搜狗微信（仅作补充，不可靠）

- `weixin.sogou.com/weixin?type=1&query=<URL编码>` 搜公众号 / `type=2` 搜文章
- **编码是 UTF-8**（不是传说中 GBK）；乱码"澶╅緳澶т箟"= UTF-8 字节被当 GBK 解
- **URL 别加 `interation=1` 参数**——会让页面结构异常、选择器拿不到结果（`type=2&query=...&page=N` 才正常）
- 翻页约第 5 页开始触发验证码（页面含"验证码/antispider"字样）→ 脚本检测到即停止，当天抓已翻页
- 结果链接是 `/link?url=...` 加密跳转，要用 Playwright `window.open()` 新页面等重定向才能解出真实 mp.weixin URL（requests 解不开；在同一 browser context 里跳转才能拿到最终 URL）
- 未认证/未收录号直接返回"暂无相关官方认证订阅号"——别在这耗时间

## 定时增量（每日自动抓新文章）

**两条路线：**

**A. 递归续抓**（简单但覆盖有限）：cron 每天重跑 `wechat_recursive.py`，state 文件去重。注意种子链接会过期、文章页互链仅 1-2 个/篇 → 定期手动补种子。

**B. 搜狗搜索增量**（`wechat_daily.py`，已验证可用）：搜狗 type=2 按公众号名搜文章（翻 10 页）→ Playwright `window.open()` 逐个解 `/link?url=` 跳转 → 读 `id="js_name"` 过滤目标公众号 → 对比 state 增量抓正文。局限：只搜得到标题/正文含该号名的文章，有盲区，抓多少算多少。

```bash
python3 tools/wechat_daily.py            # headless（cron 用）
python3 tools/wechat_daily.py --headful  # 调试
```

**cron 投递坑**：Hermes cronjob `deliver` 必须写显式 `telegram:<chat_id>`（如 `telegram:8852832249`）。只写 `deliver=telegram` 会报 "no delivery target resolved"，即使 gateway 已连上 Telegram。改完 `.env` 的 HOME_CHANNEL 后需重启 gateway（`launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway`）。

## 坑

- 单篇文章 3MB HTML 很正常（内嵌推荐区）——别嫌大
- `wechat_state.json` 放抓取目录，别删；`.incomplete` 类临时文件清理
- 反爬（"环境异常"验证页）出现时：换 UA、加间隔、或让用户从微信 App 复制文章链接
- 标题里 `【】`、引号等特殊字符存文件前 sanitize
