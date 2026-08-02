#!/usr/bin/env python3
"""
天龙大义公众号每日增量抓取
流程: 搜狗微信文章搜索(翻10页) → 逐个解跳转拿真实URL+公众号名
      → 过滤公众号=天龙大义 → 对比已抓状态 → 新文章抓正文存md

用法: python3 wechat_daily.py [--headful]
"""
import asyncio, re, sys, os, json, html as html_mod, urllib.request
from datetime import datetime

ACCOUNT = "天龙大义"
OUT_DIR = "wechat_articles"
STATE_FILE = "wechat_state.json"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"seen": [], "count": 0}


def save_state(s):
    with open(STATE_FILE, "w") as f:
        json.dump(s, f, ensure_ascii=False)


def clean(s):
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"</p>", "\n", s)
    s = re.sub(r"</(div|section|h[1-6]|li)>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html_mod.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n\n", s)
    return s.strip()


def fetch_article(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    html_text = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")
    title = re.search(r'<h1[^>]*id="activity-name"[^>]*>(.*?)</h1>', html_text, re.DOTALL)
    title = clean(title.group(1)).strip() if title else "?"
    acct = re.search(r'id="js_name"[^>]*>\s*([^<]+?)\s*<', html_text)
    account = acct.group(1).strip() if acct else "?"
    ts = re.search(r'var ct = "(\d+)"', html_text)
    date = datetime.fromtimestamp(int(ts.group(1))).strftime("%Y-%m-%d") if ts else ""
    content = re.search(r'id="js_content"[^>]*>(.*?)</div>', html_text, re.DOTALL)
    text = ""
    if content:
        c = re.sub(r"<img[^>]*data-src=\"([^\"]+)\"[^>]*>", r"![](\1)", content.group(1))
        c = re.sub(r"<img[^>]*src=\"([^\"]+)\"[^>]*>", r"![](\1)", c)
        text = clean(c)
    return {"title": title, "account": account, "date": date, "text": text}


async def main():
    headful = "--headful" in sys.argv
    state = load_state()
    seen = set(state["seen"])
    new_count = 0
    total_candidates = 0

    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=not headful)
        ctx = await browser.new_context(user_agent=UA, locale="zh-CN")
        page = await ctx.new_page()

        for pg in range(1, 11):
            url = f"https://weixin.sogou.com/weixin?type=2&query=%E5%A4%A9%E9%BE%99%E5%A4%A7%E4%B9%89&page={pg}"
            try:
                await page.goto(url, timeout=30000)
                await page.wait_for_timeout(2000)
            except Exception as e:
                print(f"第{pg}页加载失败: {str(e)[:60]}")
                break

            html_text = await page.content()
            if "验证码" in html_text and "antispider" in html_text:
                print(f"!! 第{pg}页被验证码拦截")
                break

            items = await page.eval_on_selector_all(".news-list li", """els => els.map(el => {
                const a = el.querySelector('.txt-box h3 a');
                return a ? {title: a.textContent.trim(), href: a.getAttribute('href')} : null;
            }).filter(Boolean)""")

            if not items:
                print(f"第{pg}页无结果, 停止翻页")
                break

            # 逐个解跳转
            for it in items:
                href = it["href"]
                if not href or "link?url=" not in href:
                    continue
                full = "https://weixin.sogou.com" + href if href.startswith("/") else href
                try:
                    async with ctx.expect_page() as np_info:
                        await page.evaluate(f"window.open('{full}', '_blank')")
                    np = await np_info.value
                    await np.wait_for_load_state("domcontentloaded", timeout=20000)
                    await np.wait_for_timeout(2500)
                    final_url = np.url
                    np_html = await np.content()
                    acct = re.search(r'id="js_name"[^>]*>\s*([^<]+?)\s*<', np_html)
                    account = acct.group(1).strip() if acct else "?"
                    await np.close()

                    if account != ACCOUNT:
                        continue  # 不是目标公众号
                    total_candidates += 1
                    base = final_url.split("?")[0]
                    if base in seen:
                        print(f"  跳过(已抓): {it['title'][:30]}")
                        continue
                    # 抓正文
                    art = fetch_article(final_url)
                    if art["account"] != ACCOUNT or not art["text"]:
                        continue
                    new_count += 1
                    safe = re.sub(r'[\\/:*?"<>|]', "_", art["title"])[:80]
                    path = os.path.join(OUT_DIR, f"{safe}.md")
                    md = f"# {art['title']}\n\n> 公众号: **{art['account']}** | {art['date']}\n> 链接: {base}\n\n---\n\n{art['text']}\n"
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(md)
                    seen.add(base)
                    print(f"  ✓ 新文章: {art['title'][:35]} ({len(art['text'])}字)")
                except Exception as e:
                    print(f"  跳转失败: {str(e)[:60]}")

            # 下一页判断
            nxt = await page.query_selector("#sogou_next")
            if not nxt:
                break
        await browser.close()

    state["seen"] = list(seen)
    state["count"] = state.get("count", 0) + new_count
    save_state(state)
    print(f"\n完成: 新抓 {new_count} 篇, 候选 {total_candidates} 篇, 累计已抓 {len(seen)} 链接")


if __name__ == "__main__":
    asyncio.run(main())
