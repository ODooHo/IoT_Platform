import requests
import json

url = "http://203.253.128.177:7579/Mobius/sch_platform_4/Car_list"

payload = json.dumps({
  "m2m:cnt": {
    "lbl": [
      "Car_list",
      "status"
    ],
    "mbs": 16384
  }
})
headers = {
  'Accept': 'application/json',
  'X-M2M-RI': '12345',
  'X-M2M-Origin': 'Ssch_platform_4',
  'Content-Type': 'application/vnd.onem2m-res+json; ty=3'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)
