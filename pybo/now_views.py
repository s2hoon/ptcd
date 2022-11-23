#기상청 단기예보
#from ..models import WeatherDB
from django.shortcuts import render

import os
import requests
from urllib.parse import urlencode, unquote, quote_plus
from datetime import datetime, timedelta, date
import math

import json
import googlemaps #역지오코딩

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #InsecureReuquestWarning 예외처리


def set_base_time():
    #현재시간 가져오기
    now = datetime.now()
    time=now.strftime("%H%M")
    
    #날씨데이터를 언제시각부터 가져올지 설정
    start_time  = time[0] + time[1] + '00'

    #날짜 가져오기
    today = datetime.today().strftime("%Y%m%d") 
    y = date.today() - timedelta(days=1)
    yesterday = y.strftime("%Y%m%d")    
    
    if int('0000') <= int(time) < int('0210'):
        base_date = yesterday
        base_time = '2300'
    elif int('0210') <= int(time) < int('0510'):
        base_date = today
        base_time = '0200'
    elif int('0510') <= int(time) < int('0810'):
        base_date = today
        base_time = '0500'
    elif int('8210') <= int(time) < int('1110'):
        base_date = today
        base_time = '0800'
    elif int('1110') <= int(time) < int('1410'):
        base_date = today
        base_time = '1100'
    elif int('1410') <= int(time) < int('1710'):
        base_date = today
        base_time = '1400'
    elif int('1710') <= int(time) < int('2010'):
        base_date = today
        base_time = '1700'
    elif int('2010') <= int(time) < int('2310'):
        base_date = today
        base_time = '2000'

    return base_date, base_time, start_time

#역지오코딩을 활용하여 주소를 문자열로 변환하는 함ㅅ
def reverse_geocoding(latitude, longitude):
    #역지오코딩을 활용하여 주소를 문자열로 변환
    GOOGLE_API_KEY = 'AIzaSyAOgov4B8S6uESOZ9J-wnav-6_6bcJSyUI'
    gmaps = googlemaps.Client(GOOGLE_API_KEY)
    reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude), language='ko')
    #print(reverse_geocode_result[4]['formatted_address'])
    return reverse_geocode_result[4]['formatted_address']


#geolocation으로 현재 위치좌표 가져오는 함수
def get_curr_loc():
    
    LOCATION_API_KEY = "AIzaSyAOgov4B8S6uESOZ9J-wnav-6_6bcJSyUI" # 공공데이터 포털에서 생성된 본인의 서비스 키를 복사 / 붙여넣기
    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={LOCATION_API_KEY}'
    data = {
        'considerIp': True,
    }

    result = requests.post(url, data)

    #json -> dict 변환
    loc = result.json()

    latitude = loc['location']['lat']
    longitude = loc['location']['lng']

    return latitude, longitude

#위, 경도를 x, y 좌표로 변경하는 함수
#x, y 좌표란? 기상청 날씨의 api 요청변수
def map_to_xy(lat, lng):

    NX = 149            ## X축 격자점 수
    NY = 253            ## Y축 격자점 수

    Re = 6371.00877     ##  지도반경
    grid = 5.0          ##  격자간격 (km)
    slat1 = 30.0        ##  표준위도 1
    slat2 = 60.0        ##  표준위도 2
    olon = 126.0        ##  기준점 경도
    olat = 38.0         ##  기준점 위도
    xo = 210 / grid     ##  기준점 X좌표
    yo = 675 / grid     ##  기준점 Y좌표
    first = 0


    if first == 0 :
        PI = math.asin(1.0) * 2.0
        DEGRAD = PI/ 180.0
        RADDEG = 180.0 / PI

        re = Re / grid
        slat1 = slat1 * DEGRAD
        slat2 = slat2 * DEGRAD
        olon = olon * DEGRAD
        olat = olat * DEGRAD

        sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
        sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
        sf = math.tan(PI * 0.25 + slat1 * 0.5)
        sf = math.pow(sf, sn) * math.cos(slat1) / sn
        ro = math.tan(PI * 0.25 + olat * 0.5)
        ro = re * sf / math.pow(ro, sn)
        first = 1

    def mapToGrid(lat, lon, code = 0 ):
        ra = math.tan(PI * 0.25 + lat * DEGRAD * 0.5)
        ra = re * sf / pow(ra, sn)
        theta = lon * DEGRAD - olon
        if theta > PI :
            theta -= 2.0 * PI
        if theta < -PI :
            theta += 2.0 * PI
        theta *= sn
        x = (ra * math.sin(theta)) + xo
        y = (ro - ra * math.cos(theta)) + yo
        x = int(x + 1.5)
        y = int(y + 1.5)
        return x, y

    return mapToGrid(lat, lng)

# 현재시간으로 날씨 데이터를 가져오는 함수
def getVilageFsct(nx, ny):
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'

    serviceKey = 'K7Y1L9rDTVLkFGhZPl2QeAvG9KUmWK2qQmclmrNffL%2FUQYQipP1%2BCi6HFeFV1kSN6Gi2KJ49tuimf35PFy579A%3D%3D'
    serviceKeyDecoded = unquote(serviceKey, 'UTF-8') # 공공데이터 포털에서 제공하는 서비스키는 이미 인코딩된 상태이므로, 디코딩하여 사용해야 함

    #현재시간을 구하는 기존 함수를 사용
    now = datetime.now()
    today = datetime.today().strftime("%Y%m%d") #오늘
    y = date.today() - timedelta(days=1)
    yesterday = y.strftime("%Y%m%d") #어제
    y = date.today() + timedelta(days=1)
    tomorrow = y.strftime("%Y%m%d") #내일
    y = date.today() + timedelta(days=2) 
    after_tomorrow = y.strftime("%Y%m%d") #모레

    #base_date, base_time을 전날 23시로 설정
    base_date = yesterday
    base_time = "2300"

    #파라미터 설정_오늘
    queryParams = '?' + urlencode({
    quote_plus("serviceKey"): serviceKeyDecoded,     
    quote_plus("numOfRows"): "872", #1시간당 받아올 수 있는 날씨정보는 12개, 하루동안 받아올수 있느 날씨 정보는 288개 + 2개(TMN, TMX(최고기온, 최저기온))          
    quote_plus("pageNo"): "1",              
    quote_plus("dataType"): "JSON",         
    quote_plus("base_date"): base_date,    
    quote_plus("base_time"): base_time,        
    quote_plus("nx"): nx,                
    quote_plus("ny"): ny                 
    })

    # print(url + queryParams)
    #오늘 값 요청 (웹 블우저 서버에서 요청 - url주소와 파라미터)
    res = requests.get(url + queryParams, verify=False) # verify=False이거 안 넣으면 에러남ㅜㅜ
    items = res.json().get('response').get('body').get('items') #데이터들 아이템에 json 형태로 저장


    

    
    #오늘의 날씨 dict 저장
    tmn, tmx = int, int
    today_weather = dict() 
    tomorrow_weather = dict()
    after_tomorrow_weather = dict()

    for i in range(0, 24):
        today_weather[i] = {}
        tomorrow_weather[i] = {}
        after_tomorrow_weather[i] = {}

    #주간날씨중 오늘 ~ +2일 날씨 데이터 저장
    week_data = {}
    for i in range(0, 3):
        week_data[i] = {}
        
    
    for item in items['item']:
        time = item['fcstTime'][:2]
        time = int(time)
        #오늘자
        if item['fcstDate'] == today:
            # 기온
            if item['category'] == 'TMP':
                today_weather[time]['tmp'] = item['fcstValue']
            # 습도
            if item['category'] == 'REH':
                today_weather[time]['hum'] = item['fcstValue']
            # 하늘상태
            if item['category'] == 'SKY':
                today_weather[time]['sky'] = item['fcstValue']
            # 눈/비
            if item['category'] == 'PTY':
                today_weather[time]['pty'] = item['fcstValue']
            

            #최저기온 
            if item['category'] == 'TMN':
                    # today_weather['tmn'] = item['fcstValue']
                    t_tmn = item['fcstValue']
                    tmn = str(int(float(t_tmn)))
                    week_data[0]['min'] = tmn
            #최고기온 
            if item['category'] == 'TMX':
                    # today_weather['tmx'] = item['fcstValue']
                    t_tmx = item['fcstValue']
                    tmx = str(int(float(t_tmx)))
                    week_data[0]['max'] = tmx
            
        #내일자
        elif item['fcstDate'] == tomorrow:
            # 기온
            if item['category'] == 'TMP':
                tomorrow_weather[time]['tmp'] = item['fcstValue']
            # 습도
            if item['category'] == 'REH':
                tomorrow_weather[time]['hum'] = item['fcstValue']
            # 하늘상태
            if item['category'] == 'SKY':
                tomorrow_weather[time]['sky'] = item['fcstValue']
            # 눈/비
            if item['category'] == 'PTY':
                tomorrow_weather[time]['pty'] = item['fcstValue']

             #최저기온 
            if item['category'] == 'TMN':
                    m = item['fcstValue']
                    week_data[1]['min'] = str(int(float(m)))
            #최고기온 
            if item['category'] == 'TMX':
                   m = item['fcstValue']
                   week_data[1]['max'] = str(int(float(m)))

        #모레자
        elif item['fcstDate'] == after_tomorrow:
            # 기온
            if item['category'] == 'TMP':
                after_tomorrow_weather[time]['tmp'] = item['fcstValue']
            # 습도
            if item['category'] == 'REH':
                after_tomorrow_weather[time]['hum'] = item['fcstValue']
            # 하늘상태
            if item['category'] == 'SKY':
                after_tomorrow_weather[time]['sky'] = item['fcstValue']
            # 눈/비
            if item['category'] == 'PTY':
                after_tomorrow_weather[time]['pty'] = item['fcstValue']

            #최저기온 
            if item['category'] == 'TMN':
                    m = item['fcstValue']
                    week_data[2]['min'] = str(int(float(m)))
            #최고기온 
            if item['category'] == 'TMX':
                    m = item['fcstValue']
                    week_data[2]['max'] = str(int(float(m)))
    



    t_tmx = float(t_tmx) #최고기온
    t_tmn = float(t_tmn) #최저기온
    m = datetime.today().strftime("%m") #'월'을 추출
    w = '' #문구
    if m == '6' or m == '7' or m == '8':
        if t_tmx >= 21.0:
            w = '(21°↑)과도한 냉방사용에 주의하세요'
    elif m == '11' or m == '12' or m == '1' or m == '2':
        if t_tmn <= 10.0:
            w = '(10°↓)과도한 난방사용에 주의하세요'
    else: 
        w = ''
    
    
    return today_weather, tomorrow_weather, after_tomorrow_weather, tmn, tmx, week_data, w

def getUltraSrtFcst(nx, ny):
    # 기상청_동네 예보 조회 서비스 api 데이터 url 주소, 초단기이기때문에 getUltraSrtFcst 사용
    url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"

    serviceKey = "K7Y1L9rDTVLkFGhZPl2QeAvG9KUmWK2qQmclmrNffL%2FUQYQipP1%2BCi6HFeFV1kSN6Gi2KJ49tuimf35PFy579A%3D%3D" # 공공데이터 포털에서 생성된 본인의 서비스 키를 복사 / 붙여넣기
    serviceKeyDecoded = unquote(serviceKey, 'UTF-8') # 공공데이터 포털에서 제공하는 서비스키는 이미 인코딩된 상태이므로, 디코딩하여 사용해야 함

    #현재시간을 구하는 기존 함수를 사용
    now = datetime.now()
    today = datetime.today().strftime("%Y%m%d")
    y = date.today() - timedelta(days=1)
    yesterday = y.strftime("%Y%m%d")
    #print(today)
    #print(yesterday)
    pre_hour = 0
    #base_time와 base_date를 구하는 함수
    if now.minute < 45:
            if now.hour == 0:
                base_time = "2330"
                base_date = yesterday
            else:
                pre_hour = now.hour -1
                if pre_hour < 10:
                    base_time = "0" + str(pre_hour) + "30"
                else:
                    base_time = str(pre_hour) + "30"
                base_date = today
    else:
        if now.hour < 10:
            base_time = "0" + str(now.hour) + "30"
        else:
            base_time = str(now.hour) + "30"
        base_date = today
    print(f'now.hour: {now.hour}')
    print(f'base_date: {base_date}/ base_time:{base_time}')


    #desired_time을 구하는 함수
    #초단기예보가 제공하는 6개의 시간대중 현재시간과 가장 가까운 시간
    if now.hour == 23:
        if now.minute < 30:
            desired_time = str(now.hour) + "00"
        else:
            desired_time = "0000"

    else:
        if now.minute < 30:
            desired_time = str(now.hour) + "00"
        else:
            desired_time = str(now.hour + 1) + "00"
    if len(desired_time) < 4: 
        desired_time = "0" + desired_time
    # print(f'desired_time: {desired_time}')

    #오늘의 날씨 
    queryParams = '?' + urlencode(
        { quote_plus('serviceKey') : serviceKeyDecoded, quote_plus('base_date') : base_date, quote_plus('base_time') : base_time, 
                quote_plus('nx') : nx, quote_plus('ny') : ny, quote_plus('dataType') : 'json', quote_plus('numOfRows') : '60'}) #페이지로 안나누고 한번에 받아오기 위해 numOfRows=60으로 설정해주었다
    # 값 요청 (웹 브라우저 서버에서 요청 - url주소와 파라미터)
    #print(url + queryParams)
    res = requests.get(url + queryParams, verify=False) # verify=False이거 안 넣으면 에러남ㅜㅜ
    items = res.json().get('response').get('body').get('items') #데이터들 아이템에 json 형태로 저장
    #print(items)# 테스트



    weather_data = dict() 

    #오늘의 날씨 dict저장
    for item in items['item']:
        if item['fcstTime'] == desired_time:
                # 기온
                if item['category'] == 'T1H':
                    weather_data['tmp'] = item['fcstValue']
                # 습도
                if item['category'] == 'REH':
                    weather_data['hum'] = item['fcstValue']
                # 하늘상태: 맑음(1) 구름많음(3) 흐림(4)
                if item['category'] == 'SKY':
                    weather_data['sky'] = item['fcstValue']
                # 강수형태: 없음(0) 비(1) 비/눈(2) 눈(3) 빗방울(4) 빗방울/눈날림(5) 눈날림(6)
                if item['category'] == "PTY":
                    weather_data['pty'] = item['fcstValue']
                # 1시간 동안 강수량
                if item['category'] == 'RN1':
                    weather_data['rain'] = item['fcstValue']
                #풍속
                if item['category'] == "WSD":
                    weather_data['w_speed'] = item['fcstValue'] 

    #동파가능지수 계산
    weather_data['cold'] = ''
    deg = weather_data['tmp']
    if int(deg) >= -5:
        weather_data['cold'] = '낮음'
    elif -10 <= int(deg) < -5:
        weather_data['cold'] = '보통'
    elif -15 <= int(deg) < -10:
        weather_data['cold'] = '높음'
    else:
        weather_data['cold'] = '매우높음'


    #자외선지수
    def sun_func():
        #현재시간 가져오기
        now = datetime.now()
        today = datetime.today().strftime("%Y%m%d")
        h, m = now.hour, now.minute
        if h<10:
            time = today + '0' + str(h)
        else:
            time = today + str(h)
        #자외선지수 api 주소
        url = 'https://apis.data.go.kr/1360000/LivingWthrIdxServiceV3/getUVIdxV3'

        areaNo = '1100000000'   #서울지점('1100000000'), 만약 공백일때 전체지점 조회

        #파라미터 설정_오늘
        queryParams = '?' + urlencode({
        quote_plus("serviceKey"): serviceKeyDecoded,                                            
        quote_plus("areaNo"): areaNo,    
        quote_plus("time"): time,  
        quote_plus("dataType"): "JSON",                       
        })
        #오늘 값 요청 (웹 블우저 서버에서 요청 - url주소와 파라미터)
        res = requests.get(url + queryParams, verify=False) # verify=False이거 안 넣으면 에러남ㅜㅜ
        items = res.json().get('response').get('body').get('items') #데이터들 아이템에 json 형태로 저장

        sun = ''
        for item in items['item']:
            if h==0 or h%3==0:
                s = item['h0']
            elif h%2 ==0:
                s = item['h3']
            else:
                s = item['h0']
        s = int(s)
        if s >= 11: sun = '위험'
        elif 8 <= s <=10: sun = '매우높음'
        elif 6 <= s <= 7: sun = '높음'
        elif 3 <= s <=5: sun = '보통'
        else: sun = '낮음'

        return sun

    sun = sun_func()
    weather_data['sun'] = sun

    #어제의 날씨
    yy = datetime.strptime(base_date, "%Y%m%d").date()  #strptime함수로 문자열을 datetime으로 변환
    t = yy - timedelta(days=1)
    base_date_yy = t.strftime("%Y%m%d")     #base_date_yy을 base_time 하루전으로 설정

    #api 호출
    queryParams = '?' + urlencode(
        { quote_plus('serviceKey') : serviceKeyDecoded, quote_plus('base_date') : base_date_yy, quote_plus('base_time') : base_time, #base_date_yy을 넣음
                quote_plus('nx') : nx, quote_plus('ny') : ny, quote_plus('dataType') : 'json', quote_plus('numOfRows') : '60'}) #페이지로 안나누고 한번에 받아오기 위해 numOfRows=60으로 설정해주었다
    # 값 요청 (웹 브라우저 서버에서 요청 - url주소와 파라미터)
    #print(url + queryParams)
    res = requests.get(url + queryParams, verify=False) # verify=False이거 안 넣으면 에러남ㅜㅜ
    items = res.json().get('response').get('body').get('items') #데이터들 아이템에 json 형태로 저장

     #어제의 기온을 yy_tmp(int)저장
    yy_tmp = int
    for item in items['item']:
        if item['fcstTime'] == desired_time:
                # 기온
                if item['category'] == 'T1H':
                    yy_tmp = item['fcstValue']

    y_tmp, t_tmp = int(yy_tmp), int(weather_data['tmp']) #어제, 오늘 기온
    if t_tmp >= y_tmp:
        w = f'기온이 어제보다 {t_tmp-y_tmp}° 높아요'
    else:
        w = f'기온이 어제보다 {y_tmp-t_tmp}° 낮아요'

    return weather_data, w, 

def seven_days():
    #현재시간 가져오기
    now = datetime.now()
    today = datetime.today().strftime("%Y%m%d")
    y = date.today() - timedelta(days=1)
    yesterday = y.strftime("%Y%m%d")

    #발표시각(tmFc) 설정
    if now.hour < 6:
        tmFc = yesterday + '1800'
    elif 6 <= now.hour <18:
        tmFc = today + '0600'
    else:
        tmFc = today + '1800'
    
    #예보구역코드
    regId = '11B00000'

    #중기육상예보조회 api 호출 
    url = 'http://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst'

    serviceKey = 'K7Y1L9rDTVLkFGhZPl2QeAvG9KUmWK2qQmclmrNffL%2FUQYQipP1%2BCi6HFeFV1kSN6Gi2KJ49tuimf35PFy579A%3D%3D'
    serviceKeyDecoded = unquote(serviceKey, 'UTF-8') # 공공데이터 포털에서 제공하는 서비스키는 이미 인코딩된 상태이므로, 디코딩하여 사용해야 함

    #파라미터 설정_오늘
    queryParams = '?' + urlencode({
    quote_plus("serviceKey"): serviceKeyDecoded,     
    quote_plus("numOfRows"): "10", #1시간당 받아올 수 있는 날씨정보는 12개, 하루동안 받아올수 있느 날씨 정보는 288개 + 2개(TMN, TMX(최고기온, 최저기온))          
    quote_plus("pageNo"): "1",              
    quote_plus("dataType"): "JSON",         
    quote_plus("regId"): regId,    
    quote_plus("tmFc"): tmFc,                        
    })

    #오늘 값 요청 (웹 블우저 서버에서 요청 - url주소와 파라미터)
    res = requests.get(url + queryParams, verify=False) # verify=False이거 안 넣으면 에러남ㅜㅜ
    items = res.json().get('response').get('body').get('items') #데이터들 아이템에 json 형태로 저장

    week_data = {}  #1주일 +2일의 날씨정보를 저장
    for i in range(3, 11):
        week_data[i] = {}

    #데이터를 딕셔너리 형태로 저장
    for item in items['item']:
        
        # 3일후 오전 날씨예보
        week_data[3]['skyAm'] = item['wf3Am']
        # 3일후 오후 날씨예보
        week_data[3]['skyPm'] = item['wf3Pm']
        # 4일후 오전 날씨예보
        week_data[4]['skyAm'] = item['wf4Am']
        # 4일후 오후 날씨예보
        week_data[4]['skyPm'] = item['wf4Pm']
        # 5일후 오전 날씨예보
        week_data[5]['skyAm'] = item['wf5Am']
        # 5일후 오후 날씨예보
        week_data[5]['skyPm'] = item['wf5Pm']
        # 6일후 오전 날씨예보
        week_data[6]['skyAm'] = item['wf6Am']
        # 6일후 오후 날씨예보
        week_data[6]['skyPm'] = item['wf6Pm']
        # 7일후 오전 날씨예보
        week_data[7]['skyAm'] = item['wf7Am']
        # 7일후 오후 날씨예보
        week_data[7]['skyPm'] = item['wf7Pm']
        # 8일후 오전 날씨예보
        week_data[8]['skyAm'] = item['wf8']
        # 8일후 오후 날씨예보
        week_data[8]['skyPm'] = item['wf8']
        # 9일 후 오전 날씨예보
        week_data[9]['skyAm'] = item['wf9']
        # 9일후 오후 날씨예보
        week_data[9]['skyPm'] = item['wf9']
        # 10일 후 오전 날씨예보
        week_data[10]['skyAm'] = item['wf10']
        # 10일후 오후 날씨예보
        week_data[10]['skyPm'] = item['wf10']

        #3~7일 오전, 오후의 비올 확률
        week_data[3]['rainAm'] = item['rnSt3Am']
        week_data[3]['rainPm'] = item['rnSt3Pm']
        week_data[4]['rainAm'] = item['rnSt4Am']
        week_data[4]['rainPm'] = item['rnSt4Pm']
        week_data[5]['rainAm'] = item['rnSt5Am']
        week_data[5]['rainPm'] = item['rnSt5Pm']
        week_data[6]['rainAm'] = item['rnSt6Am']
        week_data[6]['rainPm'] = item['rnSt6Pm']
        week_data[7]['rainAm'] = item['rnSt7Am']
        week_data[7]['rainPm'] = item['rnSt7Pm']
        week_data[8]['rainAm'] = item['rnSt8']
        week_data[8]['rainPm'] = item['rnSt8']
        week_data[9]['rainAm'] = item['rnSt9']
        week_data[9]['rainPm'] = item['rnSt9']
        week_data[10]['rainAm'] = item['rnSt10']
        week_data[10]['rainPm'] = item['rnSt10']

 
    #중기기온예보 api
    url2 = 'http://apis.data.go.kr/1360000/MidFcstInfoService/getMidTa'

    regId = '11B10101'

    #파라미터 설정_오늘
    queryParams = '?' + urlencode({
    quote_plus("serviceKey"): serviceKeyDecoded,     
    quote_plus("numOfRows"): "10", #1시간당 받아올 수 있는 날씨정보는 12개, 하루동안 받아올수 있느 날씨 정보는 288개 + 2개(TMN, TMX(최고기온, 최저기온))          
    quote_plus("pageNo"): "1",              
    quote_plus("dataType"): "JSON",         
    quote_plus("regId"): regId,    
    quote_plus("tmFc"): tmFc,                        
    })
    # print(url2 + queryParams)
    #오늘 값 요청 (웹 블우저 서버에서 요청 - url주소와 파라미터)
    res = requests.get(url2 + queryParams, verify=False) # verify=False이거 안 넣으면 에러남ㅜㅜ
    items = res.json().get('response').get('body').get('items') #데이터들 아이템에 json 형태로 저장

    #데이터를 딕셔너리 형태로 저장
    for item in items['item']:
        # 3일후 오전 날씨예보
        week_data[3]['min'] = item['taMin3']
        # 3일후 오후 날씨예보
        week_data[3]['max'] = item['taMax3']
        # 4일후 오전 날씨예보
        week_data[4]['min'] = item['taMin4']
        # 4일후 오후 날씨예보
        week_data[4]['max'] = item['taMax4']
        # 5일후 오전 날씨예보
        week_data[5]['min'] = item['taMin5']
        # 5일후 오후 날씨예보
        week_data[5]['max'] = item['taMax5']
        # 6일후 오전 날씨예보
        week_data[6]['min'] = item['taMin6']
        # 6일후 오후 날씨예보
        week_data[6]['max'] = item['taMax6']
        # 7일후 오전 날씨예보
        week_data[7]['min'] = item['taMin7']
        # 7일후 오후 날씨예보
        week_data[7]['max'] = item['taMax7']
        # 8일후 최저기온
        week_data[8]['min'] = item['taMin8']
        # 8일후 최고기온
        week_data[8]['max'] = item['taMax8']
        # 9일후 최저기온
        week_data[9]['min'] = item['taMin9']
        # 9일후 최고기온
        week_data[9]['max'] = item['taMax9']
        # 10일후 최저기온
        week_data[10]['min'] = item['taMin10']
        # 10일후 최고기온
        week_data[10]['max'] = item['taMax10']

    return week_data


def weather():

    #위치좌표를 가져와 위경도 설정
    lat, lng = get_curr_loc()

    #위치좌표 -> nx, ny로 변경
    #nx, ny란? 기상청 api가 위, 경도 좌표 대신 요구하는 x, y 좌표
    nx, ny = map_to_xy(lat, lng)

    #현재의 날씨 데이터 얻어오기(getUltraSrtFcst), word(어제와 오늘의 기온비교), sun(자외선지수)
    curr_weather, word = getUltraSrtFcst(nx, ny)
    curr_weather['loc'] = reverse_geocoding(lat, lng)
    #print(curr_weather)
    
    #현재 시간(h) 얻어오기
    now = datetime.now()
    str_time=now.strftime("%H")
    time = int(str_time)

    #3일치의 날씨 데이터 얻어오기(getVilageFsct)
    day1, day2, day3, tmn, tmx, week, word2 = getVilageFsct(nx, ny)
    #+3~+9일치의 날씨 데이터 얻어오기(중기예보api)
    week = seven_days()
    # week.update(week_plus)

    #week 딕셔너리의 키값을 날짜로 변경
    days = ['월', '화', '수', '목', '금', '토', '일']
    today = datetime.today().strftime("%m/%d") 
    for i in range(3,11):
        n = date.today() + timedelta(days=i)
        day = n.weekday()   #요일
        nextday = n.strftime("%m/%d")
        week[nextday] = week.pop(i)
        week[nextday]['day'] = days[day]    #요일을 week딕셔너리에 저장

    # print(week)
  
        
    #return render(request, "pybo/weather_index.html", {'curr_weather': curr_weather, 'time': time, 'day1': day1, 'day2' : day2, 'day3': day3, 'tmn': tmn, 'tmx': tmx, 'week': week, 'word': word, 'word2': word2})
weather()