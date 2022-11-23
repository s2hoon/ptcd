#주소 입력하면 좌표나오는 함수
#geocoding
import googlemaps

#위치(위, 경도) 가져오는 함수
GOOGLE_API_KEY = 'AIzaSyAOgov4B8S6uESOZ9J-wnav-6_6bcJSyUI'
gmaps = googlemaps.Client(GOOGLE_API_KEY)

def address_convert(loc):
        try:
                geocode_result = gmaps.geocode((loc), language='ko') # 한국어 설정으로 입력한 위치의 결과값을 받아온다.
                #print(geocode_result)

                latitude  = geocode_result[0]["geometry"]["location"]["lat"] # 리스트에서 위도 추출
                longitude = geocode_result[0]["geometry"]["location"]["lng"] # 리스트에서 경도 추출

                #print(latitude,longitude)
                #역지오코딩
                ## reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude), language='ko')
                # return(reverse_geocode_result[4]['formatted_address'])
        except:
                latitude, longitude = 0, 0
                #print("오류있습니다")
        if latitude == 0 or longitude == 0:
                #print("오류있습니다")
                return latitude, longitude
        else:
                reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude), language='ko')
                #print(reverse_geocode_result[4]['formatted_address'])
                return latitude, longitude


def addressing(latitude, longitude):
        reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude), language='ko')
        #print(reverse_geocode_result[4]['formatted_address'])
        return reverse_geocode_result[4]['formatted_address']


