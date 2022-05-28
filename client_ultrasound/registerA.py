import RPi.GPIO as GPIO
import time
import requests

GPIO.setmode(GPIO.BCM)
# 초음파
A_TRIG = 23
A_ECHO = 24

# LED
A_RED = 17
A_GREEN = 18

GPIO.setup(A_TRIG, GPIO.OUT)
GPIO.setup(A_ECHO, GPIO.IN)
GPIO.setup(A_RED, GPIO.OUT)
GPIO.setup(A_GREEN, GPIO.OUT)

# CNT 여부 초기에 없다고 가정
ACNT = False

def C_CNT_A():
    url = "http://203.253.128.177:7579/Mobius/sch20201529/button"

    payload = "{\n  \"m2m:cnt\": {\n    \"rn\": \"A\",\n    \"lbl\": [\"A\"],\n    \"mbs\": 16384\n  }\n}"

    headers = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'Ssch20201529',
    'Content-Type': 'application/vnd.onem2m-res+json; ty=3'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

def D_CNT_A():
    url = "http://203.253.128.177:7579/Mobius/sch20201529/button/A"

    payload = ""

    headers = {
    'Accept': 'application/json',
    'locale': 'ko',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'Ssch20201529'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    print(response.text)


try : 
    while True :
        GPIO.output(A_TRIG, False)
        time.sleep(0.00001)

        GPIO.output(A_TRIG, True)
        time.sleep(0.00001)
        GPIO.output(A_TRIG, False)

        # Echo가 OFF 되는 시점을 시작 시간으로 잡기
        while GPIO.input(A_ECHO) == 0: 
            A_START = time.time()

        # Echo가 다시 ON이 되는 시점을 수신시간으로 잡기
        while GPIO.input(A_ECHO) == 1:     
            A_STOP = time.time()

        # 초음파가 수신되는 시간으로 거리 계산
        A_T = A_STOP - A_START
        A_L = A_T * 17000
        A_L = round(A_L, 2)

        # 거리 오류
        if (A_L >= 200 or A_L <= 0) :
            print("-1")

        # 주차자리 있음 (초록불)
        elif (A_L > 15 and A_L <= 40) :
            GPIO.output(A_RED, GPIO.LOW)
            GPIO.output(A_GREEN, GPIO.HIGH)
            #print('Distance is ', L, ' cm')

            if ACNT == True :
                D_CNT_A()
                ACNT = False


        # 주차자리 없음 (빨간불)
        elif (A_L <= 15) :
            GPIO.output(A_RED, GPIO.HIGH)
            GPIO.output(A_GREEN, GPIO.LOW)
            #print('Distance is ', L, ' cm')

            if ACNT == False :
                C_CNT_A()
                ACNT = True

        time.sleep(0.1)
        
except KeyboardInterrupt:
    GPIO.cleanup()