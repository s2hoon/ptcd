# 220822 Python 누진세 한전 API 연동

import requests

API_KEY = '0MqfFehrjt3fi5010MtsOpHItHZWVAGpJ3i5Tgj3'
codeData = requests.get(
    'https://bigdata.kepco.co.kr/openapi/v1/commonCode.do?codeTy=cityCd&apiKey=0MqfFehrjt3fi5010MtsOpHItHZWVAGpJ3i5Tgj3&returnType=json').json()


def apiRequest(search_year, search_month, search_city, search_gu):
    #search_year = input("\n>> 검색대상 연도를 입력하세요 (ex : 2022)  : ")
    #search_month = input(">> 검색대상 월을 입력하세요 (ex : 02)  : ")

    #while True:
        #search_city = input(">> 검색대상 도시를 입력하세요 (ex : 대구광역시)  : ")
        #search_gu = input(">> 검색대상 시군구를 입력하세요 (ex : 수성구)  : ")
    searchCityCode = 0
    searchCode = 0
    for code in codeData.get("data"):
        if search_city.strip() == code.get("uppoCdNm") and search_gu.strip() == code.get("codeNm"):
            searchCode = code.get("code")
            searchCityCode = code.get("uppoCd")
            print('검색코드 API 응답값 : ', searchCityCode, searchCode)
    if searchCode == 0:
        print("시도 시군구 입력 오류입니다. 재시도하세요")
  
    targetUrl = 'https://bigdata.kepco.co.kr/openapi/v1/powerUsage/houseAve.do?year=' + search_year + '&month=' + search_month + '&metroCd=' + searchCityCode + '&cityCd=' + searchCode + '&apiKey=' + API_KEY + '&returnType=json'

    requestData = requests.get(targetUrl)
    jsonData = None
    if requestData.status_code == 200:
        print(":: API 통신상태 정상 ::")
        jsonData = requestData.json()
        results = checkLevel(jsonData.get("data")[0].get("powerUsage"), search_month)
        print('\n::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        print(' ', search_year + '년 ' + search_month + '월 ', end='')
        print(jsonData.get("data")[0].get("metro"), end=' ')
        print(jsonData.get("data")[0].get("city"), end=' 의 평균 전력 사용량 : ')
        print(jsonData.get("data")[0].get("powerUsage"))

        if results[1] == False:
            print("  누진세 계산 결과 : 기타계절", results[0], '단계 ')
        else:
            print("  누진세 계산 결과 : 하계", results[0], '단계 ')
        print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n')
        return(jsonData.get("data")[0].get("powerUsage"), results[1], results[0])

    else:
        print(":: API 응답 오류, 재시도하세요 ::")




def checkLevel(usage, month):
    result = 0
    isSummer = False
    month_ = int(month)
    if month_ == 7 or month_ == 8:
        isSummer = True
        print("하계 요금을 적용합니다.")
        if usage <= 300:
            result = 1
        elif 300 < usage <= 450:
            result = 2
        elif usage > 450:
            result = 3

    else:
        print("기타계절 요금을 적용합니다.")
        if usage <= 200:
            result = 1
        elif 200 < usage <= 400:
            result = 2
        elif usage > 400:
            result = 3

    return result, isSummer


'''
while True:
    apiRequest()
'''