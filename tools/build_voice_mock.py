# -*- coding: utf-8 -*-
"""お客様の声（B案・引用Q&A型）のモック16ページ＋一覧を生成する。

  python3 tools/build_voice_mock.py

- 原稿は tools/voice_source.json（旧サイト before/.../voice/ から抽出済み）
- 写真は img/mock-voice/v{num}_1.jpg / _2.jpg（無ければその場所は出さない）
- お名前はイニシャル仮表示。実名で公開する時は REAL_NAMES を True にして
  NAMES の実名を使う（※専務の承諾確認が済んでから）
- 出力: mock-voice.html（一覧）+ mock-voice-01.html〜16.html（noindex）
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = json.load(open(os.path.join(ROOT, "tools", "voice_source.json"), encoding="utf-8"))
BY = {v["file"][6:10]: v for v in SRC}

REAL_NAMES = False  # 承諾が取れたら True（NAMES の real を表示）

# 誤字の最小修正と、退職スタッフ実名の役職置換
FIXES = [
    ("大成功でし。", "大成功でした。"),
    ("とれも楽", "とても楽"),
    ("不動動産", "不動産"),
    ("購入していただのですが", "購入していたのですが"),
    ("上回りやくなかったです", "上回りたくなかったです"),
    ("シバサンホーム違いました", "シバサンホームは違いました"),
    ("いっきりと", "はっきりと"),
    ("手狭くなって", "手狭になって"),
    ("真面目にていねいに", "真面目にていねいに"),
    ("国眼さん", "担当アドバイザー"),
    ("矢部さん", "コーディネーターさん"),
    ("お店へ伺いました", "お店へうかがいました"),
    ("徹底いして", "徹底して"),
    ("他社にみ見に行ったり", "他社に見に行ったり"),
    ("しんみに話を", "親身に話を"),
    # 住まいの見当がつく表現は消す（2026-08-10 専務指示。所在地を出さない方針に合わせる）
    ("桜井店が近くだったので", "お店が近くだったので"),
    ("おすすめもあって天然芝にしました。\n実際には、子供が裸足で遊んでても気にならないし", "おすすめもあって人工芝にしました。\n実際には、子供が裸足で遊んでても気にならないし"),
]

def fix(t):
    for a, b in FIXES:
        t = t.replace(a, b)
    # 旧サイトの原稿に混ざっている全角の数字を半角に直す（２部屋→2部屋）
    t = t.translate(str.maketrans("０１２３４５６７８９", "0123456789"))
    return t

# 家ごとの設定 -----------------------------------------------------------
# layout: "qa"=見出しでQ&A分割 / "story"=物語（取材記事）
# quote: 引用ヒーロー（原稿の生の言葉から）
V = [
 dict(num="0000", no=1, layout="story", area="奈良市", family="ご夫婦とお嬢様おふたり",
      initial="M", real="森",
      title="回遊式動線で、家事も、家族の時間も。",
      quote="必要なものと不要なものを、指摘してくれるのが助かりました",
      qby="ご主人"),
 dict(num="0008", no=2, layout="qa", area="桜井市", family="ご夫婦とお子様",
      initial="", real="",
      title="自然に溶け込む、ナチュラル×シンプルな家。",
      quote="主人はアクセル、私がブレーキ！",
      qby="奥様",
      heads=[("〇家づくりを考え始めたキッカケは？", "家づくりを考え始めたキッカケは？"),
             ("シバサンホームとの出合い", "シバ・サンホームとの出会いは？"),
             ("お家づくりで悩んだ点", "お家づくりで悩んだことは？"),
             ("これからの住まい", "これからの住まいの楽しみは？")]),
 dict(num="0001", no=3, layout="story", area="", family="ご夫婦とお子様",
      initial="N", real="西村",
      title="豊かな太陽光が差し込む、開放感あふれる空間。",
      quote="とにかく明るい家にしたかった",
      qby="ご主人"),
 dict(num="0002", no=4, layout="story", area="", family="ご夫婦とお子様おふたり",
      initial="K", real="沓掛",
      title="子育てがなにより楽しく、家族の気配をいつも感じる家。",
      quote="休日の朝食のとき、しみじみ、建てて良かった、と",
      qby="ご主人"),
 dict(num="0003", no=5, layout="story", area="", family="ご夫婦とお嬢様たち・お母様",
      initial="O", real="奥田",
      title="子供が元気に走り回る、子育て思いの温かい家。",
      quote="無垢の床は迷いましたが、決めて正解でした",
      qby="奥様"),
 dict(num="0004", no=6, layout="story", area="", family="ご夫婦とお子様",
      initial="I", real="井上",
      title="その時々の気分で、雰囲気を自在にアレンジする家。",
      quote="シーンに合わせて、照明を変えられるんです",
      qby="ご主人"),
 dict(num="0010", no=7, layout="qa", area="奈良市・菖蒲池", family="ご夫婦とお子様",
      initial="", real="",
      title="広い土地に出会えたから、平屋にしました。",
      quote="シバサンホームの中で、一番喧嘩したと思います",
      qby="奥様",
      heads=[("〇家づくりを考え始めたキッカケは？", "家づくりを考え始めたキッカケは？"),
             ("シバサンホームとの出合い", "シバ・サンホームとの出会いは？"),
             ("お家づくりで悩んだ点", "お家づくりで悩んだことは？"),
             ("これからの住まい", "これからの住まいは？")],
      skip=["奈良市あやめ池の平屋"]),
 dict(num="0012", no=8, layout="qa", area="葛城市", family="ご夫婦とお子様",
      initial="", real="",
      title="ダウンフロアが魅力的な、心地いい平屋の家。",
      quote="一度は『造作の物、全部やめよう』と言うほど悩みました",
      qby="奥様",
      heads=[("家づくりを考え始めたキッカケは？", "家づくりを考え始めたキッカケは？"),
             ("シバサンホームとの出合い", "シバ・サンホームに決めた理由は？"),
             ("お家づくりで悩んだ点", "悩んだこと・これから建てる人へ"),
             ("お家づくりでこだわった点", "こだわった点は？")],
      skip=["ダウンフロアが魅力的な心地いい平屋の家"]),
 dict(num="0013", no=9, layout="qa", area="大和郡山市", family="ご夫婦とお子様たち",
      initial="", real="",
      title="西海岸風の、シンプルな暮らし。",
      quote="子供達が走っても、怒らなくていいのはありがたい",
      qby="奥様",
      heads=[("家づくりを考え始めたキッカケは？", "家づくりを考え始めたキッカケは？"),
             ("シバサンホームとの出合い", "シバ・サンホームとの出会いは？"),
             ("こだわったポイント", "こだわったポイントは？"),
             ("今だから思う事は？", "今だから思うことは？")],
      skip=["西海岸風のシンプルな暮らし"]),
 dict(num="0014", no=10, layout="qa", area="大和郡山市", family="ご夫婦とお子様たち",
      initial="", real="",
      title="シンプルで、ナチュラルな暮らし。",
      quote="どうせ住むなら、自分達の想いが詰まったお家がいい",
      qby="奥様",
      heads=[("家づくりを考え始めたキッカケは？", "家づくりを考え始めたキッカケは？"),
             ("シバサンホームとの出合い", "家づくりはどう進みましたか？"),
             ("お家づくりについて", "お家づくりで印象に残っていることは？"),
             ("実際に住んでみて…", "実際に住んでみて、いかがですか？")],
      skip=["シンプルでナチュラルな暮らし"]),
 dict(num="0015", no=11, layout="qa", area="奈良市", family="ご夫婦とお子様",
      initial="", real="",
      title="調和のとれた、スタイリッシュモダンな住まい。",
      quote="主人は、べトングレー一択でしたね",
      qby="奥様",
      heads=[("〇ConCept", "このお家のコンセプト"),
             ("〇家づくりを考え始めたキッカケは？", "家づくりを考え始めたキッカケは？"),
             ("〇家づくりの進め方", "家づくりはどう進めましたか？"),
             ("〇重視した部分やお家のイメージ", "重視した部分やお家のイメージは？"),
             ("〇これからお家づくりする方へ", "これからお家づくりをする方へ")],
      skip=["調和のとれたスタイリッシュモダンな住まい"]),
 dict(num="0016", no=12, layout="qa", area="大和郡山市", family="ご夫婦",
      initial="", real="",
      title="ゆったりと過ごせる、ナチュラルテイストのお家。",
      quote="今は沢山の友人を呼び、わが家の自慢をしています（笑）",
      qby="奥様",
      heads=[("家づくりを考え始めたキッカケは？", "家づくりを考え始めたキッカケは？"),
             ("家づくりの進め方", "家づくりはどう進めましたか？"),
             ("重視した部分とこだわりポイント", "重視した部分とこだわりポイントは？"),
             ("これからお家づくりをする方へ", "これからお家づくりをする方へ")],
      skip=["ナチュラルテイストのお家"]),
 dict(num="0017", no=13, layout="qa", area="奈良市", family="ご夫婦とお子様",
      initial="", real="",
      title="風合いのある、塗り壁の家。",
      quote="吹き抜けは反対されたけど、暮らしてみたら大正解でした",
      qby="ご夫婦",
      heads=[("家づくりを考え始めたキッカケは？", "家づくりを考え始めたキッカケは？"),
             ("シバサンホームとの出合い", "シバ・サンホームとの出会いは？"),
             ("家のこだわりポイント", "家のこだわりポイントは？"),
             ("これから家を建てる方にアドバイス", "これから家を建てる方へ")],
      skip=["風合いのある塗り壁の家"]),
 dict(num="0018", no=14, layout="qa", area="葛城市", family="ご夫婦",
      initial="", real="",
      title="こだわりの吹抜け空間がある家。",
      quote="日中は、電気もつけなくていいくらいです",
      qby="ご夫婦",
      heads=[("家づくりを考え始めたキッカケは？", "家づくりを考え始めたキッカケは？"),
             ("シバサンホームとの出合い", "シバ・サンホームとの出会いは？"),
             ("重視した部分とこだわりポイント", "重視した部分とこだわりポイントは？"),
             ("これからお家づくりをする方へ", "これからお家づくりをする方へ")],
      skip=["明るく自然体でいられる空間"]),
 dict(num="0019", no=15, layout="qa", area="三郷町", family="ご夫婦とお子様",
      initial="", real="",
      title="和の趣をプラスした、スタイリッシュな家。",
      quote="ずっと家賃を払うのが、もったいない",
      qby="ご夫婦",
      heads=[("家づくりを考え始めたキッカケは？", "家づくりを考え始めたキッカケは？"),
             ("シバサンホームとの出合い", "シバ・サンホームとの出会いは？"),
             ("重視した部分とこだわりポイント", "重視した部分とこだわりポイントは？"),
             ("これからお家づくりをする方へ", "これからお家づくりをする方へ")],
      skip=["和の趣をプラスしたスタイリッシュな家"]),
 dict(num="0020", no=16, layout="qa", area="奈良市", family="ご夫婦とお子様",
      initial="", real="",
      title="アウトドアを楽しむ、カリフォルニアスタイル。",
      quote="知り合いの『シバサンいいと思うよ』が始まりでした",
      qby="ご夫婦",
      heads=[("家づくりを考え始めたキッカケは？", "家づくりを考え始めたキッカケは？"),
             ("シバサンホームとの出合い", "シバ・サンホームとの出会いは？"),
             ("大変だったこと", "大変だったことは？"),
             ("こだわりポイント", "こだわりポイントは？"),
             ("こうしたらよかった所", "こうしたらよかった、と思うところは？"),
             ("最後にメッセージ", "最後にメッセージをどうぞ")],
      skip=["アウトドアを楽しむカリフォルニアスタイル"]),
]

CSS = """
:root{--ink:#1a1a1a;--gray:#5e5d5b;--pale:#f6f6f5;--linec:#e8e8e6}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Zen Kaku Gothic New',sans-serif;color:var(--ink);background:#fff;line-height:2.1;overflow-wrap:break-word;word-break:auto-phrase}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
.mocknote{background:var(--pale);border-bottom:1px solid var(--linec);padding:12px 20px;font-size:11.5px;color:var(--gray);line-height:1.9}
.mocknote b{color:var(--ink);font-weight:500}
header{padding:22px 24px}
header .en{font-family:'Jost',sans-serif;letter-spacing:.28em;font-size:15px;font-weight:500}
header small{display:block;font-size:10px;color:var(--gray);letter-spacing:.14em;margin-top:2px}
.quotehero{padding:50px 24px 28px;text-align:center;max-width:680px;margin:0 auto}
.quotehero .no{font-family:'Jost',sans-serif;font-size:11px;letter-spacing:.22em;color:#a3a3a1}
.quotehero h1{font-size:clamp(22px,6vw,34px);font-weight:500;letter-spacing:.04em;line-height:1.8;margin:16px 0 12px;text-wrap:balance}
.quotehero .who{font-size:12.5px;color:var(--gray);font-weight:300;letter-spacing:.06em;text-wrap:pretty}
.hero img{width:100%;aspect-ratio:4/3;object-fit:cover}
.data{max-width:640px;margin:32px auto 0;padding:0 24px}
.data .srcnote{font-size:11.5px;color:var(--gray);font-weight:300;letter-spacing:.04em}
.data table{width:100%;border-collapse:collapse;font-size:13px}
.data th,.data td{text-align:left;padding:11px 8px;border-bottom:1px solid var(--linec);font-weight:300}
.data th{width:9em;color:var(--gray);font-weight:400;letter-spacing:.06em}
.data tr:nth-child(odd){background:rgba(0,0,0,.025)}
.body{max-width:640px;margin:0 auto;padding:8px 24px 0}
.q{margin-top:44px}
.q .qn{display:grid;grid-template-columns:44px 1fr;gap:12px;align-items:baseline;border-top:1px solid var(--ink);padding-top:16px}
.q .qn .no{font-family:'Jost',sans-serif;font-size:19px;font-weight:300}
.q .qn h2{font-size:15.5px;font-weight:500;letter-spacing:.05em;line-height:1.8;text-wrap:balance}
.q p,.body>p{font-size:14px;font-weight:300;color:#333;margin:16px 0;text-wrap:pretty}
.say{margin:24px 0;padding:2px 0 2px 16px;border-left:2px solid var(--ink);font-size:14px;font-weight:400;line-height:2.1;color:var(--ink)}
figure{margin:34px 0}
figure img{width:100%}
figcaption{font-size:11.5px;color:var(--gray);font-weight:300;margin-top:9px;line-height:1.9}
.cta{margin:56px auto 0;max-width:640px;padding:30px 24px;background:#161614;color:#fff;text-align:center}
.cta h2{font-size:16.5px;font-weight:500;letter-spacing:.08em;margin-bottom:6px}
.cta p{font-size:12px;color:#c2c2c0;font-weight:300;margin-bottom:18px}
.cta a{display:block;max-width:320px;margin:0 auto;padding:14px;background:#fff;color:var(--ink);font-size:12.5px;letter-spacing:.16em}
.navrow{display:flex;justify-content:space-between;max-width:640px;margin:40px auto 0;padding:0 24px;font-family:'Jost',sans-serif;font-size:11px;letter-spacing:.2em;color:var(--gray)}
footer{margin-top:60px;padding:40px 24px 60px;background:#161614;color:#c2c2c0;text-align:center;font-size:11.5px;font-weight:300}
footer .fl{font-family:'Jost',sans-serif;letter-spacing:.3em;color:#fff;font-size:13px;margin-bottom:10px}
"""

HEAD = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="robots" content="noindex,nofollow">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
"""

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def name_of(v):
    """誰の家かの表記。⚠️所在地（市町村）も家族構成も出さない（2026-08-10 専務指示）。
    出すのはイニシャルだけ。分からない邸は空（その行ごと出さない）。"""
    if v["initial"]:
        return (v["real"] + "様邸") if (REAL_NAMES and v["real"]) else (v["initial"] + "様邸")
    return ""

def mask_name(v, t):
    """本文に残る実名をイニシャルに置き換える（森様ご夫妻→M様ご夫妻）。
    ⚠️実名で公開する時（REAL_NAMES=True）は置き換えない。"""
    if REAL_NAMES or not v.get("real") or not v.get("initial"):
        return t
    return t.replace(v["real"] + "様", v["initial"] + "様").replace(v["real"] + "邸", v["initial"] + "邸")

# 旧サイトのページ送り（本文ではない）
NAV_JUNK = {"次へ", "前へ", "＜前へ", "<<", ">>", "≪", "≫", "一覧へ", "一覧へ戻る", "▶", "│", "|"}

def paras_of(v):
    """原稿を段落にまとめ直す。
    ⚠️質問の見出し（「シバサンホームとの出合い」など）は句点で終わらないので、
    素朴に前後をつなぐと見出しが本文に飲み込まれてQ&Aが1問しか出なくなる
    （2026-08-10 に実際に発生）。見出しは必ず独立した1件として扱う。"""
    src = BY[v["num"]]["paras"]
    skip = set(v.get("skip", []))
    heads = {a for a, _ in v.get("heads", [])}
    out = []
    for p in src:
        p = mask_name(v, fix(p.strip()))
        if not p or p == "。" or p in skip or p in NAV_JUNK:
            continue
        if p in heads:                      # 見出しは独立させる（つながない）
            out.append(p)
            continue
        # 細切れ行（元サイトの改行）を前の行につなぐ: 文末記号で終わらない短い行
        if (out and out[-1] not in heads
                and not re.search(r"[。！？…笑\)）」』〜]$", out[-1])
                and not out[-1].endswith("・・・")):
            out[-1] += p
        else:
            out.append(p)
    return out

def render_paragraph(p):
    if p.startswith("「") and "」" in p and p.index("」") > len(p) * 0.5:
        return f'<div class="say">{esc(p)}</div>'
    return f"<p>{esc(p)}</p>"

def photo(v, i, cap=""):
    f = f"img/mock-voice/v{v['num']}_{i}.jpg"
    if not os.path.exists(os.path.join(ROOT, f)):
        return ""
    c = f"<figcaption>{esc(cap)}</figcaption>" if cap else ""
    return f'<figure><img src="{f}" alt="{esc(v["title"])}" loading="lazy">{c}</figure>'

def build_detail(v, prev_href, next_href):
    fname = f"mock-voice-{v['no']:02d}.html"
    page_title = f"【モック】{v['title']}｜お客様の声 #{v['no']:02d}｜シバ・サンホーム"
    h = HEAD.format(title=esc(page_title), css=CSS)
    h += f'<div class="mocknote"><b>【B案モック #{v["no"]:02d}】</b>お名前はイニシャルのみ・所在地と家族構成は出さない方針で確定。顔が写る写真は使っていません。本文は旧サイトの取材原稿のまま（誤字のみ修正）。</div>\n'
    h += '<header><div class="en">SHIBA SUN HOME</div><small>奈良の注文住宅</small></header>\n'
    nm = name_of(v)
    who = esc(v["title"]) + ("｜" + esc(nm) if nm else "")
    h += f'''<div class="quotehero">
  <div class="no">VOICE #{v["no"]:02d}</div>
  <h1>「{esc(v["quote"])}」</h1>
  <div class="who">{who}</div>
</div>\n'''
    if os.path.exists(os.path.join(ROOT, f"img/mock-voice/v{v['num']}_1.jpg")):
        h += f'<div class="hero"><img src="img/mock-voice/v{v["num"]}_1.jpg" alt="{esc(v["title"])}"></div>\n'
    h += '<div class="data"><p class="srcnote">旧サイトに掲載していた取材記事より。</p></div>\n<div class="body">\n'

    paras = paras_of(v)
    mid_photo = photo(v, 2)
    if v["layout"] == "qa":
        heads = v["heads"]
        head_keys = {a: b for a, b in heads}
        sections, cur = [], ("", [])
        for p in paras:
            if p in head_keys:
                if cur[1]:
                    sections.append(cur)
                cur = (head_keys[p], [])
            else:
                cur[1].append(p)
        if cur[1]:
            sections.append(cur)
        qn = 0
        for i, (title, ps) in enumerate(sections):
            if title:
                qn += 1
                h += f'<div class="q"><div class="qn"><div class="no">Q{qn}</div><h2>{esc(title)}</h2></div>\n'
            else:
                h += '<div class="q">\n'
            for p in ps:
                h += render_paragraph(p) + "\n"
            h += "</div>\n"
            if mid_photo and i == max(0, len(sections) // 2 - 1):
                h += mid_photo + "\n"
                mid_photo = ""
    else:
        half = len(paras) // 2
        for i, p in enumerate(paras):
            h += render_paragraph(p) + "\n"
            if mid_photo and i == half:
                h += mid_photo + "\n"
                mid_photo = ""
    h += "</div>\n"
    h += '''<div class="cta">
  <h2>建てた人の話を、聞きに来ませんか。</h2>
  <p>ご家族に合う間取りも、お金の話も、正直にお答えします。</p>
  <a href="reserve.html">来店予約</a>
</div>\n'''
    h += f'<div class="navrow"><a href="{prev_href}">← PREV</a><a href="mock-voice.html">LIST</a><a href="{next_href}">NEXT →</a></div>\n'
    h += '''<footer>
  <div class="fl">SHIBA SUN HOME</div>
  <div>株式会社シバ・サンホーム｜奈良県奈良市北之庄町41-1</div>
</footer>
</body>
</html>
'''
    open(os.path.join(ROOT, fname), "w", encoding="utf-8").write(h)
    return fname

# 一覧 -------------------------------------------------------------------
LIST_CSS = CSS + """
.whead{padding:44px 24px 10px;text-align:center}
.whead .en{font-family:'Jost',sans-serif;font-size:11px;letter-spacing:.3em;color:#a3a3a1;text-transform:uppercase}
.whead h1{font-size:clamp(22px,5.6vw,32px);font-weight:500;letter-spacing:.08em;margin:12px 0 14px;line-height:1.6;text-wrap:balance}
.whead p{font-size:13px;font-weight:300;color:var(--gray);max-width:600px;margin:0 auto;line-height:2.1;text-wrap:pretty}
.list{max-width:680px;margin:30px auto 0;padding:0 20px}
.card{display:block;margin:0 0 54px}
.card .ph{aspect-ratio:3/2;overflow:hidden;background:var(--pale)}
.card .ph img{width:100%;height:100%;object-fit:cover}
.card .no{font-family:'Jost',sans-serif;font-size:11px;letter-spacing:.22em;color:#a3a3a1;margin:16px 0 4px}
.card h2{font-size:17.5px;font-weight:500;letter-spacing:.05em;line-height:1.75;text-wrap:balance}
.card .who{font-size:12px;color:var(--gray);font-weight:300;margin-top:6px;letter-spacing:.06em}
.card .quote{font-size:13px;font-weight:300;color:#3c3c3a;margin-top:10px;padding-left:14px;border-left:2px solid var(--ink);line-height:2}
.card .more{font-family:'Jost',sans-serif;font-size:10.5px;letter-spacing:.24em;color:var(--gray);margin-top:12px}
@media(min-width:800px){.list{max-width:1040px;display:grid;grid-template-columns:1fr 1fr;gap:0 48px}.card{margin-bottom:64px}}
"""

def build_list():
    h = HEAD.format(title="【モック】お客様の声 一覧｜シバ・サンホーム", css=LIST_CSS)
    h += '<div class="mocknote"><b>【デザイン提案モック・B案】</b>旧サイトに眠っていた「お客様の声」16本の復活案。<b>新しい家から順</b>・<b>お名前はイニシャルのみ</b>・<b>所在地と家族構成は出さない</b>・顔が写る写真は不使用。公開前に残るのは「内容の時点確認」だけです。</div>\n'
    h += '<header><div class="en">SHIBA SUN HOME</div><small>奈良の注文住宅</small></header>\n'
    h += '''<div class="whead">
  <div class="en">Voice</div>
  <h1>建てた人の、声。</h1>
  <p>シバ・サンホームで家を建てたご家族に、住んでからの本音をうかがいました。ぜんぶ、実際にあった家づくりの話です。</p>
</div>
<div class="list">\n'''
    for v in sorted(V, key=lambda x: x["no"]):
        href = f"mock-voice-{v['no']:02d}.html"
        img = f"img/mock-voice/v{v['num']}_1.jpg"
        imgtag = f'<img src="{img}" alt="{esc(v["title"])}" loading="lazy">' if os.path.exists(os.path.join(ROOT, img)) else ""
        nm = name_of(v)
        wholine = f'    <div class="who">{esc(nm)}</div>\n' if nm else ""
        h += f'''  <a class="card" href="{href}">
    <div class="ph">{imgtag}</div>
    <div class="no">VOICE #{v['no']:02d}</div>
    <h2>{esc(v["title"])}</h2>
{wholine}    <div class="quote">「{esc(v["quote"])}」</div>
    <div class="more">READ →</div>
  </a>\n'''
    h += '''</div>
<footer>
  <div class="fl">SHIBA SUN HOME</div>
  <div>株式会社シバ・サンホーム｜奈良県奈良市北之庄町41-1</div>
</footer>
</body>
</html>
'''
    open(os.path.join(ROOT, "mock-voice.html"), "w", encoding="utf-8").write(h)

# 並びは「新しい家から」（2026-08-10 専務指示。旧サイトの番号が新しいほど新しい取材）
NEW_ORDER = ["0020","0019","0018","0017","0016","0015","0014","0013","0012","0010","0008","0004","0003","0002","0001","0000"]
for _v in V:
    _v["no"] = NEW_ORDER.index(_v["num"]) + 1

def main():
    order = sorted(V, key=lambda v: v["no"])
    files = []
    for i, v in enumerate(order):
        prev_href = f"mock-voice-{order[i-1]['no']:02d}.html" if i > 0 else "mock-voice.html"
        next_href = f"mock-voice-{order[(i+1) % len(order)]['no']:02d}.html"
        files.append(build_detail(v, prev_href, next_href))
    build_list()
    print("生成:", len(files), "ページ + mock-voice.html")

if __name__ == "__main__":
    main()
