#!/bin/bash
# 触ったページの改行を390pxで実測し、検査2本にかける。
#   使い方: bash tools/kaigyo_measure.sh event company members
#   （拡張子なしのページ名を並べる。トップは index）
# 「直すところはありません」以外が出たら本番に上げない。
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE=/tmp/shibasun-site
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 受け口（ブラウザからの行データを /tmp/lcdata に置く）
mkdir -p /tmp/lcdata
if ! lsof -ti:8768 >/dev/null 2>&1; then
  ( cd /tmp/lcdata && nohup python3 recv.py >/dev/null 2>&1 & )
  sleep 1
fi

# 本番と同じCSSで測るため、いったん配信用へ写す
rsync -a --delete --exclude before --exclude .git --exclude 'img/_orig_window' --exclude _kaigyo "$ROOT"/ "$SITE"/
cp "$ROOT/tools/serve.py" "$SITE/serve.py"
mkdir -p "$SITE/_kaigyo"
cp "$ROOT/tools/kaigyo_iframe.html" "$SITE/_kaigyo/"

if ! lsof -ti:8767 >/dev/null 2>&1; then
  echo "※ 配信が動いていません。preview_start name=shibasun-clean で立ち上げてください"; exit 1
fi

V=$RANDOM
TAGS=()
for name in "$@"; do
  page="/$name"; [ "$name" = "index" ] && page="/"
  tag="k_${name//\//_}"
  TAGS+=("$tag")
  printf "%-22s " "$page"
  "$CH" --headless=new --disable-gpu --virtual-time-budget=25000 --dump-dom \
    "http://127.0.0.1:8767/_kaigyo/kaigyo_iframe.html?p=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]+'?v='+sys.argv[2],safe=''))" "$page" "$V")&t=$tag" \
    2>/dev/null | grep -o '<title>[^<]*</title>' || echo "（測れませんでした）"
done

echo; echo "===== ① 語の途中／② 最終行／③ 短い行 ====="
python3 "$ROOT/tools/kaigyo_check.py" "${TAGS[@]}"
echo; echo "===== 改行しらべ ====="
for t in "${TAGS[@]}"; do
  printf "%-16s " "$t"
  python3 ~/Documents/SBB/コラム予定表/改行しらべ.py "/tmp/lcdata/$t.json" | head -1
done
echo; echo "※「直すところはありません」以外が出たら直してから測り直す（1か所直すと後ろの行がずれる）"
