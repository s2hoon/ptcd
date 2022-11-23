
from urllib.parse import urlencode, unquote
import requests
import json

#시도 - metroCd, 시군구 - cityCd, 계약종별 - cntrCd
#산업분류 - bizCd, 발전원 - genSrcCd, 복지할인 - wfTypeCd


#string으로 시도 시군구 넣어주면 코드 번호가 나오는 함수
def locationcode(loc,loc2):
    resultcode1 = 0
    resultcode2 = 0

    #공통코드 api
    #loc 첫번쨰 코드 metroCd
    url = "https://bigdata.kepco.co.kr/openapi/v1/commonCode.do"
    queryString = "?" + urlencode(
    {
    "apiKey": unquote("1C2V9O676tBEB9359s1j8j6X420q0zJ0i5kT064F"),
    "codeTy": "metroCd",
    "returnType": "json"
    }
    )
    queryURL = url + queryString
    #데이터 요청(json)
    response = requests.get(queryURL)
    jsonobject = json.loads(response.text)

    for elem in jsonobject['data']:
        if elem['codeNm']==loc:
            resultcode1 = elem['code']
            #print(elem['code'])

    #loc2 두번쨰 코드 cityCd
    queryString = "?" + urlencode(
    {
    "apiKey": unquote("1C2V9O676tBEB9359s1j8j6X420q0zJ0i5kT064F"),
    "codeTy": "cityCd",
    "returnType": "json"
    }
    )
    queryURL = url + queryString
    #데이터 요청(json)
    response = requests.get(queryURL)
    jsonobject2 = json.loads(response.text)

    for elem in jsonobject2['data']:
        if elem['codeNm']==loc2:
            resultcode2 = elem['code']
            #print(elem['code'])
    

    return resultcode1, resultcode2

#loc,loc2 = input().split()
#locationcode(loc,loc2)
