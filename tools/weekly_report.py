# -*- coding: utf-8 -*-
"""ホームページの週1レポート。専務が見たい数字だけを出す。
   ・GA4          … 訪問・商圏（奈良/大阪/京都）・人気ページ・入口
   ・Search Console … 検索のクリックと検索された言葉
   ・シバグラム台帳  … 資料請求と来店予約の件数＝いちばん大事な数字

   使い方: python3 tools/weekly_report.py [終了日 YYYY-MM-DD]（省略時は昨日まで）

   ※営業の問い合わせとテストは自動で除く（NG_WORDS）。
     判定に迷うものは件数に入れず「要確認」として別に出す。"""
import sys, datetime, collections, json, urllib.request, os
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (RunReportRequest, DateRange, Dimension, Metric, Filter, FilterExpression)
from googleapiclient.discovery import build

KEY = "/Users/sbbymac/Downloads/sheets-reader-498602-96d95c7fc631.json"
GA4 = "properties/323237980"
SITE = "sc-domain:shibasun.jp"
SHOKEN = {"Nara": "奈良", "Osaka": "大阪", "Kyoto": "京都"}  # 商圏＝奈良に住む予定の人

end = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.date.today() - datetime.timedelta(days=1)
start = end - datetime.timedelta(days=6)
p_end, p_start = start - datetime.timedelta(days=1), start - datetime.timedelta(days=7)

cred = service_account.Credentials.from_service_account_file(KEY)
ga = BetaAnalyticsDataClient(credentials=cred)

def run(dims, mets, s, e, limit=25):
    r = ga.run_report(RunReportRequest(
        property=GA4,
        date_ranges=[DateRange(start_date=str(s), end_date=str(e))],
        dimensions=[Dimension(name=d) for d in dims],
        metrics=[Metric(name=m) for m in mets],
        limit=limit))
    return [([v.value for v in row.dimension_values], [v.value for v in row.metric_values]) for row in r.rows]

def num(rows, i=0):
    return sum(int(float(m[i])) for _, m in rows) if rows else 0

print(f"■ ホームページ週報　{start}〜{end}（前の週：{p_start}〜{p_end}）\n")

# ── 全体
now = run(["country"], ["sessions", "totalUsers"], start, end)
prev = run(["country"], ["sessions", "totalUsers"], p_start, p_end)
jp_now = [r for r in now if r[0][0] == "Japan"]
jp_prev = [r for r in prev if r[0][0] == "Japan"]
def diff(a, b):
    if b == 0: return "（前の週は0）"
    d = (a - b) / b * 100
    return f"（前の週比 {d:+.0f}%）"
print("【全体・日本国内】")
print(f"  訪問 {num(jp_now)}回 {diff(num(jp_now), num(jp_prev))}")
print(f"  人数 {num(jp_now,1)}人 {diff(num(jp_now,1), num(jp_prev,1))}\n")

# ── 商圏（奈良・大阪・京都）
reg_now = run(["region"], ["sessions"], start, end, 50)
reg_prev = run(["region"], ["sessions"], p_start, p_end, 50)
def pick(rows, key):
    return sum(int(float(m[0])) for d, m in rows if key in d[0])
print("【商圏＝奈良に住む予定の人】")
tot_now = tot_prev = 0
for en, ja in SHOKEN.items():
    a, b = pick(reg_now, en), pick(reg_prev, en)
    tot_now += a; tot_prev += b
    print(f"  {ja}　{a}回 {diff(a, b)}")
print(f"  ３府県あわせて {tot_now}回 {diff(tot_now, tot_prev)}\n")

# ── よく見られたページ
print("【よく見られたページ 上位8】")
for d, m in run(["pagePath"], ["screenPageViews"], start, end, 8):
    print(f"  {m[0]:>5}回  {d[0]}")
print()

# ── 入口
print("【どこから来たか 上位6】")
for d, m in run(["sessionDefaultChannelGroup"], ["sessions"], start, end, 6):
    print(f"  {m[0]:>5}回  {d[0]}")
print()

# ── Search Console
try:
    sc = build("searchconsole", "v1", credentials=cred.with_scopes(
        ["https://www.googleapis.com/auth/webmasters.readonly"]))
    body = {"startDate": str(start), "endDate": str(end), "dimensions": ["query"], "rowLimit": 10}
    res = sc.searchanalytics().query(siteUrl=SITE, body=body).execute()
    tot = sc.searchanalytics().query(siteUrl=SITE, body={
        "startDate": str(start), "endDate": str(end)}).execute().get("rows", [{}])
    t = tot[0] if tot else {}
    print("【検索】")
    print(f"  クリック {int(t.get('clicks',0))}回 ／ 表示 {int(t.get('impressions',0))}回 "
          f"／ 順位 {t.get('position',0):.1f}位\n")
    print("  検索された言葉 上位10")
    for r in res.get("rows", []):
        print(f"    クリック{int(r['clicks']):>3}  表示{int(r['impressions']):>5}  "
              f"{r['position']:>5.1f}位  {r['keys'][0]}")
except Exception as e:
    print(f"【検索】取得できず：{e}")


# ────────────────────────────────────────────────
# コンバージョン（資料請求・来店予約）＝シバグラムの台帳から
# ────────────────────────────────────────────────
ENV_PATH = "/Users/sbbymac/Documents/SBB/koumuten-system/.env.local"
# 確実にテストと分かるものだけ自動で外す。
# ⚠️「営業」をメモで拾ってはいけない。お客様が「電話での営業は控えて」と書くことがあり、
#   実際に本物のお客様（丸山様）を誤って外した（2026-08-19）。
NG_WORDS = ["テスト", "test", "サンプル", "ダミー"]        # 名前・メモに含まれたら除外
NG_MAIL  = ["sales", "eigyou", "no-reply", "noreply"]     # 差出人が営業用アドレス

def db(sql):
    env = {}
    for line in open(ENV_PATH, encoding="utf-8"):
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    url = env["TURSO_DATABASE_URL"].replace("libsql://", "https://")
    body = {"requests": [{"type": "execute", "stmt": {"sql": sql}}, {"type": "close"}]}
    req = urllib.request.Request(url + "/v2/pipeline", data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + env["TURSO_AUTH_TOKEN"],
                 "Content-Type": "application/json"})
    res = json.loads(urllib.request.urlopen(req, timeout=60).read())["results"][0]
    if res["type"] != "ok":
        raise RuntimeError(res.get("error"))
    r = res["response"]["result"]
    return [[c.get("value") for c in row] for row in r["rows"]]

def eigyou(name, memo, mail=""):
    """営業・テストらしきものを見分ける。
       迷ったら「除外しない」。件数を少なく見せるより、見落とすほうがまだ良い。"""
    t = f"{name or ''} {memo or ''}"
    if any(w in t.lower() for w in [w.lower() for w in NG_WORDS]):
        return True
    if mail and any(w in mail.lower() for w in NG_MAIL):
        return True
    return False

try:
    # 資料請求だけを数える。予約フォームから入った人（source='HP'）は
    # 予約側で数えるので、ここに混ぜると二重になる（2026-08-19に実際に混ざった）
    shiryo = db(f"""select date(contact_date), name, coalesce(email,''), coalesce(notes,'')
                    from customers
                    where date(contact_date) between '{start}' and '{end}'
                      and inquiry_channel = '資料請求'""")
    yoyaku = db(f"""select date(created_at), customer_name, coalesce(customer_email,''),
                           coalesce(message,''), status, reservation_type
                    from reservations
                    where date(created_at) between '{start}' and '{end}'""")

    s_ok = [r for r in shiryo if not eigyou(r[1], r[3], r[2])]
    s_ng = [r for r in shiryo if eigyou(r[1], r[3], r[2])]
    y_ok = [r for r in yoyaku if not eigyou(r[1], r[3], r[2]) and r[4] != "cancelled"]
    y_ng = [r for r in yoyaku if eigyou(r[1], r[3], r[2])]
    y_cancel = [r for r in yoyaku if r[4] == "cancelled" and not eigyou(r[1], r[3], r[2])]

    print("\n【問い合わせ（いちばん大事な数字）】")
    print(f"  資料請求　{len(s_ok)}件")
    for d, nm, _, _ in s_ok:
        print(f"    {d}　{nm}")
    print(f"  来店・点検の予約　{len(y_ok)}件")
    for d, nm, _, _, _, t in y_ok:
        label = {"visit": "来店", "inspection": "点検", "meeting": "打合せ"}.get(t, t)
        print(f"    {d}　{nm}（{label}）")
    print(f"  合わせて {len(s_ok) + len(y_ok)}件")

    sess = num(jp_now)
    if sess:
        print(f"  訪問{sess}回に対する転換率　{(len(s_ok)+len(y_ok))/sess*100:.2f}%")
    if y_cancel:
        print(f"  ※取り消し {len(y_cancel)}件（件数に入れていません）")
    if s_ng or y_ng:
        print(f"  ※営業・テストとして除いたもの {len(s_ng)+len(y_ng)}件")
        for r in s_ng + y_ng:
            print(f"    {r[0]}　{r[1]}")
except Exception as e:
    print(f"\n【問い合わせ】台帳が読めませんでした：{e}")
