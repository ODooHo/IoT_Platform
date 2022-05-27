# -*- coding: utf-8 -*-
# Created by J. Yun, SCH Univ., yun@sch.ac.kr
import requests
import urllib
from urllib.parse import quote_plus
from urllib.parse import unquote_plus

# uncomment one of three .url statements below
# 1. retrieve latest three cins
url = 'http://203.253.128.177:7579/Mobius/sch_platform_4_/number?fu=2&la=5&ty=3&rcn=4'

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
    for c in jr['m2m:rsp']['m2m:cnt']:
        name=unquote_plus(c['rn'])
        print(name)
except Exception as exc:
    print('There was a problem: %s' % (exc))
