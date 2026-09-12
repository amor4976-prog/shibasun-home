#!/usr/bin/env python3
# 全ページのリンク切れ・画像切れを洗い出す。切替前に必ず回すこと。
import re, os, sys, glob
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# 本番に出さないページ（モック・バックアップ・下書き）は検査対象から外すが、
# 下書きは中身のリンクだけは見る（公開時に壊れていると困るため）
SKIP = ("jisseki-old-backup.html",)
MOCK = ("mock-", "top-mock-", "iezukuri-mock", "jisseki-mock")

pages = sorted(p for p in glob.glob("*.html") if p not in SKIP and not any(p.startswith(m) or m in p for m in MOCK))

def resolve(path):
    """内部リンクの行き先を実体のファイル名に直す。
       決まりで拡張子を書かないので（/catalog）、.html を足して探す。"""
    path = path.lstrip("/")
    if path in ("", "index.html"):
        return "index.html"
    if os.path.exists(path) and not os.path.isdir(path):
        return path
    if os.path.exists(path + ".html"):
        return path + ".html"
    if os.path.isdir(path) and os.path.exists(os.path.join(path, "index.html")):
        return os.path.join(path, "index.html")
    return None


missing_links, missing_assets, ok_links = [], [], 0
ids_by_page = {}

for p in pages:
    html = open(p, encoding="utf-8").read()
    ids_by_page[p] = set(re.findall(r'id="([^"]+)"', html))

for p in pages:
    html = open(p, encoding="utf-8").read()

    # ---- リンク（href）----
    for m in re.finditer(r'href="([^"]+)"', html):
        h = m.group(1)
        if h.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "data:")):
            continue
        if h.startswith("#"):
            if h[1:] and h[1:] not in ids_by_page[p]:
                missing_links.append((p, h, "同じページ内に見出しが無い"))
            continue
        path, _, frag = h.partition("#")
        path = unquote(path.split("?")[0])   # article.css?v=… のような版番号は外す
        if not path:
            continue
        # 内部リンクは拡張子なしで書く決まり（/catalog）。実体の .html に直してから照合する
        target = resolve(path)
        if target is None:
            missing_links.append((p, h, "ファイルが無い"))
        else:
            ok_links += 1
            if frag and target.endswith(".html") and target in ids_by_page and frag not in ids_by_page[target]:
                missing_links.append((p, h, "飛び先に見出しが無い"))

    # ---- 画像・動画・CSS・JS（src / srcset）----
    for m in re.finditer(r'(?:src|poster)="([^"]+)"', html):
        s = m.group(1)
        if s.startswith(("http", "data:", "//")):
            continue
        s = unquote(s.split("?")[0])
        if s and not os.path.exists(s):
            missing_assets.append((p, s))
    for m in re.finditer(r'srcset="([^"]+)"', html):
        for part in m.group(1).split(","):
            u = part.strip().split(" ")[0]
            if not u or u.startswith(("http", "data:")):
                continue
            u = unquote(u.split("?")[0])
            if not os.path.exists(u):
                missing_assets.append((p, u))

print(f"検査したページ {len(pages)}／内部リンク {ok_links}本が正常\n")
print(f"■ リンク切れ {len(missing_links)}件")
for p, h, why in missing_links:
    print(f"   {p:28} → {h}   （{why}）")
print(f"\n■ 画像・ファイル切れ {len(set(missing_assets))}件")
for p, s in sorted(set(missing_assets)):
    print(f"   {p:28} → {s}")

# ---- sitemap の整合 ----
if os.path.exists("sitemap.xml"):
    sm = open("sitemap.xml", encoding="utf-8").read()
    urls = re.findall(r"<loc>([^<]+)</loc>", sm)
    # サイトマップは拡張子なしURL（/blog 等）。ローカルの .html に正規化して照合する
    files = []
    for u in urls:
        seg = u.rstrip("/").split("/")[-1]
        if seg in ("", "www.shibasun.jp"):
            seg = "index"
        if not seg.endswith(".html"):
            seg += ".html"
        files.append(seg)
    bad = [f for f in files if not os.path.exists(f)]
    noindexed = []
    for f in files:
        if os.path.exists(f):
            if 'name="robots" content="noindex' in open(f, encoding="utf-8").read():
                noindexed.append(f)
    listed = set(files)
    notlisted = [p for p in pages if p not in listed
                 and 'name="robots" content="noindex' not in open(p, encoding="utf-8").read()
                 and p != "404.html"]
    print(f"\n■ サイトマップ {len(urls)}件")
    print(f"   実体の無いページ: {bad or 'なし'}")
    print(f"   検索避け(noindex)なのに載っている: {noindexed or 'なし'}")
    print(f"   公開ページなのに載っていない: {notlisted or 'なし'}")
