# *-- Geocoding 활용 코드 --*
import json
import urllib
from urllib.request import Request, urlopen
# *-- 3개의 주소 geocoding으로 변환한다.(출발지, 도착지, 경유지) --*
start = '서울특별시 중랑구 용마산로36길 21-9'
goal = '서울특별시 송파구 오금로 20'
waypoint = '서울특별시 노원구 석계로 98-2'
waypoint2 = '서울특별시 노원구 석계로 98-2'
#서울특별시 노원구 석계로 98-2
# 주소에 geocoding 적용하는 함수를 작성.
def get_location(loc) :
    client_id = 'pobhohx7jy'
    client_secret = '6vAVhJck5q6iJ6WOQYrpsgEU53MjEp38OJ190Tip'
    url = f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=" \
    			+ urllib.parse.quote(loc)
    
    # 주소 변환
    request = urllib.request.Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
    request.add_header('X-NCP-APIGW-API-KEY', client_secret)
    
    response = urlopen(request)
    res = response.getcode()
    
    if (res == 200) : # 응답이 정상적으로 완료되면 200을 return한다
        response_body = response.read().decode('utf-8')
        response_body = json.loads(response_body)
        print(response_body)
        # 주소가 존재할 경우 total count == 1이 반환됨.
        if response_body['meta']['totalCount'] == 1 : 
        	# 위도, 경도 좌표를 받아와서 return해 줌.
            lat = response_body['addresses'][0]['y']
            lon = response_body['addresses'][0]['x']
            return (lon, lat)
        else :
            print('location not exist')
        
    else :
        print('ERROR')
        
#  함수 적용
start = get_location(start)
goal = get_location(goal)
waypoint = get_location(waypoint)
waypoint2 = get_location(waypoint2)
# *-- Directions 5 활용 코드 --*
option = ''
# option : 탐색옵션 [최대 3개, traoptimal(기본 옵션) 
# / trafast, tracomfort, traavoidtoll, traavoidcaronly]

def get_optimal_route(start, goal, waypoints=['',''], option=option ) :
    client_id = 'pobhohx7jy'
    client_secret = '6vAVhJck5q6iJ6WOQYrpsgEU53MjEp38OJ190Tip'
    # start=/goal=/(waypoint=)/(option=) 순으로 request parameter 지정
    url = f"https://naveropenapi.apigw.ntruss.com/map-direction-15/v1/driving?start={start[0]},{start[1]}&goal={goal[0]},{goal[1]}&waypoint={waypoint[0]},{waypoint[1]}|{waypoint2[0]},{waypoint2[1]}&option={option}"
    request = urllib.request.Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
    request.add_header('X-NCP-APIGW-API-KEY', client_secret)
    
    response = urllib.request.urlopen(request)
    res = response.getcode()
    
    if (res == 200) :
        response_body = response.read().decode('utf-8')
        return json.loads(response_body)
            
    else :
        print('ERROR')
        
results= get_optimal_route(start, goal, waypoint, option=option)

# *-- 목적지까지의 종합 정보 추출(총 거리, 총 소요시간, 요금 등) --*
message = {
    'message' : results['message'], # traoptimal은 option 에 따라 다르게 줄 것
    'option' : list(results['route'].keys())[0],
    'total_distance' : results['route']['traoptimal'][0]['summary']['distance'],
    'total_duration' : results['route']['traoptimal'][0]['summary']['duration'],
    'fares' : {'toll' : results['route']['traoptimal'][0]['summary']['tollFare'],
              'taxi' : results['route']['traoptimal'][0]['summary']['taxiFare'],
              'fuel' : results['route']['traoptimal'][0]['summary']['fuelPrice']}
}

#print(message['total_distance'])

# *-- 목적지까지의 guidence와 각각의 거리, 소요시간 정보 추출 --*




temp = [ (guide['instructions'], guide['distance'] , guide['duration'] / 1000 ) for guide in results['route']['traoptimal'][0]['guide'] ]




