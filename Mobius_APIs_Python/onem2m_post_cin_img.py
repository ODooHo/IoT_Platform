# Created by J. Yun, SCH Univ., yun@sch.ac.kr

import requests
import base64

url = 'http://203.253.128.161:7579/Mobius/sch20181497_/img'
headers =	{
				'Accept':'application/json',
				'X-M2M-RI':'12345',
				'X-M2M-Origin':'Ssch20181497_', # change to your aei
				'Content-Type':'application/vnd.onem2m-res+json; ty=4'
			}

with open("oneM2M_logo.png", "rb") as img:
    enc_str = base64.b64encode(img.read()).decode('utf-8')
# print(enc_str)

# print(enc_str)
data =	{
			"m2m:cin": {
				"con": enc_str
			}
		}

r = requests.post(url, headers=headers, json=data)

try:
	r.raise_for_status()
	jr = r.json()
	
	print(jr)
	print(jr['m2m:cin']['con'])
except Exception as exc:
	print('There was a problem: %s' % (exc))
