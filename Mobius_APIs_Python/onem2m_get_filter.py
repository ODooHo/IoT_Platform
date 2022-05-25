# Created by J. Yun, SCH Univ., yun@sch.ac.kr

import requests

# uncomment one of three .url statements below
# 1. retrieve latest three cins
url = 'http://203.253.128.161:7579/Mobius/sch20181497_/dust?fu=2&la=3&ty=4&rcn=4'

# 2. retrieve three cins created after ct=20210512T100525
# url = 'http://203.253.128.161:7579/Mobius/sch19999999/dust?fu=2&lim=3&ty=4&rcn=4' \
# 		+ '&cra=20210512T100525'
			
# 3. retrieve three cins created after ct=20210512T100525 and before ct=20210512T100540
# url = 'http://203.253.128.161:7579/Mobius/sch19999999/dust?fu=2&lim=3&ty=4&rcn=4' \
# 		+ '&cra=20210512T100525&crb=20210512T100540"'

headers = {'Accept':'application/json',
			'X-M2M-RI':'12345',
			'X-M2M-Origin':'SOrigin'}

r = requests.get(url, headers=headers)

try:
	r.raise_for_status()
	jr = r.json()

	print(jr)
	for c in jr['m2m:rsp']['m2m:cin']:
		print(c['con'])
except Exception as exc:
	print('There was a problem: %s' % (exc))
