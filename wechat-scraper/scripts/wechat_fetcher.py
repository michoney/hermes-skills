#!/usr/bin/env python3
"""
微信公众号文章抓取器
用法:
  python3 wechat_fetcher.py <文章URL> [更多URL...]
  python3 wechat_fetcher.py urls.txt        # 从文件读链接(每行一个)

输出: 保存到 ./wechat_articles/<标题>.md
"""

import re
import sys
import os
import html as html_mod
import urllib.request
from datetime import datetime

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
OUT_DIR = "wechat_articles"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")


def clean(s):
    """去掉标签和多余空白"""
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"</p>", "\n", s)
    s = re.sub(r"</(div|section|h[1-6]|li)>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html_mod.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n\n", s)
    return s.strip()


def parse(html_text):
    """提取公众号文章字段"""
    def grab(pattern, group=1, default="?"):
        m = re.search(pattern, html_text, re.DOTALL)
        return m.group(group).strip() if m else default

    title = grab(r'<h1[^>]*id="activity-name"[^>]*>(.*?)</h1>')
    title = clean(title) if title != "?" else "?"

    account = grab(r'id="js_name"[^>]*>\s*([^<]+?)\s*<')
    if account == "?":
        account = grab(r"var nickname = \"([^\"]+)\"")
    if account == "?":
        account = grab(r'id="js_profile_name"[^>]*>(.*?)<')

    author = grab(r'id="js_author_name"[^>]*>(.*?)<')
    if author == "?":
        author = grab(r"var author = \"([^\"]+)\"")

    ts = grab(r"var ct = \"(\d+)\"")
    date = ""
    if ts.isdigit():
        date = datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M")

    # 正文
    content = grab(r'id="js_content"[^>]*>(.*?)</div>', default="")
    if content:
        # 保留图片
        content = re.sub(r"<img[^>]*data-src=\"([^\"]+)\"[^>]*>", r"![](\1)", content)
        content = re.sub(r"<img[^>]*src=\"([^\"]+)\"[^>]*>", r"![](\1)", content)
        text = clean(content)
    else:
        text = ""

    # 原文链接
    orig = grab(r'href="([^"]*mp\.weixin\.qq\.com[^"]*)"', default="")

    return {
        "title": title,
        "account": account,
        "author": author,
        "date": date,
        "url": orig or "",
        "text": text,
    }


def save_md(article, url):
    os.makedirs(OUT_DIR, exist_ok=True)
    safe_title = re.sub(r'[\\/:*?"<>|]', "_", article["title"])[:80]
    path = os.path.join(OUT_DIR, f"{safe_title}.md")
    md = f"""# {article['title']}

> 公众号: **{article['account']}** | 作者: {article['author']} | {article['date']}
> 链接: {url}

---

{article['text']}
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    return path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    urls = []
    if sys.argv[1].endswith(".txt"):
        with open(sys.argv[1]) as f:
            urls = [l.strip() for l in f if l.strip()]
    else:
        urls = sys.argv[1:]

    for url in urls:
        try:
            print(f"抓取: {url[:60]}...", end=" ", flush=True)
            html_text = fetch(url)
            art = parse(html_text)
            if not art["text"]:
                print(f"[跳过] 正文为空 ({art['title']})")
                continue
            path = save_md(art, url)
            print(f"✓ {art['title'][:40]} ({len(art['text'])}字)")
        except Exception as e:
            print(f"[失败] {e}")


if __name__ == "__main__":
    main()
