import msgpack

from django.http import HttpResponse
from django.utils import timezone
# for sessioncounter
from django.core.cache import cache

from .models import (
    PatrollerUser,
)

def with_http_msgpack(fn):
    def wrapper(request):
        unpacked_data = msgpack.unpackb(request.body, raw=False)
        respondingData = fn(unpacked_data)
        packedData = msgpack.packb(respondingData)
        return HttpResponse(packedData)
    return wrapper

def ignore_kwargs(fn):
    def wrapper(request, **kwargs):
        return fn(request)
    return wrapper

#date
def getServerDate():
    currentdate = timezone.now().strftime("%Y/%m/%d %H:%M:%S") #not sure if D/M/Y works but Y/M/D is fine for now

    return currentdate

#account creation
def createAccount(givenID):
    startingCurrency = [0, 696969, 0, "", 0, "0"] #[TPTOTAKE??, TP, TPTOGET, '', ??, '??']
    startingMessages = [0, [[1, "localhosttesting_1", "breadbreakr test 1", "2024-01-23 17:46:11", "2050-02-22 17:46:11", 1, 3], [2, "localhosttesting_2", "breadbreakr test 2!!", "2026-01-23 17:46:11", "2069-02-22 17:46:11", 1, 3]]]
    startingRivals = [0, [[100, 1, 0, 0, [[80000, 0], [80010, 0], [80020, 0], [80030, 0]], [[180000, 0], [180010, 0], [180020, 0], [180030, 0]], [1002001, 1002005, 1003004, 1003007, 1004001, 1004002]], [200, 1, 0, 0, [[80100, 0], [80110, 0], [80120, 0], [80130, 0]], [[180100, 0], [180110, 0], [180120, 0], [180130, 0]], [2001000, 2001010, 2002000, 2003000, 2004000, 2004005]], [300, 1, 0, 0, [[80200, 0], [80210, 0], [80220, 0], [80230, 0], [80240, 0], [80250, 0]], [[180200, 0], [180210, 0], [180220, 0], [180230, 0]], [3001001, 3002000, 3002014, 3003000, 3003006, 3004000]]]]
    startingCharacters = [0, [[1, '2026-05-21 18:54:17', [[1, '2026-05-21 18:54:17']], [[4, '2026-05-21 18:54:17']], [[3200000, '2026-05-21 18:54:18']], []], [4, '2026-05-21 18:54:17', [[1, '2026-05-21 18:54:17']], [[1, '2026-05-21 18:54:17']], [[3210100, '2026-05-21 18:54:18']], []], [5, '2026-05-21 18:54:17', [[1, '2026-05-21 18:54:17']], [[2, '2026-05-21 18:54:17']], [[3130900, '2026-05-21 18:54:18']], []], [8, '2026-05-21 18:54:17', [[1, '2026-05-21 18:54:17']], [[1, '2026-05-21 18:54:17']], [], [[30810, '2026-05-21 18:54:18']]], [12, '2026-05-21 18:55:37', [[1, '2026-05-21 18:55:37']], [[1, '2026-05-21 18:55:37']], [[3130901, '2026-05-21 18:55:37']], [[131210, '2026-05-21 18:55:37']]]], [[1010, '2026-05-21 18:54:18'], [1040, '2026-05-21 18:54:18']], [[20100, 0, 0, '2026-05-21 18:54:17'], [20110, 0, 0, '2026-05-21 18:54:17'], [20200, 0, 0, '2026-05-21 18:54:17'], [30810, 0, 0, '2026-05-21 18:54:18'], [50030, 0, 0, '2026-05-21 18:54:17'], [131210, 0, 0, '2026-05-21 18:55:37']], [[10030, '2026-05-21 18:54:18'], [10040, '2026-05-21 18:54:18'], [10050, '2026-05-21 18:54:18'], [110020, '2026-05-21 18:54:18']], []]
    newUser = PatrollerUser(userID=givenID, gameCurrency=startingCurrency, messageList=startingMessages, rivalList=startingRivals, userCharacters=startingCharacters)
    newUser.save()
    return None

#session counter - not sure if this is the actual purpose or method of producing the session hexadecmial
def getSession():
    key = cache.get('sessionCounter')
    if key is not None:
        pass
    else:
        cache.set('sessionCounter', 1855130961786517)

    hexSession = hex(cache.get('sessionCounter'))[2:]
    cache.incr('sessionCounter', 1)

    return hexSession


##user ID assignment##
#Dunno how to decrypt the data the client is sending
#Just gonna take the last 50 digits of the encrypted data, take all the letters out, limit it to 19 chars, and use that.
#triple check this actually works later lol
def calculateUserID(encryptedData):

    inEncryptedData = encryptedData[-50:]
    cutEncryptedData = inEncryptedData[:20]
    calculatedUserID = ''.join(filter(str.isdigit, cutEncryptedData))

    return calculatedUserID


from django.conf import settings

env_base_path = 'LALALALALA/'
prd_base_path = 'dbtb-prd/LALALALALA/'


def env_uri():
    return '/'.join([
        'https:/',
        # os.environ.get('ENV_HOST'),
        settings.ENV_HOST,
        env_base_path,
    ])


def prd_uri():
    return '/'.join([
        'https:/',
        # os.environ.get('PRD_HOST'),
        settings.PRD_HOST,
        prd_base_path,
    ])
