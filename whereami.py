#geolocation api로 현재 위치 가져오기
import os
import requests
#from dotenv import load_dotenv
import json
from urllib.parse import urlencode, unquote, quote_plus
import math
#geocoding
import googlemaps
from numpy import result_type

def getlocation():
    #위치(위, 경도) 가져오는 함수
    GOOGLE_API_KEY = 'AIzaSyAOgov4B8S6uESOZ9J-wnav-6_6bcJSyUI'
    gmaps = googlemaps.Client(GOOGLE_API_KEY)

    #현재위치(위, 경도) 가져오는 함수
    #load_dotenv(verbose=True)
    LOCATION_API_KEY = "AIzaSyAOgov4B8S6uESOZ9J-wnav-6_6bcJSyUI" # 공공데이터 포털에서 생성된 본인의 서비스 키를 복사 / 붙여넣기
    #LOCATION_API_KEY = unquote(LOCATION_API_KEY, 'UTF-8') # 공공데이터 포털에서 제공하는 서비스키는 이미 인코딩된 상태이므로, 디코딩하여 사용해야 함
    #LOCATION_API_KEY = os.getenv('AIzaSyBl2aDuQAzEzwFginc7ry8UDhOLiK40HH0')    #에러가 왜나는지 모르겠음ㅠㅠ
    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={LOCATION_API_KEY}'
    data = {
        'considerIp': True,
    }
    result = requests.post(url, data)
    #print(result.text)
    #json파일을 딕셔너리로 변환
    loc_dict = result.json()
    #print(loc_dict)
    latitude = loc_dict['location']['lat']
    longitude = loc_dict['location']['lng']
    return latitude, longitude

#역지오코딩을 활용하여 주소를 문자열로 변환
#reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude), language='ko')
#print(reverse_geocode_result[4]['formatted_address'])


#print(getlocation())