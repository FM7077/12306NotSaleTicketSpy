import pymongo
from bson.objectid import ObjectId

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient['12306Spy']
mycol = mydb['spyTicket']

def getSpyInfoObj(objectId):
    spyInfo = mycol.find_one({'_id': ObjectId(objectId)})
    return spyInfo

def getSpyInfoText(objectId):
    spyInfo = mycol.find_one({'_id': ObjectId(objectId)})
    text = 'Spy info:\n'\
            'Departure station: ' + spyInfo['depStation'] + '\n'\
            'Destination station: ' + spyInfo['desStation'] + '\n'\
            'Depart date: ' + spyInfo['date'] + '\n'\
            'Train no: ' + spyInfo['tno'] + '\n'\
            'Status: ' + spyInfo['status'] + '\n'\
            'Sent?: ' + str(spyInfo['isSent'])
    return text
