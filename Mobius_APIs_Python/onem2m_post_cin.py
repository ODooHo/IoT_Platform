import requests

url = 'http://203.253.128.161:7579/Mobius/sch20181497_/ledm'
headers =	{
				'Accept':'application/json',
				'X-M2M-RI':'12345',
				'X-M2M-Origin':'Ssch20181497_', # change to your aei
				'Content-Type':'application/vnd.onem2m-res+json; ty=4'
			}

data =	{
			"m2m:cin": {
				"con": "1"
			}
		}

r = requests.post(url, headers=headers, json=data)

try:
	r.raise_for_status()
	print(r)
except Exception as exc:
	print('There was a problem: %s' % (exc))
