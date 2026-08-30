#!/usr/bin/env python3
"""トップのYouTubeの数字を最新にする（月末のルーティン）。

  python3 tools/update_youtube_stats.py          # 書き換える
  python3 tools/update_youtube_stats.py --dry    # 今の数字を見るだけ

直す場所は index.html の2か所。
  ① YouTubeの枠 …… 累計総再生回数／チャンネル登録者数／「◯年◯月時点」
  ② 信頼バーの4枚目 …… 登録◯.◯◯万人・◯◯◯万回再生

⚠️登録者数はAPIでも3桁に丸めた値しか返らない（YouTubeの仕様）。
   実数はチャンネル所有者のYouTube Studioにしかない。
書き換えたあとは必ず
  python3 tools/moji_check.py index.html
  bash tools/deploy.sh "YouTubeの数字を更新" index.html
"""
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

SA = Path.home() / "Downloads/sheets-reader-498602-96d95c7fc631.json"
CHANNEL = "UC4XwoZ806Ga4STcg5WoO3zg"
HTML = Path(__file__).resolve().parent.parent / "index.html"


def fetch():
    """APIキーでは401になる。サービスアカウントのOAuthトークンで聞く。"""
    from google.oauth2 import service_account
    import google.auth.transport.requests as tr

    cred = service_account.Credentials.from_service_account_file(
        str(SA), scopes=["https://www.googleapis.com/auth/youtube.readonly"]
    )
    cred.refresh(tr.Request())
    url = (
        "https://www.googleapis.com/youtube/v3/channels"
        f"?part=statistics&id={CHANNEL}"
    )
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + cred.token})
    st = json.load(urllib.request.urlopen(req))["items"][0]["statistics"]
    return int(st["viewCount"]), int(st["subscriberCount"])


def man(n):
    """11200 -> '1.12万'  3211599 -> '321万'（切り捨て。増える一方なので控えめ側）"""
    if n >= 1_000_000:
        return f"{n // 10000}万"
    return f"{n / 10000:.2f}".rstrip("0").rstrip(".") + "万"


def main():
    views, subs = fetch()
    now = datetime.now()
    print(f"再生 {views:,}回 ／ 登録 {subs:,}人（{man(subs)}人・丸め値）")
    if "--dry" in sys.argv:
        return

    s = HTML.read_text(encoding="utf-8")
    before = s
    rules = [
        ("再生回数", r"(<em>累計総再生回数</em><b>)[^<]*(</b>)", rf"\g<1>{views:,}回\g<2>"),
        ("登録者数", r"(<em>チャンネル登録者数</em><b>)[^<]*(</b>)", rf"\g<1>{subs:,}人\g<2>"),
        ("時点", r'(<p class="ytasof">)[^<]*(</p>)', rf"\g<1>{now.year}年{now.month}月時点\g<2>"),
        ("信頼バー", r'(<span class="tb-c">登録)[^<]*(</span>)',
         rf"\g<1>{man(subs)}人・{man(views)}回再生\g<2>"),
    ]

    missing = []
    for name, pat, rep in rules:
        s, hit = re.subn(pat, rep, s)
        if hit == 0:
            missing.append(name)

    if missing:
        # 目印が見つからない＝index.html の書き方が変わった。黙って通さない。
        print("★見つからなかった目印: " + "、".join(missing))
        print("  index.html を直したあと、このスクリプトの目印も直してください。")
        sys.exit(1)

    if s == before:
        print("すでに最新でした。書き換えなし。")
        return
    HTML.write_text(s, encoding="utf-8")
    print("index.html を書き換えました。moji_check → deploy を回してください。")


if __name__ == "__main__":
    main()
