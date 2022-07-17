
from urllib.parse import urlencode, unquote
import requests
import json
import pandas as pd # pandas 모듈 로드


#공통코드 입력
metroCd,cityCd = input().split()



#전기차 충전소 api
url = "https://bigdata.kepco.co.kr/openapi/v1/EVcharge.do"
queryString = "?" + urlencode(
{
  "apiKey": unquote("1C2V9O676tBEB9359s1j8j6X420q0zJ0i5kT064F"),
  "metroCd": metroCd,
  "cityCd": cityCd,
  "returnType": "json"
}
)
queryURL = url + queryString
#데이터 요청(json)
response = requests.get(queryURL)

#pandas 데이터프레임
info = json.loads(response.text)
df = pd.json_normalize(info['data'])
df.to_csv("전기차 충전소.csv", index=False, encoding="utf-8-sig")



print(df)

