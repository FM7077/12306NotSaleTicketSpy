import sys
sys.path.append('..')
from utils.getSpyInfo import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import pymongo
from bson.objectid import ObjectId

myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient['12306Spy']
mycol = mydb['spyTicket']

def mySpyList(update, context):
    userId = update.message.from_user.id
    keyboard = spyListInlineKeyboard(userId)
    if len(keyboard) > 0:
        markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Bellow is your ticket spy', reply_markup=markup)
    else:
        update.message.reply_text('Can not find ticket spy.' + '\n'\
            'Enter /spy to spy a ticket')

def choseSpyInfo(update, context):
    query = update.callback_query
    query.answer()
    objectId = query.data.split('_')[2]
    userId = query.data.split('_')[3]
    spyInfo = getSpyInfoObj(objectId)
    text = getSpyInfoText(objectId)
    query.edit_message_text(text, reply_markup=spyInfoInlineKeyboard(objectId, spyInfo['tno'], userId))

def operateSpy(update, context):
    query = update.callback_query
    query.answer()
    action = query.data.split('_')[2]
    if(action == 'DELETE'):
        objectId = query.data.split('_')[3]
        tno = query.data.split('_')[4]
        userId = query.data.split('_')[5]
        query.edit_message_text('Are you sure to delete ' + tno + ' spy?', reply_markup=spyDelInlineKeyboard(objectId, userId))
    elif(action == 'BACK'):
        userId = int(query.data.split('_')[3])
        keyboard = spyListInlineKeyboard(userId)
        if len(keyboard) > 0:
            markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text('Bellow is your ticket spy', reply_markup=markup)
        else:
            query.edit_message_text('Can not find ticket spy.' + '\n'\
                'Enter /spy to spy a ticket')

def delSpyConfirm(update, context):
    query = update.callback_query
    query.answer()
    action = query.data.split('_')[2]
    objectId = query.data.split('_')[3]
    userId = query.data.split('_')[4]
    if(action == 'DELETE'):
        mycol.delete_one({'_id': ObjectId(objectId)})
        keyboard = spyListInlineKeyboard(int(userId))
        if len(keyboard) > 0:
            markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text('Bellow is your ticket spy', reply_markup=markup)
        else:
            query.edit_message_text('Can not find ticket spy.' + '\n'\
                'Enter /spy to spy a ticket')
    else:
        spyInfo = getSpyInfoObj(objectId)
        text = getSpyInfoText(objectId)
        query.edit_message_text(text, reply_markup=spyInfoInlineKeyboard(objectId, spyInfo['tno'], userId))

##################### inline keyboard ##########################
def spyListInlineKeyboard(userId):
    spyInfos = mycol.find({'userId': userId}).sort('isSent')
    keyboard = []
    for spyInfo in spyInfos:
        if spyInfo['isSent']: 
            emoji = '\U00002714' 
        else: 
            emoji = '\U0000231B'
        callBackData = 'SPY_TICKET_' + str(spyInfo['_id']) + '_' + str(userId)
        displayInfo = emoji + '  ' + spyInfo['tno'] + '  ' + spyInfo['depStation'] + ' -> ' + spyInfo['desStation']
        newSpyInfoButton = [InlineKeyboardButton(displayInfo, callback_data=callBackData)]
        keyboard.append(newSpyInfoButton)
    return keyboard

def spyInfoInlineKeyboard(objectId, tno, userId):
    keyboard = [[InlineKeyboardButton('Delete Spy', callback_data='OPERATE_SPY_DELETE_' + objectId + '_' + tno + '_' + userId)],
        [InlineKeyboardButton('Back to Spy list', callback_data='OPERATE_SPY_BACK_' + userId)]]
    return InlineKeyboardMarkup(keyboard)

def spyDelInlineKeyboard(objectId, userId):
    keyboard = [[InlineKeyboardButton('Yes', callback_data='DELETE_SPY_DELETE_' + objectId + '_' + userId),
        InlineKeyboardButton('No', callback_data='DELETE_SPY_CANCEL_' + objectId + '_' + userId)]]
    return InlineKeyboardMarkup(keyboard)