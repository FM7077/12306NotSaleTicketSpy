import sys
sys.path.append('..')
from utils.spyTicketFunction import spyTicket
from model.spyInfo import spy_info
import pymongo
from bson.objectid import ObjectId
from datetime import datetime

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient['12306Spy']
mycol = mydb['spyTicket']

def spyTicketJob(context):
    spyInfos = mycol.find({'isSent': False})
    for spyInfo in spyInfos:
        result = spyTicket(spyInfo)
        if(result['status']):
            context.bot.send_message(chat_id=spyInfo['chatId'], text='Ticket ' + result['data']['tno'] + ' is on sale\n'\
                'Remain seats:\n'\
                ' - Business seat: ' + str(result['data']['topSeat']) + '\n'\
                ' - First class seat: ' + str(result['data']['firstSeat']) + '\n'\
                ' - Second class seat: ' + str(result['data']['secondSeat']) + '\n'\
                ' - Standing ticket: ' + str(result['data']['standTicket']) + '\n'\
                ' - Business berth: ' + str(result['data']['topBerth']) + '\n'\
                ' - Soft berth: ' + str(result['data']['softBerth']) + '\n'\
                ' - Dynamic berth: ' + str(result['data']['dynaBerth']) + '\n'\
                ' - Hard berth: ' + str(result['data']['hardBerth']) + '\n')
            mycol.update_one({'_id': ObjectId(spyInfo['_id'])}, 
                {
                    '$set': {
                        'isSent': True, 
                        'status': 'onSale',
                        'lastUpdateTime': datetime.now()
                    }
                }
            )
        else:
            mycol.update_one({'_id': ObjectId(spyInfo['_id'])}, 
                {
                    '$set': {
                        'status': result['data'],
                        'lastUpdateTime': datetime.now()
                    }
                }
            )