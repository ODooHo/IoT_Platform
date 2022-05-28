import requests
import urllib
from urllib.parse import quote_plus
from urllib.parse import unquote_plus

url = 'http://203.253.128.177:7579/Mobius/sch_platform_4/Car_list/A?fu=2&la=5&ty=3&rcn=4'

headers = {'Accept': 'application/json',
           'X-M2M-RI': '12345',
           'X-M2M-Origin': 'SOrigin'}

r = requests.get(url, headers=headers)

try:
    r.raise_for_status()
    jr = r.json()
    for c in jr['m2m:rsp']['m2m:cnt']:
        name=unquote_plus(c['rn'])
        print(name)
except Exception as exc:
    print('There was a problem: %s' % (exc))
