#!/usr/bin/env python3
"""
公众号文章递归爬虫 — 从种子链接顺藤摸瓜抓完整个公众号
用法:
  python3 wechat_recursive.py <种子文章URL> [最大篇数=50]
"""
import re, sys, os, html as html_mod, urllib.request, json
from datetime import datetime

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
OUT_DIR = "wechat_articles"
STATE_FILE = "wechat_state.json"  # 记录已抓链接 (去重 + 增量)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")


def clean(s):
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"</p>", "\n", s)
    s = re.sub(r"</(div|section|h[1-6]|li)>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html_mod.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n\n", s)
    return s.strip()


def extract_links(html_text, biz):
    """从文章页提取同公众号(同biz)的其他文章链接"""
    links = set()
    # 格式1: s?__biz=xxx&mid=...&idx=...&sn=... (同号文章)
    pat1 = re.findall(r'(https?://mp\.weixin\.qq\.com/s\?[^"\'\\ ]*__biz=' + re.escape(biz) + r'[^"\'\\ ]*)', html_text)
    for l in pat1:
        l = html_mod.unescape(l)
        l = l.split('&amp;')[0] if False else l  # 保留完整
        links.add(l)
    # 格式2: /s/xxx (短链接)
    pat2 = re.findall(r'https?://mp\.weixin\.qq\.com/s/[a-zA-Z0-9_-]{10,}', html_text)
    for l in pat2:
        links.add(l)
    return links


def parse_article(html_text):
    def grab(pattern, group=1, default="?"):
        m = re.search(pattern, html_text, re.DOTALL)
        return m.group(group).strip() if m else default

    title = grab(r'<h1[^>]*id="activity-name"[^>]*>(.*?)</h1>')
    title = clean(title) if title != "?" else "?"
    account = grab(r'id="js_name"[^>]*>\s*([^<]+?)\s*<')
    if account == "?":
        account = grab(r'var nickname = "([^"]+)"')
    author = grab(r'id="js_author_name"[^>]*>(.*?)<')
    ts = grab(r'var ct = "(\d+)"')
    date = ""
    if ts.isdigit():
        date = datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d")
    content = grab(r'id="js_content"[^>]*>(.*?)</div>', default="")
    if content:
        content = re.sub(r"<img[^>]*data-src=\"([^\"]+)\"[^>]*>", r"![](\1)", content)
        content = re.sub(r"<img[^>]*src=\"([^\"]+)\"[^>]*>", r"![](\1)", content)
        text = clean(content)
    else:
        text = ""
    return {"title": title, "account": account, "author": author, "date": date, "text": text}


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"seen": [], "count": 0}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, ensure_ascii=False)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    seed = sys.argv[1]
    max_articles = int(sys.argv[2]) if len(sys.argv) > 2 else 50

    state = load_state()
    seen = set(state["seen"])
    queue = [seed]
    os.makedirs(OUT_DIR, exist_ok=True)

    biz = None
    new_count = 0

    while queue and new_count < max_articles:
        url = queue.pop(0)
        # 规范化: 去掉 tracking 参数
        base = url.split("?")[0]
        if url in seen or base in seen:
            continue
        try:
            print(f"[{len(seen)+1}] 抓取 {base[-30:]}...", end=" ", flush=True)
            html_text = fetch(url)
        except Exception as e:
            print(f"[网络错误] {str(e)[:50]}")
            continue

        # 确定 biz
        if not biz:
            m = re.search(r'__biz=([A-Za-z0-9=]+)', html_text)
            m2 = re.search(r'var biz = "([^"]+)"', html_text)
            biz = (m2 or m).group(1) if (m2 or m) else None
            if biz:
                print(f"biz={biz}", end=" ")
        if not biz:
            print("[无法识别biz, 跳过]")
            seen.add(url)
            continue

        art = parse_article(html_text)
        seen.add(url)
        if art["text"]:
            new_count += 1
            safe_title = re.sub(r'[\\/:*?"<>|]', "_", art["title"])[:80]
            path = os.path.join(OUT_DIR, f"{safe_title}.md")
            md = f"# {art['title']}\n\n> 公众号: **{art['account']}** | 作者: {art['author']} | {art['date']}\n> 链接: {base}\n\n---\n\n{art['text']}\n"
            with open(path, "w", encoding="utf-8") as f:
                f.write(md)
            print(f"✓ {art['title'][:25]} ({len(art['text'])}字, 共{new_count}篇)")
        else:
            print(f"[空正文跳过]")

        # 提取新链接
        new_links = extract_links(html_text, biz)
        for l in new_links:
            l = l.replace("\\x26amp;", "&").replace("&amp;", "&")
            if l not in seen:
                queue.append(l)
        # 保存进度
        state["seen"] = list(seen)
        state["count"] = new_count
        save_state(state)

    print(f"\n完成: 本次新增 {new_count} 篇, 累计 {len(seen)} 个链接")


if __name__ == "__main__":
    main()
