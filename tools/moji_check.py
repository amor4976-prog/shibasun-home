# -*- coding: utf-8 -*-
"""文字の混入検査：日本語以外の文字（ハングル・キリル文字など）・文字化け・
   全角英数字・半角カタカナ・閉じていない括弧を洗い出す。
   使い方: python3 tools/moji_check.py [ファイル...]  （省略時は *.html *.js *.txt）"""
import unicodedata, glob, re, sys

BAD_SCRIPTS = ("HANGUL","CYRILLIC","GREEK","ARABIC","HEBREW","THAI",
               "DEVANAGARI","ARMENIAN","GEORGIAN","BENGALI","TAMIL")

targets = sys.argv[1:] or (glob.glob('*.html') + glob.glob('*.js') + glob.glob('*.txt'))
problems = []
for f in sorted(targets):
    # 道具そのもの（.py／.sh）は検査しない。検査の合図に使う文字を持っているため
    if f.endswith('.py') or f.endswith('.sh'):
        continue
    try:
        s = open(f, encoding='utf-8').read()
    except Exception:
        continue
    for i, ch in enumerate(s):
        if ord(ch) < 128:
            continue
        try:
            name = unicodedata.name(ch)
        except ValueError:
            continue
        if any(b in name for b in BAD_SCRIPTS):
            ctx = s[max(0, i-25):i+25].replace('\n', ' ')
            problems.append((f, f'別の言語の文字「{ch}」', ctx))
    for pat, label in [('�', '文字化け(�)'), ('。。', '。の重複'), ('、、', '、の重複')]:
        if pat in s:
            problems.append((f, label, ''))
    z = re.findall(r'[Ａ-Ｚａ-ｚ０-９]', s)
    if z:
        problems.append((f, f'全角の英数字 {len(z)}文字（{"".join(sorted(set(z)))[:20]}）', ''))
    if re.search(r'[｡-ﾟ]', s):
        problems.append((f, '半角カタカナ', ''))
    # 括弧は「お客様に見える文章」だけ数える（コード・コメントの括弧は数えない）
    visible = s
    if f.endswith('.html'):
        visible = re.sub(r'<script.*?</script>', '', visible, flags=re.S)
        visible = re.sub(r'<style.*?</style>', '', visible, flags=re.S)
        visible = re.sub(r'<!--.*?-->', '', visible, flags=re.S)
    elif f.endswith('.js') or f.endswith('.py'):
        visible = ''  # コードは対象外
    for a, b in [('「', '」'), ('（', '）'), ('『', '』'), ('【', '】')]:
        if visible.count(a) != visible.count(b):
            problems.append((f, f'{a}{b} の数が合わない（{visible.count(a)}対{visible.count(b)}）', ''))

if problems:
    print(f'★ {len(problems)}件みつかりました')
    for f, label, ctx in problems:
        print(f'   {f}: {label}')
        if ctx:
            print(f'      …{ctx}…')
    sys.exit(1)
print(f'検査したファイル {len(targets)}個 ／ 問題なし')
