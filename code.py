from urllib.parse import urlencode, unquote
import requests
import json
import pandas as pd # pandas 모듈 로드


#시도 - metroCd, 시군구 - cityCd, 계약종별 - cntrCd
#산업분류 - bizCd, 발전원 - genSrcCd, 복지할인 - wfTypeCd
code = input()


#공통코드 api
url = "https://bigdata.kepco.co.kr/openapi/v1/commonCode.do"
queryString = "?" + urlencode(
{
  "apiKey": unquote("1C2V9O676tBEB9359s1j8j6X420q0zJ0i5kT064F"),
    "codeTy": code,
    "returnType": "json"
}
)
queryURL = url + queryString
#데이터 요청(json)
response = requests.get(queryURL)

#pandas 데이터프레임
info = json.loads(response.text)
df = pd.json_normalize(info['data'])
df.to_csv("공통코드.csv", index=False, encoding="utf-8-sig")



print(df)

