# -*- coding: utf-8 -*-
"""改行検査：ブラウザで実測した行データ(/tmp/lcdata/*.json)を読み、
   ①語の途中で切れている ②最終行が3文字以下 ③1〜3文字だけの行 を洗い出す。"""
import json, sys, re, glob, os
from janome.tokenizer import Tokenizer
T = Tokenizer()

def merged(text):
    out = []
    for t in T.tokenize(text):
        pos = t.part_of_speech.split(',')
        # 助動詞・接尾だけ前にくっつける（「こと・もの・ため」等の形式名詞の前で切るのは許容）
        if ((pos[0] == '助動詞') or (len(pos) > 1 and pos[1] == '接尾')) and out:
            out[-1] += t.surface
        else:
            out.append(t.surface)
    return out

tags = sys.argv[1:] or [os.path.basename(p)[:-5] for p in glob.glob('/tmp/lcdata/*.json')]
split, orphan, tiny = [], [], []
blocks = 0
for tag in tags:
    p = f'/tmp/lcdata/{tag}.json'
    if not os.path.exists(p):
        print(f'※ {tag}.json が無い'); continue
    for b in json.load(open(p)):
        if 'lines' not in b:
            continue
        blocks += 1
        L = [x for x in b['lines'] if x.strip()]
        if len(L) < 2:
            continue
        page = re.sub(r'\?.*', '', b['p'])
        text = ''.join(L)
        sp, i = [], 0
        for t in merged(text):
            sp.append((i, i + len(t), t)); i += len(t)
        off = 0
        for k in range(len(L) - 1):
            off += len(L[k])
            for a, bb, tk in sp:
                if a < off < bb and len(tk) > 1:
                    if re.fullmatch(r'[0-9A-Za-z\.\-,／/％%]+', tk):
                        break
                    split.append((page, b['w'], tk, L[k][-9:], L[k + 1][:9]))
                    break
        if len(L[-1]) <= 3:
            orphan.append((page, b['w'], L[-2][-12:], L[-1]))
        for x in L[:-1]:
            if len(x) <= 3:
                tiny.append((page, b['w'], x, text[:24]))

print(f"検査した文章のかたまり {blocks}個")
print(f"① 語の途中で切れている　{len(split)}件")
print(f"② 最後の行が3文字以下　{len(orphan)}件")
print(f"③ 途中に3文字以下の行　{len(tiny)}件")
for label, rows in (("① 語の途中", split), ("② 最終行が短い", orphan), ("③ 途中の短い行", tiny)):
    if not rows: continue
    print(f"\n{label}")
    for r in rows[:40]:
        print("   ", "  ".join(str(x) for x in r))
