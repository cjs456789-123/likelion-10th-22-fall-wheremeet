import json
from django.shortcuts import render
from .models import Meetingplace
from operator import itemgetter

import numpy 
from numpy import sin, cos, arccos, pi, round
import time
from urllib.request import urlopen
from datetime import datetime

from django.db.models import Q
from WMapp.models import Meetingplace
from .data.csv_to_db_run import csv_to_db

from .special_key import geolocation_key, kakaoapi_key

# Create your views here.

kakaokey = kakaoapi_key


### 운영중/운영종료 표시
def open_close_time(time1):
    now = datetime.now()

    time1 = time1.split(' ')

    time = time1[now.weekday()] # 현재요일과 같은 요일 데이터만 추출
    weekday = time[0]           # 월화수목금토일
    hourMin = time[1:]          # 00:00~24:00 / 운영종료

    if ((hourMin == "운영종료") | (hourMin == "영업종료")):     # "운영종료"와 "영업종료"가 혼합된 DB
        return "운영종료"
    
    else:
        hourMin = time[1:].split('~')
        open_hour = hourMin[0][:2]
        open_min  = hourMin[0][3:]
        close_hour = hourMin[1][:2]
        close_min  = hourMin[1][3:]

        now = now.strftime('%Y-%m-%d %H:%M:%S') # 타입변환

        current_hour = now[11:13]
        current_min  = now[14:16]

        if (current_hour > open_hour and current_hour < close_hour): 
            return '운영중'
        elif (current_hour == open_hour):
            if current_min >= open_min: 
                return '운영중'
            else: 
                return '운영종료'
        elif (current_hour == close_hour):
            if current_min <= close_min: 
                return '운영중'
            else: 
                return '운영종료'   
        else: 
            return '운영종료'


### 거리 계산
def rad2deg(radians):
    degrees = radians * 180 / pi
    return degrees

def deg2rad(degrees):
    radians = degrees * pi / 180
    return radians

def getDistanceBetweenPointsNew(latitude1, longitude1, latitude2, longitude2, unit = 'meters'):
    
    theta = longitude1 - longitude2
    
    distance = 60 * 1.1515 * rad2deg(
        arccos(
            (sin(deg2rad(latitude1)) * sin(deg2rad(latitude2))) + 
            (cos(deg2rad(latitude1)) * cos(deg2rad(latitude2)) * cos(deg2rad(theta)))
        )
    )
    
    if unit == 'miles':
        return round(distance, 0)
    if unit == 'meters':
        return round(distance * 1.609344 * 1000, 0)

### 실시간 현재위치 렌더링 -> 다소 부정확...
def currentPosition():
    key = geolocation_key

    url = f'https://ipgeolocation.abstractapi.com/v1/?api_key={key}'

    response = urlopen(url)
    # time.sleep(0.1)
    response_bytes = response.read()
    # print(type(response_bytes))
    # print(response.getheader('Content-Type'))
    response_json = response_bytes.decode()
    # print(response_json)
    # print(type(response_json))   # string

    ### str -> json 타입 변환
    data = json.loads(response_json)

    # 현재위치 위도,경도
    myLat = data['latitude']
    myLng = data['longitude']
    
    return myLat, myLng     # --> map.js로 보내기 or map.html로 보내기


## 미팅룸 정보(+distance)
meetingplaces = Meetingplace.objects.all()
if not meetingplaces:
    csv_to_db(Meetingplace)
    meetingplaces = Meetingplace.objects.all()
    
if len(meetingplaces) > 80:
    meetingplaces = meetingplaces[:71]    
    
# myLat, myLng = currentPosition()      # 현재위치
myLat, myLng = 37.5884768, 126.9919398  # 호암관

meetingplace_information = [
{
    "id"           : meetingplace.id,
    "name"         : meetingplace.name,
    "address"      : meetingplace.address,
    "lat"          : meetingplace.lat,
    "lon"          : meetingplace.lon,
    "location"     : meetingplace.location,
    "people"       : meetingplace.people,
    "table"        : meetingplace.table,
    "outlet"       : meetingplace.outlet,
    "meeting_room" : meetingplace.meeting_room,
    "smoking_room" : meetingplace.smoking_room,
    "meeting"      : meetingplace.meeting,
    "time"         : meetingplace.time,                                         # 영업시간
    "open_close"   : open_close_time(meetingplace.time),                        # 운영중/운영종료 정보제공
    "distance"     : getDistanceBetweenPointsNew(myLat, myLng,                  # 현재위치~미팅룸 거리 계산
                                              float(meetingplace.lat),
                                              float(meetingplace.lon), unit = 'meters'),
    "url"          : meetingplace.url
} for meetingplace in meetingplaces]

### 메인페이지
def main(request):
    # location마다 거리가 짧은 가게 2곳 데이터 선택 (교내 라운지/교내 카페/교외 카페)
    data = sorted(meetingplace_information, key=itemgetter('location', 'distance', 'name'))    # 종목,거리,장소명 순서로 오름차순

    idxLounge = list()
    idxInCafe = list()
    idxOutCafe = list()

    for i in range(len(data)):
        if   data[i]["location"] == "교내 라운지":        
            idxLounge.append(i)
        elif data[i]["location"] == "교내 카페":
            idxInCafe.append(i)
        elif data[i]["location"] == "교외 카페":
            idxOutCafe.append(i)
        else:
            pass
        
    # 거리가 가까운 2곳씩 선정하기
    nearLounges  = data[idxLounge[0]:idxLounge[2]]
    nearInCafes  = data[idxInCafe[0]:idxInCafe[2]]
    nearOutCafes = data[idxOutCafe[0]:idxOutCafe[2]]
    
    nearPlaces = {'nearLounges' : nearLounges,
                  'nearInCafes' : nearInCafes,
                  'nearOutCafes': nearOutCafes}         # 리스트 하나로 만들어 html에 연동하면 어떨까? 
                                                        # -> 카테고리 구분때문에 content 전체 for문을 적용불가
    return render(request, 'main.html', nearPlaces)



### 검색기능 구현
def search(request):    
    if request.method == 'POST':
        searched = request.POST['searched']
        global cafes
        cafes = Meetingplace.objects.filter(name__contains=searched)
        if not cafes:
            csv_to_db(Meetingplace)
            cafes = Meetingplace.objects.filter(name__contains=searched)
            
        
        
        ## map.html에서 반복문 돌리려면 형변환 필요! ##
        meetingdict = []
        for meetingArea in cafes:
            content = {
                    "id"           : meetingArea.id,
                    "name"         : meetingArea.name,
                    "address"      : meetingArea.address,
                    "lat"          : str(meetingArea.lat),
                    "lon"          : str(meetingArea.lon),
                    "location"     : meetingArea.location,
                    "people"       : meetingArea.people,
                    "table"        : meetingArea.table,
                    "outlet"       : meetingArea.outlet,
                    "meeting_room" : meetingArea.meeting_room,
                    "smoking_room" : meetingArea.smoking_room,
                    "meeting"      : meetingArea.meeting,
                    "time"         : meetingArea.time,                                         # 영업시간
                    "open_close"   : open_close_time(meetingArea.time),                        # 운영중/운영종료 정보제공
                    "distance"     : getDistanceBetweenPointsNew(myLat, myLng,                  # 현재위치~미팅룸 거리 계산
                                                            float(meetingArea.lat),
                                                            float(meetingArea.lon), unit = 'meters'),
                    "url"          : meetingArea.url

            }
            meetingdict.append(content)
        meetingJson = json.dumps(meetingdict, ensure_ascii=False)
        
        return render(request, 'map.html',
                      {'searched': searched, 'meetingJson': meetingJson, "kakaokey" : kakaokey,
                       'meetingplace_information':meetingplace_information})   # distance, open_close만 따로   #meetingJson에 포함되므로 필요없을지도 몰라
                       
    else:
        return render(request, 'map.html', {"kakaokey" : kakaokey})

### 필터(희병님 작성코드)
def filter(request):    
    people = request.GET.get('people', None)
    table = request.GET.get('table', None)
    outlet = request.GET.get('outlet', None)
    meeting_room = request.GET.get('meeting_room', None)
    smoking_room = request.GET.get('smoking_room', None)
    meeting = request.GET.get('meeting', None)
    # open_evening = request.GET.get('open_evening', None)

    q = Q()

    # if people != "0":
    #     q &= Q(people=people)
    # if table != "0":
    #     q &= Q(table=table)
    # if outlet != "0":
    #     q &= Q(outlet=outlet)
    # if meeting_room != "0":
    #     q &= Q(meeting_room=meeting_room)
    # if smoking_room != "0":
    #     q &= Q(smoking_room=smoking_room)
    # if meeting != "0":
    #     q &= Q(meeting=meeting)
    # # if open_evening != "0":
    # #     q &= Q(open_evening=open_evening)
    
    ### 수정(221216)
    if people != "0" and people != None:
        q &= Q(people=int(people))
    if table != "0" and table != None:
        q &= Q(table=int(table))
    if outlet != "0" and outlet != None:
        q &= Q(outlet=int(outlet))
    if meeting_room != "0" and meeting_room != None:
        q &= Q(meeting_room=bool(meeting_room))
    if smoking_room != "0" and smoking_room != None:
        q &= Q(smoking_room=bool(smoking_room))
    if meeting != "0" and meeting != None:
        q &= Q(meeting=bool(meeting))


    global cafes
    cafes = Meetingplace.objects.filter(q)
    if not cafes:
        csv_to_db(Meetingplace)
        cafes = Meetingplace.objects.filter(q)
        
    if len(cafes) > 80:
        cafes = cafes[:71]
        
    
    result = [{
        "id"           : cafe.id,
        "name"         : cafe.name,
        "address"      : cafe.address,
        "lat"          : str(cafe.lat),
        "lon"          : str(cafe.lon),
        "location"     : cafe.location,
        "people"       : cafe.people,
        "table"        : cafe.table,
        "outlet"       : cafe.outlet,
        "meeting_room" : cafe.meeting_room,
        "smoking_room" : cafe.smoking_room,
        "meeting"      : cafe.meeting,
        "time"         : cafe.time,                                         # 영업시간
        "open_close"   : open_close_time(cafe.time),                        # 운영중/운영종료 정보제공
        "distance"     : getDistanceBetweenPointsNew(myLat, myLng,                  # 현재위치~미팅룸 거리 계산
                                                float(cafe.lat),
                                                float(cafe.lon), unit = 'meters'),
        "url"          : cafe.url

    } for cafe in cafes]
    
    resultJson = json.dumps(result, ensure_ascii=False)
    
    return render(request, 'map.html', {"resultJson":resultJson, "kakaokey" : kakaokey})
    # return render(request, 'test.html', {"resultJson":cafes, "length":len(cafes)})


def filter_on(request):
    
    return render(request, 'filter.html')


### 1. (검색 ->) 지도 -> 리스트업
### 2. (필터 ->) 지도 -> 리스트업
def listup(request):
    
    return render(request, 'listup.html', {"listupDatas":cafes, "meetingplace_information":meetingplace_information})
    
# def listup(request):
#     # 필터경로
#     filter = True
#     return render(request, 'listup.html', {"cafes":cafes, "filter":filter})



# # 지도 인포윈도우로 가게 상세페이지 들어가기
# def map_to_detail(request):
    
#     return render(request, '')              # detail 페이지로 이동
