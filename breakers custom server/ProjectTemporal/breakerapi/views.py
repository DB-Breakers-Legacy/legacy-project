from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone
import msgpack
import json
import logging
from django.http import HttpResponse

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import asyncio
import os

from django.core.cache import cache #for sessioncounter

from .models import PatrollerUser, MessageBot
from .helpers import (
    getServerDate,
    getSession,
    createAccount,
    calculateUserID,
    env_uri,
    prd_uri,
    ignore_kwargs,
)
from django.conf import settings

#logs
logger = logging.getLogger(__name__)

#constants
SKILLSCAPPEDATONE = [
    130930, 130361, 131921
]

#000000/api/sys/get_env_v3
@ignore_kwargs
def getEnv(request):
    if request.method == 'POST':
        currentdate = getServerDate()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'session': '',
            },
            [0, env_uri(), prd_uri()],
        ]
                
      
        #print("It is active!!!!!") #debug
        #print(respondingData)
        #logger.info("test variable contents: %s",respondingData)
        
        
        packedData = msgpack.packb(respondingData)
        
        response = HttpResponse(packedData) #content_type="application/x-messagepack; charset=utf-8"
        
        return response
    
#BANDAI SERVER RESP: result date 2026/01/24 12:33:52 session https://cosmos.channel.or.jp/&https://dbtb-prd.cosmos.channel.or.jp/    
    
#000000/api/sys/agree_kpi
@ignore_kwargs
def agreeKPI(request):
    if request.method == 'POST':
        currentdate = getServerDate()

        #BANDAI RESP: [{'result': 0, 'date': '2026/05/21 18:54:33', 'session': ''}, [0]]
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'session': '',
            },
            [0],
        ]

        packedData = msgpack.packb(respondingData)
        response = HttpResponse(packedData)
        return response

#025348/api/sys/kpi
@ignore_kwargs
def envKPI(request):
    if request.method == 'POST':
        currentdate = getServerDate()

        #BANDAI RESP: [{'result': 0, 'date': '2026/05/21 18:55:31', 'version': '09.01', 'flag': '0', 'session': '6a0f55233e251'}, [0]]
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            },
            [0],
        ]

        packedData = msgpack.packb(respondingData)
        response = HttpResponse(packedData)
        return response

#000000/api/user/auth
#
# CURRENTLY BYPASSED IN BINARY, note: this is checked by save data, use your own
# save's ID for testing as we dont have account creation yet.
@ignore_kwargs
def getUserAuth(request):
    if request.method == 'POST':
        currentdate = getServerDate()
        countSession = getSession()
        
        unpacked = msgpack.unpackb(request.body, raw=False)
        requestUserID = unpacked[1][0] #Maybe put some random server-side salt because steamID is public
        createAccount(requestUserID)
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'session': countSession,
            },
            [0, [requestUserID, 0]],
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
#result date 2026/01/24 12:33:53 session 6974bc3111f68 289193220923131928
        
    
#000000/api/user/get_country
@ignore_kwargs
def getUserCountry(request):
    if request.method == 'POST':
        currentdate = getServerDate()
        countSession = getSession()
        
        #countryCode = request.ipinfo.country #setup later
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'session': countSession,
            },
            [0, 'GB'],
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
    
#result date 2026/01/24 12:33:53 session 6974bc317e519 GB


#000000/api/user/get_tracking_num
#useful as an indicator that the server is working.
@ignore_kwargs
def getTrackingNum(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        #HIYA-BREADBREAKR
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'session': countSession,
            },
            [0, 'HIYA-BREADBREAKR'],
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
    
#result date 2026/01/24 12:33:53 session 6974bc31aeb12 ZSYY-UPA8U2YQ2SF HIYA-BREADBREAKR


#025348/api/close/get_close_info
@ignore_kwargs
def getCloseInfo(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            },
            [0, '', [[1, '2100-01-01 07:00:00'], [2, '2100-01-01 07:15:00'], [3, '2100-01-01 07:25:00'], [4, '2125-07-01 00:00:00']], [], [0, '', '', 0, '']],
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
    
#I have no idea what this could mean
#result date 2026/01/24 17:44:19 version 09.00 flag 0 session 697504f33f560 2100-01-01 07:00:00 2100-01-01 07:15:00 2100-01-01 07:25:00 2125-07-01 00:00:00   


#025348/api/user/create_user_info
@ignore_kwargs
def createUserInfo(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        unpacked = msgpack.unpackb(request.body, raw=False)
        usrCountryCode = unpacked[1][0]
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            },
            [0, usrCountryCode, 0],
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
    
#result date 2026/01/24 17:44:19 version 09.00 flag 0 session 697504f37b58f GB


#025348/api/adjustment_data_manage/read
@ignore_kwargs
def readAdjustmentData(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        #adjustmentData
        adjustmentDataLocation = os.path.join('adjustmentdata.txt')
        try:
            with open(adjustmentDataLocation, 'r', encoding='utf-8') as f:
                adjustmentData = f.read()
        except FileNotFoundError:
            print("adjustment data missing!")

        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            },
            [0, 2, adjustmentData],
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
    
#I have no idea why tf it sends a massive string, hopefully its not too important, might be gamestate, changing flight speed, numbers etc...
#result date 2026/01/24 17:44:20 version 09.00 flag 0 session 697504f436666 BLAH

#Start menu calls ends here!

#Game start calls

#025348/api/battle/get_stun_server_info 
@ignore_kwargs
def getStunServer(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        #NOTE: We will need our own STUN server when official shuts down! note: I think we can just use official without issue?
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            },
            [0, [['dbform-prd-025348-stun01.cosmos.channel.or.jp', 3478], ['dbform-prd-025348-stun02.cosmos.channel.or.jp', 3478]]],
        ]


        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        #[0, [['dbform-prd-025348-stun01.cosmos.channel.or.jp', 3478], ['dbform-prd-025348-stun02.cosmos.channel.or.jp', 3478]]], https://cosmos.channel.or.jp/& https://127.0.0.1/LALALALALA/'


#025348/api/patroller/get_status
@ignore_kwargs
def getPatrollerStatus(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        #TODO get patroller status from user db, then combine with season pass.
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #looks like season pass
            #1st list is survivor lvl, lvlprogress??, zeni, spirit, ??
            [0, [208, 16150, 1049219, 435491, 0], [19, 4990, 0, 20, 1230, 2], [19, 4990, 20, 1230], [9, '2025-07-30 02:00:00', '2050-12-31 14:59:59', 9, 85, [[1, 1, 1, 150, [['ZENY', 0, 5000]]], [2, 1, 5, 150, [['SPIRIT', 0, 500]]], [3, 1, 6, 150, [['TicketID', 10000, 1]]], [4, 1, 6, 150, [['TicketID', 90100, 1]]], [5, 1, 6, 150, [['TP_COIN', 0, 50]]], [6, 1, 6, 150, [['ZENY', 0, 5000]]], [7, 1, 6, 150, [['TicketID', 10000, 1]]], [8, 1, 8, 150, [['TicketID', 90100, 1]]], [9, 1, 8, 150, [['TP_COIN', 0, 50]]], [10, 1, 8, 150, [['TicketID', 10000, 1]]], [11, 1, 8, 150, [['ZENY', 0, 5000]]], [12, 1, 8, 150, [['SPIRIT', 0, 500]]], [13, 1, 8, 150, [['ZENY', 0, 10000]]], [14, 1, 8, 150, [['TicketID', 90100, 1]]], [15, 1, 8, 150, [['TP_COIN', 0, 50]]], [16, 1, 8, 150, [['ZENY', 0, 10000]]], [17, 1, 8, 150, [['SPIRIT', 0, 500]]], [18, 1, 8, 150, [['ZENY', 0, 10000]]], [19, 1, 8, 150, [['TicketID', 10000, 1]]], [20, 1, 10, 150, [['TP_COIN', 0, 50]]], [21, 1, 10, 150, [['ZENY', 0, 15000]]], [22, 1, 10, 150, [['SPIRIT', 0, 1000]]], [23, 1, 10, 150, [['ZENY', 0, 15000]]], [24, 1, 10, 150, [['TicketID', 90100, 1]]], [25, 1, 10, 150, [['TP_COIN', 0, 100]]], [26, 1, 10, 150, [['ZENY', 0, 15000]]], [27, 1, 10, 150, [['SPIRIT', 0, 1000]]], [28, 1, 10, 150, [['TicketID', 10000, 1]]], [29, 1, 10, 150, [['TicketID', 90100, 1]]], [30, 1, 10, 150, [['StampID', 1100, 1]]], [31, 1, 10, 150, [['ZENY', 0, 15000]]], [32, 1, 10, 150, [['TicketID', 10000, 1]]], [33, 1, 10, 150, [['TicketID', 90100, 1]]], [34, 1, 10, 150, [['TicketID', 10000, 1]]], [35, 1, 12, 150, [['TP_COIN', 0, 100]]], [36, 1, 12, 150, [['TicketID', 10000, 1]]], [37, 1, 12, 150, [['TicketID', 90100, 1]]], [38, 1, 12, 150, [['TicketID', 10000, 1]]], [39, 1, 12, 150, [['TicketID', 90100, 1]]], [40, 1, 12, 150, [['StampID', 1080, 1]]], [41, 1, 12, 150, [['ZENY', 0, 20000]]], [42, 1, 12, 150, [['TicketID', 10000, 1]]], [43, 1, 12, 150, [['TicketID', 90100, 1]]], [44, 1, 12, 150, [['TicketID', 10000, 1]]], [45, 1, 16, 150, [['TP_COIN', 0, 100]]], [46, 1, 16, 150, [['SPIRIT', 0, 1500]]], [47, 1, 16, 150, [['TicketID', 90100, 1]]], [48, 1, 16, 150, [['TicketID', 10000, 1]]], [49, 1, 16, 150, [['TicketID', 90100, 1]]], [50, 1, 18, 150, [['StampID', 1090, 1]]], [51, 1, 20, 0, [['TicketID', 10000, 1]]], [52, 1, 20, 0, [['TicketID', 90100, 1]]], [53, 1, 20, 0, [['TicketID', 10000, 1]]], [54, 1, 20, 0, [['TicketID', 90100, 1]]], [55, 1, 20, 0, [['TicketID', 10000, 1]]], [56, 1, 20, 0, [['TicketID', 90100, 1]]], [57, 1, 20, 0, [['TicketID', 10000, 1]]], [58, 1, 20, 0, [['TicketID', 90100, 1]]], [59, 1, 20, 0, [['TicketID', 10000, 1]]], [60, 1, 20, 0, [['CostumeItemID', 114135, 1]]], [61, 1, 20, 0, [['TicketID', 10000, 2]]], [62, 1, 20, 0, [['TicketID', 90100, 1]]], [63, 1, 20, 0, [['TicketID', 10000, 2]]], [64, 1, 20, 0, [['TicketID', 90100, 1]]], [65, 1, 20, 0, [['TicketID', 10000, 2]]], [66, 1, 20, 0, [['TicketID', 90100, 2]]], [67, 1, 20, 0, [['TicketID', 10000, 2]]], [68, 1, 20, 0, [['TicketID', 90100, 2]]], [69, 1, 20, 0, [['TicketID', 90100, 2]]], [70, 1, 20, 0, [['CostumeItemID', 114134, 1]]]], 35, [['TicketID', 90100, 1]], ['https://127.0.0.1/static/patrollerstatus1.png', 'https://127.0.0.1/static/patrollerstatus2.png']], [5, 0, 2, 2, '2026-07-10 05:59:59'], ['', 0], [1, 1, 1], 0, 0, '2026-07-13 06:00:00', '2026-07-27 05:59:59']
        ] #these dates need to be ahead or game closes connection
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)

#025348/api/gamecurrency/get_owned
@ignore_kwargs
def getGameCurrencyOwned(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        #get user ID
        unpacked = msgpack.unpackb(request.body, raw=False)
        requestUserID = unpacked[0]['userId']
        
        #get response data
        userObj = PatrollerUser.objects.get(userID=requestUserID)
        responseData = userObj.gameCurrency
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            },
            responseData
            #[TPTOTAKE??, TP, TPTOGET, '', ??, '??']
        ]
        
        #example [0, 62, 19, '', 0, '0']
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        
#Rival (raider) training/data

#025348/api/rival/get_list
@ignore_kwargs
def getRivalList(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        #get user ID
        unpacked = msgpack.unpackb(request.body, raw=False)
        requestUserID = unpacked[0]['userId']
        
        #get response data
        userObj = PatrollerUser.objects.get(userID=requestUserID)
        responseData = userObj.rivalList
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            },
            responseData
        ]
        
        #structure: [RAIDERID, RAIDERLVL, RAIDERLVLPROG, SKILLPOINTS, [[SKILLID, SKILLLEVEL], [80010, 1], [80020, 20], [80030, 5]], [[180000, 20], [180010, 20], [180020, 0], [180030, 0]], [RAIDERLINES, 1002001, 1002002, 1002003, 1002004, 1002005, 1002007, 1002008, 1002010, 1002011, 1002012, 1002013, 1002014, 1003000, 1003001, 1003002, 1003004, 1003006, 1003007, 1003008, 1003009, 1003011, 1003012, 1003015, 1004001, 1004002, 1004003, 1004005, 1004007, 1004008, 1004010, 1004011, 1004014, 1004015, 1004018, 1004020, 1004021, 1004022, 1004023, 1004026, 1004028, 1004029, 1004032, 1004033]]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        
#025348/api/rival/skill_reset
#
#example POST: [{'titleCd': '025348', 'userId': '289193220923131928', 'session':
#'69c53c10d8143', 'platform': 3, 'version': '09.01'}, [1200]]
@ignore_kwargs
def rivalSkillReset(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        #get user ID
        unpacked = msgpack.unpackb(request.body, raw=False)
        requestUserID = unpacked[0]['userId']
        
        #get raider ID
        requestRaiderID = unpacked[1][0]
        
        userObj = PatrollerUser.objects.get(userID=requestUserID)
        raiderList = userObj.rivalList
        
        #prepare index by counting all raider ids
        raiderIndex = [x[0] for x in raiderList[1]] #Example [100, 200, 300, 400, 600, 700, 800, 1200, 1300]
        
        requestedRaiderArray = [x for x in raiderList[1] if x[0] == requestRaiderID]
        #exmp result: [[1200, 3, 0, 0, [[80200, 0], [80230, 0], [80240, 0], [80250, 0], [81100, 0], [81110, 0], [81120, 0], [81130, 0]], [[180220, 0], [181100, 2], [181110, 0], [181120, 0], [181130, 0], [181140, 0]], [3001001, 3002000, 3002014, 3003000, 3003006, 12004000, 12004003, 12004005, 12004010, 12004012, 12004014, 12004015, 12004020, 12004023]]]
        
        resultPoints = raiderList[1][raiderIndex.index(requestRaiderID)][3]
        
        #update database
        updatedRaiderArray = raiderList
        
        for x in updatedRaiderArray[1][raiderIndex.index(requestRaiderID)][4]:
            resultPoints += x[1]
            x[1] = 0
        for x in updatedRaiderArray[1][raiderIndex.index(requestRaiderID)][5]:
            resultPoints += x[1]
            x[1] = 0
        
        updatedRaiderArray[1][raiderIndex.index(requestRaiderID)][3] = resultPoints
            
        userObj.rivalList = updatedRaiderArray
        userObj.save()
        
        #response
        responseData = [0, [requestRaiderID, resultPoints, requestedRaiderArray[0][4], requestedRaiderArray[0][5]]]

        for x in responseData[1][2]:
            x[1] = 0
        for x in responseData[1][3]:
            x[1] = 0
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            },
            responseData
        ]
        
        #response: [0, [1200, 2, [[80200, 0], [80230, 0], [80240, 0], [80250, 0], [81100, 0], [81110, 0], [81120, 0], [81130, 0]], [[180220, 0], [181100, 0], [181110, 0], [181120, 0], [181130, 0], [181140, 0]]]]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        
#[{'titleCd': '025348', 'userId': '289193220923131928', 'session': '69ca7688ae9b3', 'platform': 3, 'version': '09.01'}, [[[1300, 181200, 19], [1300, 181210, 1]]]]
#025348/api/rival/training
@ignore_kwargs
def rivalTraining(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        #get user ID
        unpacked = msgpack.unpackb(request.body, raw=False)
        requestUserID = unpacked[0]['userId']
        
        #user raider list
        userObj = PatrollerUser.objects.get(userID=requestUserID)
        raiderList = userObj.rivalList
        updatedRaiderArray = raiderList
        
        
        #prepare index by counting all raider ids
        raiderIndex = [x[0] for x in raiderList[1]] #Example [100, 200, 300, 400, 600, 700, 800, 1200, 1300]
        #exmp result: [[1200, 3, 0, 0, [[80200, 0], [80230, 0], [80240, 0], [80250, 0], [81100, 0], [81110, 0], [81120, 0], [81130, 0]], [[180220, 0], [181100, 2], [181110, 0], [181120, 0], [181130, 0], [181140, 0]], [3001001, 3002000, 3002014, 3003000, 3003006, 12004000, 12004003, 12004005, 12004010, 12004012, 12004014, 12004015, 12004020, 12004023]]]
        

        #loop through request and set skill lvl
        #[[1300, 181200, 19], [1300, 181210, 1]]
        for x in unpacked[1][0]: 
            raiderTrainID = x[0]
            raiderTrainSkillID = x[1]
            raiderTrainSkillVal = x[2]
            raiderPointsLeft = raiderList[1][raiderIndex.index(raiderTrainID)][3]
            raiderPointsLeft -= raiderTrainSkillVal
            
            if raiderPointsLeft < 0:
                #TODO: handle, log, maybe force raider reset?
                break
            
            updatedRaiderArray[1][raiderIndex.index(raiderTrainID)][3] = raiderPointsLeft
            
            #index actives: [80200, 80230, 80240, 80250, 81100, 81110, 81120, 81130]
            skillIndex = [x[0] for x in raiderList[1][raiderIndex.index(raiderTrainID)][4]]
            passiveActiveIndex = 4
            if raiderTrainSkillID not in skillIndex:
                #index passives
                skillIndex = [x[0] for x in raiderList[1][raiderIndex.index(raiderTrainID)][5]]
                passiveActiveIndex = 5
            
            for x in updatedRaiderArray[1][raiderIndex.index(raiderTrainID)][passiveActiveIndex]:
                if x[0] == raiderTrainSkillID:
                    x[1] = raiderTrainSkillVal
                    break
                    
        userObj.rivalList = updatedRaiderArray
        userObj.save()
        
        #response
        responseData = [0, []]
        for x in raiderIndex:
            responseData[1] += [[x, updatedRaiderArray[1][raiderIndex.index(x)][3], updatedRaiderArray[1][raiderIndex.index(x)][4], updatedRaiderArray[1][raiderIndex.index(x)][5]]]
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            },
            responseData
        ]
        
        #[0, [[100, 0, [[80000, 4], [80010, 1], [80020, 20], [80030, 5]], [[180000, 20], [180010, 20], [180020, 0], [180030, 0]]], [200, 0, [[80100, 0], [80110, 0], [80120, 0], [80130, 16]], [[180100, 20], [180110, 7], [180120, 0], [180130, 0]]], [300, 0, [[80200, 1], [80210, 6], [80220, 1], [80230, 0], [80240, 1]], [[180200, 20], [180210, 20], [180220, 0], [180230, 0]]], [400, 0, [[80300, 0], [80310, 1], [80320, 0], [80330, 0], [80340, 0], [80350, 0], [80360, 6], [80370, 0], [80380, 0]], [[180300, 20], [180301, 0], [180302, 0], [180303, 0], [180310, 20], [180311, 20], [180312, 0], [180320, 0], [180321, 0], [180323, 20], [180324, 0], [180330, 0]]], [600, 0, [[80500, 20], [80510, 11], [80520, 4], [80530, 0], [80540, 1]], [[180500, 1], [180501, 20], [180502, 0], [180503, 0]]], [700, 0, [[80600, 0], [80610, 2], [80620, 20], [80630, 2], [80640, 0], [80650, 0], [80660, 0], [80670, 0]], [[180600, 20], [180601, 2], [180610, 0], [180620, 0], [180621, 0], [180622, 0]]], [800, 0, [[80700, 7], [80710, 0], [80720, 0], [80730, 0], [80740, 2], [80750, 20], [80760, 0], [80770, 0]], [[180700, 20], [180701, 0], [180702, 0], [180710, 0], [180720, 0], [180730, 0]]], [1200, 0, [[80200, 0], [80230, 0], [80240, 0], [80250, 0], [81100, 0], [81110, 0], [81120, 0], [81130, 1]], [[180220, 0], [181100, 0], [181110, 1], [181120, 0], [181130, 0], [181140, 0]]], [1300, 0, [[81200, 0], [81201, 0], [81210, 0], [81220, 0], [81230, 0], [81231, 0], [81240, 0], [81241, 0], [81250, 0], [81260, 0], [81270, 0]], [[181200, 0], [181201, 0], [181202, 0], [181203, 0], [181210, 0], [181211, 20], [181212, 0], [181230, 0], [181231, 0], [181232, 0]]]]]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)        
        
        
#025348/api/avatar_create/get_list
@ignore_kwargs
def getAvatarCreateList(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            },
            [0, [], []] #investigate
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
#025348/api/character/get
@ignore_kwargs
def getCharacter(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        #get user ID
        unpacked = msgpack.unpackb(request.body, raw=False)
        requestUserID = unpacked[0]['userId']
        
        #get response data
        userObj = PatrollerUser.objects.get(userID=requestUserID)
        responseData = userObj.userCharacters
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #add to database, 2nd part looks like skills
            responseData
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        
#025348/api/character/get_item
@ignore_kwargs
def getCharacterItems(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #items and their acquisition date
            [0, [[2150, '2023-11-02 09:58:53'], [2157, '2023-12-20 16:30:03'], [2166, '2023-12-31 18:25:40'], [2170, '2023-11-12 15:20:07'], [2179, '2024-07-01 12:38:57'], [2183, '2024-12-10 21:14:15'], [2185, '2024-12-10 21:14:12'], [2187, '2025-02-26 20:13:57'], [2188, '2025-02-26 20:13:52'], [2189, '2025-02-26 20:13:48'], [2191, '2025-07-30 10:50:14'], [2193, '2025-07-30 10:50:17'], [2194, '2025-07-30 10:50:20'], [6106, '2022-10-14 09:10:00'], [6200, '2022-10-14 09:10:00'], [6403, '2022-10-14 09:10:00'], [6705, '2022-10-14 09:10:00'], [13406, '2022-10-14 09:10:00'], [18402, '2023-09-05 15:26:22'], [21700, '2024-12-30 19:04:53'], [21701, '2024-12-24 18:57:25'], [21704, '2025-01-01 16:08:17'], [50011, '2023-11-09 14:51:09'], [50021, '2023-11-02 14:22:43'], [50041, '2023-11-07 10:53:32'], [50071, '2023-11-02 12:35:50'], [50111, '2023-12-17 22:10:02'], [50121, '2023-12-09 17:57:51'], [50141, '2023-12-08 15:51:19'], [50711, '2024-05-04 15:48:21'], [50721, '2024-05-01 20:06:00'], [50741, '2024-04-30 15:48:42'], [51221, '2024-08-23 17:27:37'], [51231, '2024-08-10 18:51:23'], [51241, '2024-09-09 16:59:20'], [51611, '2024-03-05 22:59:53'], [51621, '2024-03-02 22:01:40'], [51641, '2024-03-02 19:11:58'], [52221, '2024-07-03 13:32:32'], [52231, '2024-07-04 13:20:55'], [52241, '2024-07-01 14:19:32'], [52310, '2024-08-10 20:18:49'], [52320, '2024-08-10 18:50:52'], [52330, '2024-07-03 13:45:32'], [52340, '2024-07-09 15:51:05'], [52621, '2024-12-11 23:03:41'], [52641, '2024-12-10 22:48:31'], [53040, '2023-12-24 15:55:56'], [53310, '2023-12-11 17:35:03'], [53320, '2023-12-11 16:09:32'], [53340, '2023-12-08 16:10:36'], [54110, '2024-05-25 17:39:49'], [54120, '2024-05-07 18:33:07'], [54140, '2024-05-11 14:56:56'], [54170, '2024-05-18 17:08:04'], [54210, '2024-05-05 15:56:08'], [54220, '2024-05-04 16:12:03'], [54240, '2024-05-04 18:24:21'], [54671, '2025-05-18 20:12:37'], [55110, '2024-09-23 14:04:01'], [55120, '2024-10-08 14:15:08'], [55130, '2024-09-25 17:38:46'], [55140, '2024-10-02 18:27:55'], [100003, '2022-10-14 09:10:00'], [101800, '2023-12-20 16:15:08'], [112010, '2023-11-02 13:36:12'], [112021, '2022-10-14 09:16:13'], [112032, '2022-10-14 11:17:29'], [113060, '2023-11-07 11:34:25'], [113070, '2024-03-02 19:10:58'], [114061, '2024-05-03 22:15:48'], [114090, '2022-10-15 17:06:43'], [114100, '2023-11-16 10:48:34'], [114134, '2026-01-03 14:44:32'], [114135, '2025-12-23 16:25:54'], [115001, '2024-05-25 17:40:41'], [115002, '2022-10-14 09:16:59'], [115003, '2024-05-05 16:47:12'], [115027, '2023-12-15 21:12:28'], [116020, '2022-10-25 18:53:46'], [116021, '2023-12-15 20:36:08'], [116036, '2024-07-09 15:00:17'], [116080, '2023-12-07 16:09:48'], [116110, '2024-03-10 17:05:26'], [116140, '2024-05-03 20:28:08'], [116190, '2023-12-03 16:51:09'], [116200, '2023-11-05 22:12:35'], [120030, '2022-10-16 15:12:31'], [120033, '2023-11-09 14:24:32'], [120034, '2024-03-05 20:36:05'], [120035, '2024-07-11 19:08:06'], [120036, '2024-12-16 22:37:02'], [120052, '2023-11-22 18:01:29'], [120054, '2022-11-15 21:56:34'], [120080, '2024-05-01 19:52:25']], [[10, '2022-10-14 09:10:00'], [60, '2022-10-14 09:10:00'], [70, '2022-10-16 15:17:31'], [80, '2022-10-16 15:17:51'], [110, '2023-11-03 10:01:03'], [130, '2022-10-14 10:50:07'], [140, '2022-10-14 10:50:07'], [280, '2023-11-26 12:37:34'], [290, '2025-04-17 18:16:02'], [300, '2023-12-19 19:01:27'], [320, '2025-07-28 14:40:38'], [390, '2022-10-14 09:10:00'], [400, '2025-07-28 14:40:01'], [430, '2025-07-28 14:40:34'], [440, '2025-07-28 14:40:26'], [650, '2022-10-14 09:10:00'], [670, '2022-11-15 21:31:41'], [680, '2025-07-28 14:39:58'], [690, '2024-03-03 17:57:17'], [700, '2024-05-01 22:12:21'], [730, '2025-06-07 15:39:40'], [920, '2024-05-06 17:32:09'], [970, '2024-03-08 16:02:07'], [1040, '2025-05-16 17:38:48']], [[10, '2022-10-14 09:10:00'], [20, '2022-10-14 09:10:00'], [30, '2022-10-14 09:10:00'], [40, '2022-10-14 09:10:00'], [50, '2022-10-14 09:10:00'], [60, '2022-11-15 21:32:01'], [100, '2023-11-03 10:00:39'], [110, '2022-10-15 17:49:48'], [140, '2022-10-14 13:06:19'], [190, '2022-10-14 09:10:00'], [200, '2022-10-14 09:10:00'], [210, '2022-10-14 09:10:00'], [220, '2025-07-28 14:40:45'], [230, '2024-07-01 12:41:07'], [240, '2024-09-21 15:24:47'], [250, '2023-11-03 10:00:26'], [260, '2024-08-23 17:11:50'], [270, '2022-11-15 21:32:08'], [300, '2025-04-17 18:16:20'], [390, '2025-04-17 18:16:17'], [470, '2024-12-21 21:06:30'], [560, '2023-11-18 14:42:57'], [590, '2023-11-11 11:59:17'], [610, '2023-12-19 19:11:42'], [630, '2024-07-01 12:41:48'], [700, '2024-03-03 19:29:55'], [710, '2024-05-02 16:02:13'], [720, '2024-05-06 20:31:02'], [750, '2024-03-08 15:10:17'], [760, '2024-05-18 17:08:49'], [780, '2024-09-22 16:31:36'], [790, '2024-07-04 13:31:12'], [820, '2024-09-21 15:23:14'], [850, '2024-12-22 18:52:11'], [870, '2024-12-29 19:13:14'], [880, '2024-12-21 23:48:00'], [890, '2024-12-14 18:28:35'], [910, '2024-12-11 23:46:54'], [950, '2025-05-17 15:35:03'], [960, '2025-05-14 18:48:50'], [970, '2025-05-11 17:42:30'], [1030, '2025-05-15 18:49:30'], [1080, '2025-11-22 14:56:20'], [1090, '2025-11-25 15:18:11'], [1100, '2025-11-19 22:31:25']], [[90, '2023-11-19 16:09:07'], [1000, '2022-10-14 09:10:00'], [1160, '2024-04-28 18:26:33'], [1260, '2023-11-11 17:07:37'], [1280, '2022-11-06 22:12:58'], [1300, '2022-11-15 21:32:50'], [1320, '2025-07-28 14:41:01']], [[10, '2022-10-14 09:10:00'], [90, '2023-11-02 14:31:18'], [130, '2022-11-15 21:32:39'], [220, '2022-10-19 17:05:48'], [260, '2024-03-03 18:19:15'], [270, '2024-03-02 19:38:43']], [[1, 1, 1, '2022-10-14 09:10:00']]]
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
#025348/api/battle/get_diarkis_matching_server_info
@ignore_kwargs
def getMatchingServer(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #investigate
            [0,
             #ip addr and port for UDP server
             [settings.UDP_HOST,
              settings.UDP_PORT,
              # IV key, decrypt Key, sid key, hash key
              # INVESTIGATE: where tf does SID ever get used?
              '185af50497054644bf89f96ff2f798b2',
              '3710c0f30922423a8fd8befcc1f83b3d',
              'c2498a5532f947808e8684812b022b95',
              '61a174c3f20a4b75bb4d2f17e183f25e'],
             [1, 1]]
        ] 
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        
#025348/api/user/get_ban_status
@ignore_kwargs
def getBanStatus(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #investigate
            [0, 0, 0]
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        

#025348/api/commonpurchase/get_purchase_status
@ignore_kwargs
def getPurchaseStatus(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #investigate
            [0, '']
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        
        
#025348/api/item/get_item_possession
@ignore_kwargs
def getItemPossession(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #investigate
            [0, []]
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        

#025348/api/battle/get_challenge_list
@ignore_kwargs
def getChallengeList(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #investigate
            [0, [1, 1, [[1, 3, 14969, 102, 'challenge_match_count', 'ChallengeObjective_match_count', 1, 3], [1, 3, 15136, 902, 'challenge_open_crate', 'ChallengeObjective_open_crate', 2, 10], [1, 3, 15138, 1002, 'challenge_open_treasure', 'ChallengeObjective_open_treasure', 0, 3]], [[1, 9644, 10301, 'challenge_survivor_match_count', 'ChallengeObjective_patroller_match_count', 6, 15], [1, 9656, 200, 'challenge_raider_match_count', 'ChallengeObjective_villain_match_count', 1, 3], [1, 9697, 3101, 'challenge_revive_survivor', 'ChallengeObjective_revive_patroller', 1, 10], [1, 9732, 2001, 'challenge_launch__and_alive', 'ChallengeObjective_launch__and_alive', 1, 2], [1, 9735, 14100, 'challenge_dragon_change', 'ChallengeObjective_dragon_change', 4, 10], [1, 9738, 13601, 'challenge_discover_launch_key', 'ChallengeObjective_discover_launch_key', 0, 5], [1, 9740, 1801, 'challenge_open_aidbox', 'ChallengeObjective_open_aidbox', 0, 3], [1, 9741, 802, 'challenge_reach_translevel_3', 'ChallengeObjective_reach_translevel_3', 0, 5], [1, 9742, 3801, 'challenge_interact_launch_system', 'ChallengeObjective_interact_launch_system', 9, 60], [1, 9743, 2100, 'challenge_win_raider', 'ChallengeObjective_win_villain', 0, 1]]]]
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        
        
#025348/api/event/get_schedule_list
@ignore_kwargs
def getScheduleList(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #investigate
            [0, [['UPCP_2512_01', '1226_UPCP_ssp01', 1, '2025-12-26 06:00:00', '2026-01-28 05:59:59', 1, -1, '', '', '[{"battle_match_type":3,"role_type":2,"bonus_type":3,"cubed_count":1.1}]']]]
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        
#025348/api/user/update_manner_point
@ignore_kwargs
def updateMannerPoint(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #investigate
            [0, 0, 0]
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        
#025348/api/bnid_reward/grant_reward
@ignore_kwargs
def grantReward(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #investigate
            [1501]
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        

#025348/api/message/get_message_list
#POST: [{'titleCd': '025348', 'userId': '289193220923131928', 'session': '69c53b6c88849', 'platform': 3, 'version': '09.01'}, ['en', 'GB']]
@ignore_kwargs
def getMessageList(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        #get user ID
        unpacked = msgpack.unpackb(request.body, raw=False)
        requestUserID = unpacked[0]['userId']
        
        #get response data
        userObj = PatrollerUser.objects.get(userID=requestUserID)
        responseData = userObj.messageList
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, 
            responseData
        ]
        
        #message structure
        #[1, 'localhosttesting_20260326154312', 'breadbreakr test 1', '2026-01-23 17:46:11', '2050-02-22 17:46:11', 1, 3]
        #[[??, 'id', 'message name', 'send date', 'valid date', ??, iconstatus]
        #icon status: 3 == taken, 2 == gift, 1 == message
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
#[0, [[1, 'localhosttesting_20260326154312', 'breadbreakr test 1', '2026-01-23 17:46:11', '2050-02-22 17:46:11', 1, 3], [2, 'localhosttesting_20260327133850', 'breadbreakr test 2', '2026-01-23 17:46:11', '2069-02-22 17:46:11', 0, 2], [2, 's_0_13_17_1_20251226135526', 'Notice of Ranked Match Rewards', '2025-12-26 13:55:25', '2026-01-25 13:55:25', 1, 3], [2, 's_1_13_16_1_20251226135526', 'Notice of Ranked Match Rewards', '2025-12-26 13:55:25', '2026-01-25 13:55:25', 1, 3], [1, '200221013_OBTtest_O3', 'Notification of Beta-Test Special Reward', '2022-10-12 15:00:00', '2050-12-31 14:59:59', 1, 3], [1, 'wo_2022101301', 'Official Launch Commemorative Gift 1', '2022-10-12 15:00:00', '2050-12-31 14:59:59', 1, 3], [1, 'wo_2022101302', 'Official BLAH Commemorative Gift 2', '2022-10-12 15:00:00', '2050-12-31 14:59:59', 1, 3]]]
        
#025348/api/message/get_message_info
#example POST: [{'titleCd': '025348', 'userId': '289193220923131928', 'session': '69c53c0d454b8', 'platform': 3, 'version': '09.01'}, ['en', 1, '20260313_CosMatch']]
@ignore_kwargs
def getMessageInfo(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        #get message ID
        unpacked = msgpack.unpackb(request.body, raw=False)
        requestMessageID = unpacked[1][2]
        
        #get response data
        messageInfo = MessageBot.objects.get(messageID=requestMessageID)
        responseData = messageInfo.messageContents
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #investigate
            responseData
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
#example RESPONSE: [0, 1, '20260313_CosMatch', 'Notice of Costume Party Campaign Rewards', 'We will be distributing rewards for players using certain costumes in online matches during the Costume Party Campaign.<br><br>▼ Gifts<br>- TP Token x 50<br>- Season 9 Spirit Siphon Ticket x 2<br>Please claim items before messages are deleted.<br><br>Based on the results of the tally, wallpapers for use on computers and smartphones are also being distributed on the official X account and official website!<br>Check out the official X page and official site!<br><br>Official X (formerly Twitter) Account<br>Japanese: @DB_THEBREAKERS<br>English: @DBTB_EN<br><br>Official Site<br>Japanese page: https://dbas.bn-ent.net/<br>English page: https://dbas.bn-ent.net/en/', 1, 2, [['TP_COIN', 0, 50], ['TicketID', 90100, 2]], '2026-03-25 06:00:00', '2026-04-08 05:59:59']


#025348/api/message/update_message_item_received
@ignore_kwargs
def updateMessageList(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        #LOW PRIO TODO: get resource values from message and apply it to user values, then get message info and set status to taken
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            },
            [0]
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
#025348/api/regularly_run/get_emergency_message
@ignore_kwargs
def getEmergencyMessage(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #investigate
            [0, [['10', '2025-05-11 06:00:00', '2028-05-12 05:29:59', 'PWNED BY BREADBREAKR!! >:D PWNED BY BREADBREAKR!! >:D PWNED BY BREADBREAKR!! >:D PWNED BY BREADBREAKR!! >:D.']]]
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        
        
#025348/api/news/get_3d_model_news
@ignore_kwargs
def get3DModelNews(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #investigate
            [0, [['https://127.0.0.1/static/3dmodelnews.png', '2026-01-09 06:00:00', '2026-02-03 05:59:59']]]
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        
        
#025348/api/lootbox/ticket_master_list
@ignore_kwargs
def ticketMasterList(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #investigate
                          # XXX(dmr): figure out wtf to do with static
            [0, [[10000, 'Spirit Siphon Ticket', 'https://127.0.0.1/static/tickets1.png', '2022-01-29 15:00:00', '2099-12-31 14:59:59'], [10010, 'Guaranteed Skill Summon Ticket', 'https://127.0.0.1/static/tickets2.png', '2022-01-29 15:00:00', '2023-02-16 00:59:59'], [10020, '5-Star Transphere Guaranteed Ticket', 'https://127.0.0.1/static/tickets3.png', '2022-01-20 06:00:00', '2023-02-23 05:59:59'], [10100, 'Season 1 Spirit Siphon Ticket', 'https://127.0.0.1/static/tickets4.png', '2022-01-29 15:00:00', '2023-02-16 00:59:59'], [11000, 'Spirit Siphon Trial Ticket', 'https://127.0.0.1/static/tickets5.png', '2022-01-29 15:00:00', '2099-12-31 14:59:59'], [20100, 'Season 2 Spirit Siphon Ticket', 'https://127.0.0.1/static/tickets6.png', '2022-01-29 15:00:00', '2023-06-19 06:00:00'], [30100, 'Season 3 Spirit Siphon Ticket', 'https://127.0.0.1/static/tickets7.png', '2022-01-29 15:00:00', '2023-11-01 00:59:59'], [40010, '1st Anniversary Ticket', 'https://127.0.0.1/static/tickets8.png', '2022-01-29 15:00:00', '2024-02-29 00:59:59'], [40020, 'Premium 1st Anniversary Ticket', 'https://127.0.0.1/static/tickets9.png', '2022-01-29 15:00:00', '2024-03-13 05:59:59'], [40100, 'Season 4 Spirit Siphon Ticket', 'https://127.0.0.1/static/tickets10.png', '2022-01-29 15:00:00', '2024-02-29 00:59:59'], [50100, 'Season 5 Spirit Siphon Ticket', 'https://127.0.0.1/static/tickets11.png', '2022-01-29 15:00:00', '2024-06-26 00:59:59'], [60100, 'Season 6 Spirit Siphon Ticket', 'https://127.0.0.1/static/tickets12.png', '2022-01-29 15:00:00', '2024-11-20 00:59:59'], [70010, '2nd Anniversary Ticket', 'https://127.0.0.1/static/tickets13.png', '2022-01-29 15:00:00', '2025-02-26 00:59:59'], [70020, 'Premium 2nd Anniversary Ticket', 'https://127.0.0.1/static/tickets14.png', '2022-01-29 15:00:00', '2025-03-28 05:59:59'], [70100, 'Season 7 Spirit Siphon Ticket', 'https://127.0.0.1/static/tickets15.png', '2022-01-29 15:00:00', '2025-02-26 00:59:59'], [80010, 'S8 Step-Up BONUS Ticket', 'https://127.0.0.1/static/tickets16.png', '2022-01-29 15:00:00', '2025-07-30 00:59:59'], [80100, 'Season 8 Spirit Siphon Ticket', 'https://127.0.0.1/static/tickets17.png', '2022-01-29 15:00:00', '2025-08-04 05:59:59'], [90100, 'Season 9 Spirit Siphon Ticket', 'https://127.0.0.1/static/tickets18.png', '2022-01-29 15:00:00', '2099-12-31 14:59:59']]]
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        
#025348/api/leaderboard/get_leaderboard_model
@ignore_kwargs
def getLeaderboardModel(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #low priority
                          # XXX(dmr): figure out wtf to do with static
            [0, 2, 2, [[[['375136190421202904', 1, 'moto_puarMAX', 'モトちゃん', 4, 0, 41775, '3166291872982515232', 0, 0], ['963080250628000833', 2, 'SURVIVOR', 'rabbity-circle67', 1, 0, 33625, '3036399418636827374', 0, 0], ['740769260111005546', 3, 'CLS-ILUMINAL', 'saain_8170', 3, 0, 33360, '76561199235324734', 0, 0], ['718483220202044149', 4, 'Glitch', 'Glitch', 3, 0, 31165, '76561198359742349', 0, 0], ['979817221015013610', 5, 'Bubbles', 'Bubbles UvU', 2, 0, 29465, '2535430209865880', 0, 0], ['019082200219155514', 6, 'SURVIVOR', 'kyneugh33', 1, 0, 25700, '7812435748251006551', 0, 0], ['281010221028090426', 7, 'SURVIVOR', 'GamePlayer9315', 1, 0, 24945, '4859849250656599714', 0, 0], ['733823240707085250', 8, 'snorlax', 'dun_culvert2', 1, 0, 24745, '1733956198815569177', 0, 0], ['369760210211095610', 9, 'OKUDA', 'pristine_space55', 1, 0, 23855, '4177853203040228955', 0, 0], ['839607200205115709', 10, 'SURVIVOR', 'Campanella4946', 1, 0, 23525, '3343986644585987375', 0, 0]], 0, 9, 'https://127.0.0.1/static/leaderboard1.png', '', [0, 0, '', 0]], [[['979817221015013610', 1, 'Bubbles', 'Bubbles UvU', 2, 0, 7839, '2535430209865880', 0, 0], ['333057221207212237', 2, 'karabin', 'DHI', 4, 0, 6304, '13152535997968064030', 0, 0], ['309059200726061450', 3, 'WD', 'tyughbxcfgsefcxv', 3, 0, 5273, '76561198356596425', 0, 0], ['412414200305055920', 4, 'Burning_T', 'Burning_TDKR', 1, 0, 4791, '1746732581343647040', 0, 0], ['848140240908024428', 5, 'fufu', 'NinjaElock', 1, 0, 4692, '125421662267087017', 0, 0], ['445965251214195541', 6, 'danblic', 'Danblic', 3, 0, 4690, '76561198809334985', 0, 0], ['846029211223111454', 7, 'Chiki', 'Chiki-Chiki-FE', 1, 0, 4516, '2757208850353179861', 0, 0], ['685217251114105828', 8, 'oreo', 'taigason', 1, 0, 4280, '5116504691443127365', 0, 0], ['700995200211051711', 9, 'Schneire11', 'scere-capone', 1, 0, 4272, '6653664829893048860', 0, 0], ['733823240707085250', 10, 'snorlax', 'dun_culvert2', 1, 0, 4263, '1733956198815569177', 0, 0]], 1, 9, 'https://127.0.0.1/static/leaderboard2.png', '', [0, 0, '', 0]]]]
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        
#025348/api/user/update_avatar #client posts a MASSIVE fucking data dump, investigate, no way its text
@ignore_kwargs
def updateAvatar(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #investigate
            [0]
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        
#025348/api/commonpurchase/tokusho
@ignore_kwargs
def tokusho(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            }, #JP only call which is in english for some reason
            [0, "This notification based on Japan's Act on Specified Commercial Transactions (Act No. 57 of 1976) is intended for customers residing in Japan.\n\nThe terms and conditions of this service are described below.\n\n-Distributor\nBANDAI NAMCO Entertainment Inc.\n5-37-8 Shiba, Minato-ku, Tokyo, Japan 108-0014\n\n-Representative\nCEO Nao Udagawa\n\n-Contact\nBANDAI NAMCO Entertainment Support Center\nhttps://bnfaq.channel.or.jp/inquiry/2761\nReception Hours: 10:00 am - 5:00 pm (Mon. - Fri. excluding national and company holidays)\nIf you would like to receive our telephone number, please contact us from the URL.\nPlease make sure to include the game title in question in your e-mail.\n\n-Product Pricing\nThe sales prices of products are displayed on each piece of content.\n\n-Payment Methods\nPayment can be made via items exclusive to this service or by other methods specified separately.\n\n-Payment Timing\nPayment must be made when purchasing a product (content).\n\n-Delivery Period\nPurchased content will be provided immediately after the payment process is completed.\n\n-Returns and Cancellations\nReturn or cancellation requests cannot be accepted due to the nature of the product.\n\n-Errors\nIn the event of service errors, we will fix the error or replace your purchased products (content).\n\n-System Requirements\nSystem requirements to use this service are the same as for the game software that contains this service. Please see our product page from the URL below for the software system requirements:\n\nhttps://www.bandainamcoent.co.jp/\n\n-Qualified Invoice Issuer Registration Number\nT7010701019273\n\n-Consumption tax rate for this service\n10%\n\nThis service requires internet access. Please note that costs required for internet communication must be assumed by the customer.\n"]
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        
#survivor training

#025348/api/transball/unlock_spattack
#[{'titleCd': '025348', 'userId': '289193220923131928', 'session': '69ca769a80161', 'platform': 3, 'version': '09.01'}, [[[5, 3120001]]]]
@ignore_kwargs
def unlockSpattack(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        currentDate2 = timezone.now().strftime("%Y-%m-%d %H:%M:%S") #kinda gay that its a different format here
        countSession = getSession()
        
        #get IDs
        unpacked = msgpack.unpackb(request.body, raw=False)
        requestUserID = unpacked[0]['userId']
        
        requestCharacterID = unpacked[1][0][0][0]
        requestSpattackID = unpacked[1][0][0][1]
        
        #user character list
        userObj = PatrollerUser.objects.get(userID=requestUserID)
        characterList = userObj.userCharacters
        updatedCharacterList = characterList
        
        #prepare index by counting all character ids
        characterIndex = [x[0] for x in characterList[1]] #Example [1, 2, 3, 4]
        
        requestedCharacterArray = [x for x in characterList[1] if x[0] == requestCharacterID]
        #exmp result: [5, "2022-10-14 09:10:00", [[1, "2022-10-14 09:10:00"]], [[1, "2022-10-14 20:34:35"], [2, "2022-10-14 09:10:00"], [3, "2023-11-02 10:02:23"]], [[3120000, "2022-11-15 21:33:16"], [3120002, "2024-05-06 16:58:30"], [3130900, "2022-10-14 09:10:00"], [3200000, "2022-10-22 19:37:29"]], [[30510, "2022-10-14 20:34:35"], [150170, "2022-11-15 21:35:31"], [150180, "2022-10-16 13:13:25"]]]
        
        #update database
        appendingData = [requestSpattackID, currentDate2] #[3120001, "2069-11-15 21:33:16"]

        updatedCharacterList[1][characterIndex.index(requestCharacterID)][4].append(appendingData)
        
        userObj.userCharacters = updatedCharacterList
        userObj.save()
        
        #response
        responseData = [0, [], 696969] #TODO: last is spirit
        for x in characterIndex:
            appendData = [x, []]
            for i in updatedCharacterList[1][characterIndex.index(x)][4]:
                appendData[1].append(i[0])
                
            responseData[1].append(appendData)
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            },
            responseData
        ]
        
        #[{'result': 0, 'date': '2026/03/30 13:12:12', 'version': '09.01', 'flag': '0', 'session': '69ca76ac05c49'}, [0, [[1, [3030600, 3101600, 3101601, 3200000, 3200003, 3200005, 3200009, 3200010, 3230000]], [2, [3200000, 3200001, 3200400, 3201200, 3240001]], [3, [3200000, 3200009, 3200400, 3201200]], [4, [3100100, 3200400, 3200800, 3210100, 3300100]], [5, [3120000, 3120002, 3130900, 3200000, 3120001]], [6, [3030000, 3130900, 3200000, 3200400, 3300200]], [7, [3100000, 3200300, 3200400]], [8, [3010100, 3100300, 3100301, 3200100, 3200400, 3201000]], [9, [3030400, 3100400, 3130900, 3200400, 3300500]], [10, [3110000, 3120300]], [11, [3101500, 3130901, 3300600]], [12, [3120003, 3120004, 3130901]], [13, [3130900, 3200000, 3200008, 3200800]], [14, [3101400, 3200400]], [15, [3200500, 3300700]], [17, [3200012, 3200013, 3300900]], [19, [3101100, 3120200, 3130400, 3130700]], [20, [3120800, 3130100, 3200000, 3220000]], [21, [3120100, 3121000, 3200000, 3200009]], [25, [3020000, 3200400]], [26, [3100700, 3130900, 3200400]], [27, [3040100, 3130900, 3200000, 3200009]], [28, [3101000, 3130900, 3200400, 3301000]], [30, [3200011, 3200400]], [31, [3030200, 3030300, 3130900, 3200400]], [32, [3101200, 3200000, 3200400]], [34, [3020200, 3110200, 3120600, 3220200]]], 398964]]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
        
#025348/api/skill/training
#1: [{'titleCd': '025348', 'userId': '289193220923131928', 'session': '69ca76ba532c6', 'platform': 3, 'version': '09.01'}, [[[130930, 1]]]]
#2: [{'titleCd': '025348', 'userId': '289193220923131928', 'session': '69ca76c6efdb0', 'platform': 3, 'version': '09.01'}, [[[132520, 20]]]]
@ignore_kwargs
def skillTraining(request):
    if request.method == 'POST':
        #generic response data
        currentdate = getServerDate()
        countSession = getSession()
        
        
        respondingData = [{
            'result': 0,
            'date': currentdate,
            'version': '09.01',
            'flag': '0',
            'session': countSession,
            },
            [0]
        ]
        
        packedData = msgpack.packb(respondingData)
        
        return HttpResponse(packedData)
        
#1: [{'result': 0, 'date': '2026/03/30 13:12:39', 'version': '09.01', 'flag': '0', 'session': '69ca76c6efdb0'}, [0, [[130930, 1, 1]], 347964]]
#2: [{'result': 0, 'date': '2026/03/30 13:13:00', 'version': '09.01', 'flag': '0', 'session': '69ca76dcbc719'}, [0, [[132520, 20, 1]], 307864]]
