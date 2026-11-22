"""One monitoring-only activity commit per month avoids the public-repo inactivity cutoff."""
import base64
import datetime
import json
import os
import urllib.error
import urllib.request

url = 'https://api.github.com/repos/' + os.environ['GITHUB_REPOSITORY'] + '/contents/.github/monitor/active.json'
headers = {'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
           'Accept': 'application/vnd.github+json'}
sha = None
today = datetime.datetime.now(datetime.timezone.utc).date()
try:
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=20) as response:
        previous = json.load(response)
    sha = previous['sha']
    last = json.loads(base64.b64decode(previous['content']))['last_activity']
    if (today - datetime.date.fromisoformat(last)).days < 28:
        print('Monitoring activity is recent; no commit needed')
        raise SystemExit(0)
except urllib.error.HTTPError as error:
    if error.code != 404:
        raise

payload = {'message': 'Maintain external booking monitor activity',
           'content': base64.b64encode((json.dumps({'last_activity': str(today)}) + '\n').encode()).decode()}
if sha:
    payload['sha'] = sha
request = urllib.request.Request(url, method='PUT', headers=headers, data=json.dumps(payload).encode())
with urllib.request.urlopen(request, timeout=20) as response:
    result = json.load(response)
print('Monitoring-only monthly activity commit:', result['commit']['sha'])
