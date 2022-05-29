import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import requests
import urllib
import RPi.GPIO as GPIO
import time
from urllib.parse import quote_plus
from urllib.parse import unquote_plus

GPIO.setmode(GPIO.BCM)
# 초음파

B_TRIG = 27
B_ECHO = 22


# LED

B_RED = 5
B_GREEN = 6


GPIO.setup(B_TRIG, GPIO.OUT)
GPIO.setup(B_ECHO, GPIO.IN)
GPIO.setup(B_RED, GPIO.OUT)
GPIO.setup(B_GREEN, GPIO.OUT)

# CNT 여부 초기에 없다고 가정
ACNT = False
counter_B=0


def register_B(car):
    url = 'http://203.253.128.177:7579/Mobius/sch_platform_4/status/B'
    headers =	{'Accept':'application/json',
    'X-M2M-RI':'12345',
    'X-M2M-Origin':'Ssch_platform_4', # change to your aei
    'Content-Type':'application/vnd.onem2m-res+json; ty=3'
    }

    data =	{
        "m2m:cnt": {
            "rn": car
            }
            }

    r = requests.post(url, headers=headers, json=data)

    try:
	    r.raise_for_status()
	    print(r)
    except Exception as exc:
	    print('There was a problem: %s' % (exc))

def delete_car_B(car):
    url = ('http://203.253.128.177:7579/Mobius/sch_platform_4/status/B/%s' %car)
    headers =	{
        'Accept':'application/json',
        'X-M2M-RI':'12345',
        'X-M2M-Origin':'Ssch_platform_4', # change to your aei
        'Content-Type':'application/vnd.onem2m-res+json; ty=3'
        }
        
    payload= ""
    response = requests.request("DELETE", url, headers=headers, data=payload)



lists=[]

plt.style.use('dark_background')

img_ori = cv2.imread('B-2.jpeg')


height, width, channel = img_ori.shape
plt.figure(figsize=(12, 10))
plt.imshow(img_ori,cmap='gray')
print(height, width, channel)


print(height, width, channel)

gray = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
plt.figure(figsize=(12,10))
plt.imshow(gray, cmap='gray')

plt.show()
img_blurred = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)

img_blur_thresh = cv2.adaptiveThreshold(
    img_blurred,
    maxValue=255.0,
    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    thresholdType=cv2.THRESH_BINARY_INV,
    blockSize=19,
    C=9
)
img_thresh = cv2.adaptiveThreshold(
    gray,
    maxValue=255.0,
    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    thresholdType=cv2.THRESH_BINARY_INV,
    blockSize=19,
    C=9
)

plt.figure(figsize=(20,20))
plt.subplot(1,2,1)
plt.title('Threshold only')
plt.imshow(img_thresh, cmap='gray')
plt.subplot(1,2,2)
plt.title('Blur and Threshold')
plt.imshow(img_blur_thresh, cmap='gray')



contours, _ = cv2.findContours(
    img_blur_thresh,
    mode=cv2.RETR_LIST,
    method=cv2.CHAIN_APPROX_SIMPLE
)

temp_result = np.zeros((height, width, channel), dtype=np.uint8)

cv2.drawContours(temp_result, contours=contours, contourIdx=-1, color=(255,255,255))
plt.figure(figsize=(12, 10))
plt.imshow(temp_result)


temp_result = np.zeros((height, width, channel), dtype=np.uint8)

contours_dict = []

for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(temp_result, pt1=(x, y), pt2=(x + w, y + h), color=(255, 255, 255), thickness=2)

    contours_dict.append({
        'contour': contour,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'cx': x + (w / 2),
        'cy': y + (h / 2)
    })
plt.figure(figsize=(12,10))
plt.imshow(temp_result, cmap='gray')


MIN_AREA = 80
MIN_WIDTH, MIN_HEIGHT = 2, 8
MIN_RATIO, MAX_RATIO = 0.25, 1.0

possible_contours = []

cnt = 0
for d in contours_dict:
    area = d['w'] * d['h']
    ratio = d['w'] / d['h']

    if area > MIN_AREA \
            and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT \
            and MIN_RATIO < ratio < MAX_RATIO:
        d['idx'] = cnt
        cnt += 1
        possible_contours.append(d)

temp_result = np.zeros((height, width, channel), dtype=np.uint8)

for d in possible_contours:
    cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x'] + d['w'], d['y'] + d['h']), color=(255, 255, 255),
                  thickness=2)

plt.figure(figsize=(12, 10))
plt.imshow(temp_result, cmap='gray')
plt.show()

MAX_DIAG_MULTIPLYER = 5
MAX_ANGLE_DIFF = 12.0
MAX_AREA_DIFF = 0.5
MAX_WIDTH_DIFF = 0.8
MAX_HEIGHT_DIFF = 0.2
MIN_N_MATCHED = 3


def find_chars(contour_list):
    matched_result_idx = []

    for d1 in contour_list:
        matched_contours_idx = []
        for d2 in contour_list:
            if d1['idx'] == d2['idx']:
                continue

            dx = abs(d1['cx'] - d2['cx'])
            dy = abs(d1['cy'] - d2['cy'])

            diagonal_length1 = np.sqrt(d1['w'] ** 2 + d1['h'] ** 2)

            distance = np.linalg.norm(np.array([d1['cx'], d1['cy']]) - np.array([d2['cx'], d2['cy']]))
            if dx == 0:
                angle_diff = 90
            else:
                angle_diff = np.degrees(np.arctan(dy / dx))
            area_diff = abs(d1['w'] * d1['h'] - d2['w'] * d2['h']) / (d1['w'] * d1['h'])
            width_diff = abs(d1['w'] - d2['w']) / d1['w']
            height_diff = abs(d1['h'] - d2['h']) / d1['h']

            if distance < diagonal_length1 * MAX_DIAG_MULTIPLYER \
                    and angle_diff < MAX_ANGLE_DIFF and area_diff < MAX_AREA_DIFF \
                    and width_diff < MAX_WIDTH_DIFF and height_diff < MAX_HEIGHT_DIFF:
                matched_contours_idx.append(d2['idx'])

        matched_contours_idx.append(d1['idx'])

        if len(matched_contours_idx) < MIN_N_MATCHED:
            continue

        matched_result_idx.append(matched_contours_idx)

        unmatched_contour_idx = []
        for d4 in contour_list:
            if d4['idx'] not in matched_contours_idx:
                unmatched_contour_idx.append(d4['idx'])

        unmatched_contour = np.take(possible_contours, unmatched_contour_idx)

        recursive_contour_list = find_chars(unmatched_contour)

        for idx in recursive_contour_list:
            matched_result_idx.append(idx)

        break

    return matched_result_idx


result_idx = find_chars(possible_contours)

matched_result = []
for idx_list in result_idx:
    matched_result.append(np.take(possible_contours, idx_list))

temp_result = np.zeros((height, width, channel), dtype=np.uint8)

for r in matched_result:
    for d in r:
        cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x'] + d['w'], d['y'] + d['h']), color=(255, 255, 255),
                      thickness=2)

PLATE_WIDTH_PADDING = 1.3  # 1.3
PLATE_HEIGHT_PADDING = 1.5  # 1.5
MIN_PLATE_RATIO = 3
MAX_PLATE_RATIO = 10

plate_imgs = []
plate_infos = []

for i, matched_chars in enumerate(matched_result):
    sorted_chars = sorted(matched_chars, key=lambda x: x['cx'])

    plate_cx = (sorted_chars[0]['cx'] + sorted_chars[-1]['cx']) / 2
    plate_cy = (sorted_chars[0]['cy'] + sorted_chars[-1]['cy']) / 2

    plate_width = (sorted_chars[-1]['x'] + sorted_chars[-1]['w'] - sorted_chars[0]['x']) * PLATE_WIDTH_PADDING

    sum_height = 0
    for d in sorted_chars:
        sum_height += d['h']

    plate_height = int(sum_height / len(sorted_chars) * PLATE_HEIGHT_PADDING)

    triangle_height = sorted_chars[-1]['cy'] - sorted_chars[0]['cy']
    triangle_hypotenus = np.linalg.norm(
        np.array([sorted_chars[0]['cx'], sorted_chars[0]['cy']]) -
        np.array([sorted_chars[-1]['cx'], sorted_chars[-1]['cy']])
    )

    angle = np.degrees(np.arcsin(triangle_height / triangle_hypotenus))

    rotation_matrix = cv2.getRotationMatrix2D(center=(plate_cx, plate_cy), angle=angle, scale=1.0)

    img_rotated = cv2.warpAffine(img_thresh, M=rotation_matrix, dsize=(width, height))

    img_cropped = cv2.getRectSubPix(
        img_rotated,
        patchSize=(int(plate_width), int(plate_height)),
        center=(int(plate_cx), int(plate_cy))
    )

    if img_cropped.shape[1] / img_cropped.shape[0] < MIN_PLATE_RATIO or img_cropped.shape[1] / img_cropped.shape[
        0] < MIN_PLATE_RATIO > MAX_PLATE_RATIO:
        continue

    plate_imgs.append(img_cropped)
    plate_infos.append({
        'x': int(plate_cx - plate_width / 2),
        'y': int(plate_cy - plate_height / 2),
        'w': int(plate_width),
        'h': int(plate_height)
    })

    plt.subplot(len(matched_result), 1, i + 1)
    plt.imshow(img_cropped, cmap='gray')
    plt.show()

longest_idx, longest_text = -1, 0
plate_chars = []

for i, plate_img in enumerate(plate_imgs):
    plate_img = cv2.resize(plate_img, dsize=(0, 0), fx=1.6, fy=1.6)
    _, plate_img = cv2.threshold(plate_img, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # find contours again (same as above)
    contours, _ = cv2.findContours(plate_img, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)

    plate_min_x, plate_min_y = plate_img.shape[1], plate_img.shape[0]
    plate_max_x, plate_max_y = 0, 0

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        area = w * h
        ratio = w / h

        if area > MIN_AREA \
                and w > MIN_WIDTH and h > MIN_HEIGHT \
                and MIN_RATIO < ratio < MAX_RATIO:
            if x < plate_min_x:
                plate_min_x = x
            if y < plate_min_y:
                plate_min_y = y
            if x + w > plate_max_x:
                plate_max_x = x + w
            if y + h > plate_max_y:
                plate_max_y = y + h

    img_result = plate_img[plate_min_y:plate_max_y, plate_min_x:plate_max_x]

    img_result = cv2.GaussianBlur(img_result, ksize=(3, 3), sigmaX=0)
    _, img_result = cv2.threshold(img_result, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_result = cv2.copyMakeBorder(img_result, top=10, bottom=10, left=10, right=10, borderType=cv2.BORDER_CONSTANT,
                                    value=(0, 0, 0))

    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
    chars = pytesseract.image_to_string(img_result, lang='kor', config='--psm 7 --oem 0')

    result_chars = ''
    has_digit = False
    for c in chars:
        if ord('가') <= ord(c) <= ord('힣') or c.isdigit():
            if c.isdigit():
                has_digit = True
            result_chars += c

    print(result_chars)
    plate_chars.append(result_chars)

    if has_digit and len(result_chars) > longest_text:
        longest_idx = i

    plt.subplot(len(plate_imgs), 1, i + 1)
    plt.imshow(img_result, cmap='gray')

info = plate_infos[longest_idx]
chars = plate_chars[longest_idx]

print(chars)

img_out = img_ori.copy()

cv2.rectangle(img_out, pt1=(info['x'], info['y']), pt2=(info['x']+info['w'], info['y']+info['h']), color=(255,0,0), thickness=2)

cv2.imwrite(chars + '.jpg', img_out)

plt.figure(figsize=(12, 10))
plt.imshow(img_out)
plt.show()

car = quote_plus(result_chars)


try : 
    while True :
        GPIO.output(B_TRIG, False)
        time.sleep(0.00001)

        GPIO.output(B_TRIG, True)
        time.sleep(0.00001)
        GPIO.output(B_TRIG, False)

        # Echo가 OFF 되는 시점을 시작 시간으로 잡기
        while GPIO.input(B_ECHO) == 0: 
            B_START = time.time()

        # Echo가 다시 ON이 되는 시점을 수신시간으로 잡기
        while GPIO.input(B_ECHO) == 1:     
            B_STOP = time.time()

        # 초음파가 수신되는 시간으로 거리 계산
        B_T = B_STOP - B_START
        B_L = B_T * 17000
        B_L = round(B_L, 2)

        # 거리 오류
        if (B_L >= 200 or B_L <= 0) :
            print("-1")

        # 주차자리 있음 (초록불)
        elif (B_L > 15 and B_L <= 40) :
            #print('Distance is ', L, ' cm')
            GPIO.output(B_RED, GPIO.LOW)
            GPIO.output(B_GREEN, GPIO.HIGH)
            if ACNT == True:
                delete_car_B(car)
                ACNT = False


        # 주차자리 없음 (빨간불)
        elif (B_L <= 15) :
            counter_B+=1
            #print('Distance is ', L, ' cm')
            if ACNT == False and counter_B==100:
                GPIO.output(B_RED, GPIO.HIGH)
                GPIO.output(B_GREEN, GPIO.LOW)
                register_B(car)
                ACNT = True
                counter_B=0

        time.sleep(0.1)
        
except KeyboardInterrupt:
    GPIO.cleanup()



##A초음파, B초음파, H(handicap)초음파 있다고 가정
##A 주차 완료 -> register_A(인수 car)
##A초음파에서,차량 나감 -> delete_car_A(인수 car)
##flag = 차량 나가고 들어오고 판별

# if A:
#     register_A(car)
# elif B:
#     register_B(car)
# elif H:
#     register_H(car)

# if flag_A:
#     delete_car_A(car)
# elif flag_B:
#     delete_car_B(car)
# elif flag_H:
#     delete_car_H(car)
