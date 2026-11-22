"""Independent, read-only booking monitor; no booking POSTs, analytics or customer data."""
import concurrent.futures
import datetime
import email.message
import hashlib
import json
import os
import smtplib
import ssl
import time
import urllib.error
import urllib.request

BASE = 'https://www.shibasun.jp'
TARGETS = [BASE + '/', BASE + '/reserve', BASE + '/booking-flow.js',
           BASE + '/booking-flow.css',
           'https://shibagram.onrender.com/api/public/slots?type=visit&includeFull=1']
STATE_TITLE = '[booking-health] Current incident'
RECIPIENT = 'yasuhiro@shibasun.jp'


def probe(url):
    for attempt in range(1, 3):
        result = {'url': url, 'ok': False, 'attempts': attempt}
        try:
            request = urllib.request.Request(url, headers={
                'User-Agent': 'Shibasun-Booking-Health/1.0', 'Origin': BASE})
            with urllib.request.urlopen(request, timeout=20) as response:
                data = response.read(2_000_000)
                text = data.decode('utf-8')
                result['status'] = response.status
                result['ok'] = response.status == 200
                if '/api/public/slots' in url:
                    slots = json.loads(text).get('slots')
                    result['ok'] = result['ok'] and isinstance(slots, list)
                    if result['ok']:
                        result['ok'] = all(isinstance(s, dict) and
                            isinstance(s.get('id'), str) and s.get('status') in ('open', 'full')
                            for s in slots)
                        result['slot_count'] = len(slots)
                        result['open_count'] = sum(s.get('status') == 'open' for s in slots)
                    result['ok'] = result['ok'] and response.headers.get(
                        'Access-Control-Allow-Origin') in ('*', BASE)
                elif url in (BASE + '/', BASE + '/reserve'):
                    result['ok'] = result['ok'] and all(marker in text for marker in
                        ('id="rsv-app"', 'async function rsvLoad()', 'id="kouho"'))
                else:
                    result['ok'] = result['ok'] and len(data) > 100 and '<html' not in text[:200].lower()
                if result['ok']:
                    return result
                result['error'] = 'invalid_response'
        except urllib.error.HTTPError as error:
            result.update(ok=False, status=error.code, error='http_error')
        except Exception as error:
            result.update(ok=False, error=type(error).__name__)
        if attempt == 1:
            time.sleep(2)
    return result


def github(path, method='GET', payload=None):
    request = urllib.request.Request(
        'https://api.github.com/repos/' + os.environ['GITHUB_REPOSITORY'] + path,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
                 'Accept': 'application/vnd.github+json',
                 'X-GitHub-Api-Version': '2022-11-28'}, method=method)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def mail(subject, text):
    # Existing company SMTP account, encrypted repository secrets; never print credentials.
    message = email.message.EmailMessage()
    message['From'] = 'シバサンホーム 予約サイト監視 <yasuhiro@shibasun.jp>'
    message['To'] = RECIPIENT
    message['Subject'] = subject
    message.set_content(text)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=25,
                          context=ssl.create_default_context()) as smtp:
        smtp.login(os.environ['MONITOR_SMTP_USER'], os.environ['MONITOR_SMTP_PASSWORD'])
        smtp.send_message(message)


def transition(previous, signature):
    if signature:
        return 'failed' if previous is None else ('changed' if previous != signature else 'unchanged')
    return 'recovered' if previous is not None else 'unchanged'


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(probe, TARGETS))
    failed = [item for item in results if not item['ok']]
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()
    run_url = 'https://github.com/' + os.environ['GITHUB_REPOSITORY'] + '/actions/runs/' + os.environ['GITHUB_RUN_ID']
    summary = json.dumps({'checked_at': now, 'healthy': not failed, 'results': results}, ensure_ascii=False, indent=2)
    print(summary)
    with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as file:
        file.write('## 予約サイト監視\n\n```json\n' + summary + '\n```\n')

    # A test sends one labelled email and does not alter real incident state.
    if os.environ.get('NOTIFICATION_TEST') == 'true':
        mail('【監視テスト】予約サイトの通知を確認しています',
             'これは通知の到着確認用です。異常発生のお知らせではありません。\n\n'
             'CodexやMacを閉じていても、外部から30分ごとに予約画面と空き枠を確認します。\n'
             '異常を検出したときと復旧したときに、このメールでお知らせします。\n'
             '広告予算は変更していません。\n\n確認日時: ' + now + '\n確認記録: ' + run_url)
        print('Notification test accepted by SMTP server')

    issues = github('/issues?state=open&per_page=100')
    incidents = [issue for issue in issues if issue['title'] == STATE_TITLE and issue['user']['login'] == 'github-actions[bot]' and 'pull_request' not in issue]
    if len(incidents) > 1:
        raise RuntimeError('Multiple monitor state issues; refusing duplicate notification')
    incident = incidents[0] if incidents else None
    previous = json.loads(incident['body'])['signature'] if incident else None
    signature = hashlib.sha256(json.dumps([
        {key: item.get(key) for key in ('url', 'status', 'error')} for item in failed
    ], sort_keys=True).encode()).hexdigest() if failed else None
    change = transition(previous, signature)
    print('Monitor transition:', change)
    if change == 'unchanged':
        return
    if change in ('failed', 'changed'):
        text = ('予約画面または空き枠の読み込みに異常を検出しました。\n'
                '自動で再確認しても正常な応答を得られていません。\n'
                '予約操作の最終送信までは検査していません。\n\n' + summary + '\n\n確認記録: ' + run_url)
        mail('【要確認】シバサンホームの予約画面・空き枠に異常', text)
        body = json.dumps({'signature': signature, 'checked_at': now, 'failed': failed}, ensure_ascii=False)
        if incident:
            github('/issues/' + str(incident['number']), 'PATCH', {'body': body})
        else:
            github('/issues', 'POST', {'title': STATE_TITLE, 'body': body})
    else:
        mail('【復旧】シバサンホームの予約画面・空き枠',
             '予約画面と空き枠の読み込みが正常に戻ったことを確認しました。\n\n' + summary + '\n\n確認記録: ' + run_url)
        github('/issues/' + str(incident['number']), 'PATCH', {'state': 'closed', 'state_reason': 'completed'})


if __name__ == '__main__':
    main()
