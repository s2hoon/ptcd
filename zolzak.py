import requests
from urllib.parse import urlencode, unquote, quote_plus
from datetime import date, timedelta, datetime

# 기상청_동네 예보 조회 서비스 api 데이터 url 주소, 초단기이기때문에 getUltraSrtFcst 사용
url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"

serviceKey = "K7Y1L9rDTVLkFGhZPl2QeAvG9KUmWK2qQmclmrNffL/UQYQipP1+Ci6HFeFV1kSN6Gi2KJ49tuimf35PFy579A==" # 공공데이터 포털에서 생성된 본인의 서비스 키를 복사 / 붙여넣기
serviceKeyDecoded = unquote(serviceKey, 'UTF-8') # 공데이터 포털에서 제공하는 서비스키는 이미 인코딩된 상태이므로, 디코딩하여 사용해야 함

now = datetime.now()
today = datetime.today().strftime("%Y%m%d")
y = date.today() - timedelta(days=1)
yesterday = y.strftime("%Y%m%d")
#print(today)
#print(yesterday)

# 위도와 경도를 x,y좌표로 변경
nx = 61 
ny = 129
    
if now.minute<45: # base_time와 base_date 구하는 함수
    if now.hour==0:
        base_time = "2330"
        base_date = yesterday
    else:
        pre_hour = now.hour-1
        if pre_hour<10:
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


queryParams = '?' + urlencode({ quote_plus('serviceKey') : serviceKeyDecoded, quote_plus('base_date') : base_date, quote_plus('base_time') : base_time, quote_plus('nx') : nx, quote_plus('ny') : ny, quote_plus('dataType') : 'json', quote_plus('numOfRows') : '60'}) #페이지로 안나누고 한번에 받아오기 위해 numOfRows=60으로 설정해주었다
                                   
# 값 요청 (웹 브라우저 서버에서 요청 - url주소와 파라미터)
res = requests.get(url + queryParams, verify=False) # verify=False이거 안 넣으면 에러남ㅜㅜ
items = res.json().get('response').get('body').get('items') #데이터들 아이템에 저장
#print(items)# 테스트

weather_data = dict()

for item in items['item']:
    # 기온
    if item['category'] == 'T1H':
        weather_data['tmp'] = item['fcstValue'] + " °C"
    # 습도
    if item['category'] == 'REH':
        weather_data['hum'] = item['fcstValue'] + " %"
    # 하늘상태: 맑음(1) 구름많음(3) 흐림(4)
    if item['category'] == 'SKY':
        if item['fcstValue'] == '1':
            weather_data['sky'] = '맑음'
        elif item['fcstValue'] == '3':
            weather_data['sky'] = '구름많음'
        elif item['fcstValue'] == '4':
            weather_data['sky'] = '흐림'
        #weather_data['sky'] = item['fcstValue']
    # 1시간 동안 강수량
    if item['category'] == 'RN1':
        weather_data['rain'] = item['fcstValue']

print("response: ", weather_data)