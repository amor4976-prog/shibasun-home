#!/bin/bash
# HPの公開はこれを通す。検査に落ちたら公開しない。
#
#   使い方: bash tools/deploy.sh "コミットの説明" ファイル1 ファイル2 ...
#
# 2026-08-16 専務「今後絶対にないようにして」を受けて用意。
# 目視での確認をやめ、機械が通ったものだけを公開する。

set -e
cd "$(dirname "$0")/.."
SRC="$(pwd)"
MSG="$1"; shift

if [ -z "$MSG" ] || [ $# -eq 0 ]; then
  echo "使い方: bash tools/deploy.sh \"説明\" ファイル..." >&2
  exit 1
fi

echo "── ① 変な文字が混ざっていないか"
python3 tools/moji_check.py "$@" || { echo "★止めました。文字を直してから、もう一度。" >&2; exit 1; }

echo "── ② リンク切れ・一覧漏れ"
python3 tools/check_links.py

echo "── ③ 公開"
D="$(mktemp -d)/hp"
git clone -q --depth 1 https://github.com/amor4976-prog/shibasun-home.git "$D"
for f in "$@"; do
  cp "$SRC/$f" "$D/$f"
done
cd "$D"
git add "$@"
git commit -q -m "$MSG

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push -q
echo "反映しました（Cloudflareの反映まで1〜2分）"
