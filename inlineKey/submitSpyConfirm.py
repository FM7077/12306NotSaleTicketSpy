from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
import sys
sys.path.append('..')
from utils.getStations import getStationInfo
import pymongo
from datetime import datetime

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient['12306Spy']
mycol = mydb['spyTicket']

def chooseTrainNo(update, context):
    keyboard = [[InlineKeyboardButton("Yes", callback_data='SUBMIT_SPY_CONFIRM'),\
        InlineKeyboardButton("No", callback_data='SUBMIT_SPY_CANCEL')]]
    markup = InlineKeyboardMarkup(keyboard)
    text = update.message.text
    context.user_data['tno'] = text
    update.message.reply_text('Spy info:\n'\
        'Departure station: ' + context.user_data['depStation'] + '\n'\
        'Destination station: ' + context.user_data['desStation'] + '\n'\
        'Departure date: ' + context.user_data['date'] + '\n'\
        'Train no: ' + context.user_data['tno'] + '\n'\
        'Are you sure to spy this train?' + '\n', reply_markup=markup)
    return ConversationHandler.END

def submitSpyConfirm(update, context):
    query = update.callback_query
    chatId = query.message.chat.id
    query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    selectedValue = query.data
    query.answer()
    userId = context.user_data['userId']
    depStation = context.user_data['depStation']
    desStation = context.user_data['desStation']
    date = context.user_data['date']
    tno = context.user_data['tno']
    depTeleCode = getStationInfo(depStation)['teleCode']
    desTeleCode = getStationInfo(desStation)['teleCode']
    if(selectedValue == 'SUBMIT_SPY_CONFIRM'):
        query.edit_message_text('Spy info:\n'\
            'Departure station: ' + context.user_data['depStation'] + '\n'\
            'Destination station: ' + context.user_data['desStation'] + '\n'\
            'Depart date: ' + context.user_data['date'] + '\n'\
            'Train no: ' + context.user_data['tno'])
        query.message.reply_text('Spy page: ' + 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=' 
            + depStation + ',' 
            + depTeleCode + '&ts='
            + desStation + ','
            + desTeleCode + '&date='
            + date + '&flag=N,N,Y')
        try:
            mycol.insert_one({
                'chatId': chatId,
                'userId': userId,
                'depStation': depStation,
                'depTeleCode': depTeleCode,
                'desStation': desStation,
                'desTeleCode': desTeleCode,
                'date': date,
                'tno': tno,
                'status': 'new',
                'isSent': False,
                'lastUpdateTime': datetime.now()
            })
            query.message.reply_text('Spy submitted')
        except:
            query.message.reply_text('Fail to submit spy, please try again.')
    elif(selectedValue == 'SUBMIT_SPY_CANCEL'):
        query.edit_message_text('Cancel submit spy')
