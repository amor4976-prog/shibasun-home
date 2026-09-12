# -*- coding: utf-8 -*-
"""構造化データ（JSON-LD）の検査。公開前に必ず回す。
   ・タグが混ざっていないか（<span class="nb"> が入るとJSONが壊れる。2026-09-13にトップで発生）
   ・JSONとして読めるか
   ・@type と、FAQPageなら質問の数を出す
   使い方: python3 tools/ldjson_check.py [ページ.html ...]（省略時は全ページ）"""
import re, json, glob, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SKIP = ('jisseki-old-backup.html',)
MOCK = ('mock-', 'top-mock-', 'iezukuri-mock', 'jisseki-mock')
pages = sys.argv[1:] or sorted(p for p in glob.glob('*.html')
                               if p not in SKIP and not any(p.startswith(m) or m in p for m in MOCK))
BLK = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
bad, n = [], 0
for p in pages:
    s = open(p, encoding='utf-8').read()
    for m in BLK.finditer(s):
        n += 1
        t = m.group(1)
        if '<' in t:
            tags = sorted(set(re.findall(r'<[^>]+>', t)))
            bad.append((p, 'タグが混ざっている ' + ' '.join(tags[:3])))
            continue
        try:
            json.loads(t)
        except Exception as e:
            bad.append((p, 'JSONが読めない: ' + str(e)[:70]))

print(f'検査したページ {len(pages)}／構造化データ {n}件')
print(f'■ 異常 {len(bad)}件')
for p, why in bad:
    print(f'   {p:26} {why}')
if bad:
    print('\n※ 本文の <span class="nb"> を置換するときは ld+json の中に当てないこと。'
          '当ててしまったら中のタグを消して json.loads で検算する')
sys.exit(1 if bad else 0)
