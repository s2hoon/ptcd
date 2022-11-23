from re import L
from django.shortcuts import render , get_object_or_404,redirect, redirect
from django.http import HttpResponse
from django.utils import timezone
from whereami import getlocation
from django.contrib.auth.models import User
from django.contrib import auth
from place import addressing
from coding import locationcode
from charger import charger
from hs1 import checkNujin1
from hs2 import apiRequest
import json
# Create your views here.
def index(request):
    return render(request, 'pybo/index.html')

def kakaomap(request):
    if request.method == 'POST':
        
        #전기차 충전소 정보 받기
        address1 = request.POST['drop1']
        address2 = request.POST['drop2']
        code1,code2= locationcode(address1,address2)

        coordinate, cartype, stnplace, rapidcnt, slowcnt = charger(code1,code2)
        charger_information = {
            'coordinate' :coordinate,
            'cartype' :cartype,
            'stnplace' :stnplace,
            'rapidcnt' : rapidcnt,
            'slowcnt' :slowcnt,
        }
        charger_information = json.dumps(charger_information)



        #내위치 좌표 얻고 한글로 바꿔주기
        address = getlocation()
        latitude = address[0]
        longitude = address[1]
        address = addressing(latitude, longitude)


       #전기차 충전소 좌표랑 내위치(한글) 데이터 보내주기
        return render(request, 'pybo/kakaomap.html',{'charger_information':charger_information,'address':address})

    
    
    else:
        #내위치 좌표 얻고 한글로 바꿔주기
        address = getlocation()
        latitude = address[0]
        longitude = address[1]
        address = addressing(latitude, longitude)
        

        #내위치 좌표랑 내위치(한글) 데이터 보내주기
        return render(request, 'pybo/kakaomap.html',{'lat':latitude,'long' : longitude,'address':address})





def hs(request):
    if request.method == 'GET':
        #누진세 예측 기능
        data = request.GET.get('powerusage')
        if(data == None):
            return render(request, 'pybo/hs.html')
        else:
            data = int(data)
            summer_cost=checkNujin1(data,450,300)
            other_cost=checkNujin1(data,400,200)
            return render(request, 'pybo/hs.html',{'summer_cost':summer_cost, 'other_cost':other_cost})   

        
    return render(request, 'pybo/hs.html')


def hs2(request):
    if request.method == 'GET':
        #평균 전력량 예측
        search_year = request.GET.get('year')
        search_month = request.GET.get('month')
        search_city = request.GET.get('city')
        search_gu = request.GET.get('gu')
        powerusage, season ,level =apiRequest(search_year, search_month,search_city, search_gu)
        if season == False:
            season ='기타 계절'
        else :
            season ='하계'



        return render(request, 'pybo/hs.html',{'powerusage':powerusage,'season': season ,'level':level})


def sj(request):
    return render(request, 'pybo/profile.html')

def sj2(request):
    return render(request, 'pybo/main.html')

def pj(request):
    return render(request, 'pybo/profitability.html')