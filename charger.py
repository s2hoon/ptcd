#전기차 충전소나오는 api
from urllib.parse import urlencode, unquote
import requests
import json
import pandas as pd # pandas 모듈 로드
from place import address_convert
from whereami import getlocation
from coding import locationcode
from place import addressing

#loc1,loc2= getlocation()
#address = addressing(loc1, loc2)
#address= address.split()
#print(address[1],address[2])
#metroCd,cityCd = locationcode(address[1],address[2])


def charger(code1, code2):
  coordinate = []
  cartype = []
  stnplace = []
  rapidcnt = []
  slowcnt = []

  #공통코드 입력
  #metroCd,cityCd = input().split()
  
  #전기차 충전소 api
  url = "https://bigdata.kepco.co.kr/openapi/v1/EVcharge.do"
  queryString = "?" + urlencode(
  {
    "apiKey": unquote("1C2V9O676tBEB9359s1j8j6X420q0zJ0i5kT064F"),
    "metroCd": code1,
    "cityCd": code2,
    "returnType": "json"
  }
  )
  queryURL = url + queryString
  #데이터 요청(json)
  response = requests.get(queryURL)
  #json 으로 읽기
  info = json.loads(response.text)
  
  
  # geocoding 함수 적용
  for arr in info['data']:
    coordinate.append(address_convert(arr['stnAddr']))
    cartype.append( arr['carType'] )#차종류
    stnplace.append(  arr['stnPlace']) #건물명
    rapidcnt.append(  arr['rapidCnt'] )#급속충전기 대수
    slowcnt.append(arr['slowCnt']) #완속 충전기 대수

  return coordinate, cartype , stnplace, rapidcnt, slowcnt
    #print(address, stnplace ,cartype, rapidcnt, slowcnt, end = " ")
    #print()