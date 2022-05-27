# -*- coding: utf-8 -*-
# Created by J. Yun, SCH Univ., yun@sch.ac.kr
import requests
import urllib
from urllib.parse import quote_plus
from urllib.parse import unquote_plus

num_list = []
name = []
# uncomment one of three .url statements below
# 1. retrieve latest three cins
url = 'http://203.253.128.177:7579/Mobius/sch_platform_4_/number?fu=2&la=3&ty=3&rcn=4'

# 2. retrieve three cins created after ct=20210512T100525
# url = 'http://203.253.128.161:7579/Mobius/sch19999999/dust?fu=2&lim=3&ty=4&rcn=4' \
# 		+ '&cra=20210512T100525'

# 3. retrieve three cins created after ct=20210512T100525 and before ct=20210512T100540
# url = 'http://203.253.128.161:7579/Mobius/sch19999999/dust?fu=2&lim=3&ty=4&rcn=4' \
# 		+ '&cra=20210512T100525&crb=20210512T100540"'

headers = {'Accept': 'application/json',
           'X-M2M-RI': '12345',
           'X-M2M-Origin': 'SOrigin'}

r = requests.get(url, headers=headers)

try:
    r.raise_for_status()
    jr = r.json()

    print(jr)
    for c in jr['m2m:rsp']['m2m:cnt']:
        num_list.append(c['rn'])
        print(c['rn'])
except Exception as exc:
    print('There was a problem: %s' % (exc))

url = 'http://203.253.128.177:7579/Mobius/sch_platform_4_/number?fu=2&la=1&ty=3&rcn=4'
headers = {'Accept': 'application/json',
           'X-M2M-RI': '12345',
           'X-M2M-Origin': 'SOrigin'}

r = requests.get(url, headers=headers)
try:
    r.raise_for_status()
    jr = r.json()
    print(jr)
    for c in jr['m2m:rsp']['m2m:cnt']:
        name = c['rn']
except Exception as exc:
    print('There was a problem: %s' % (exc))
flag = False
print(name)
for i in range(len(num_list)):
    if num_list[i] == name:
        flag = True
        break
    else:
        continue

url = ('http://203.253.128.177:7579/Mobius/sch_platform_4_/number/%s' % name)
headers = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'Ssch_platform_4_',  # change to your aei
    'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
}
if flag:
    data = {
        "m2m:cin": {
            "con": "1"
        }
    }
else:
    data = {
        "m2m:cin": {
            "con": "0"
        }
    }

r = requests.post(url, headers=headers, json=data)
try:
    r.raise_for_status()
    print(r)
except Exception as exc:
    print('There was a problem: %s' % (exc))

