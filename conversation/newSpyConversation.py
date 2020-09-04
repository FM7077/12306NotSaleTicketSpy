from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
from utils.getStations import getStationInfo
from inlineKey.submitSpyConfirm import chooseTrainNo
from datetime import datetime

CHOOSE_DEPARTURE, CHOOSE_DESTINATION, CHOOSE_DATE, CHOOSE_TRAIN_NO = range(4)

def newSpy(update, context):
    userId = update.message.from_user.id
    context.user_data['userId'] = userId
    update.message.reply_text('Please enter departure train station first')
    return CHOOSE_DEPARTURE

def chooseDeparture(update, context):
    text = update.message.text
    context.user_data['depStation'] = text
    if(getStationInfo(str(text)) != None):
        update.message.reply_text('The departure station is <{}>'.format(text) + '\n'\
            'Now please enter the destination station')
        return CHOOSE_DESTINATION
    else:
        update.message.reply_text('Invalid station name, please re-enter the departure station.')
        return CHOOSE_DEPARTURE

def chooseDestination(update, context):
    text = update.message.text
    context.user_data['desStation'] = text
    if text == context.user_data['depStation']:
        update.message.reply_text('Destination staion can not be the same as departure station\n' + 
            'please re-enter the destination station')
        return CHOOSE_DESTINATION
    if(getStationInfo(str(text)) != None):
        update.message.reply_text('The destination station is <{}>'.format(text) + '\n'\
            'Now please enter the departure date,' + '\n'\
            'format: YYYY-MM-dd, eg: 2020-09-29')
        return CHOOSE_DATE
    else:
        update.message.reply_text('Invalid station name, please re-enter the destination station.')
        return CHOOSE_DESTINATION

def chooseDate(update, context):
    text = update.message.text
    context.user_data['date'] = text
    try:
        datetime.strptime(text, '%Y-%m-%d').date()
    except:
        update.message.reply_text('Invalid date, please re-enter the departure date.')
        return CHOOSE_DATE
    update.message.reply_text('The departure date is <{}>'.format(text) + '\n'\
        'Now please enter the train no,' + '\n'\
        'eg: G1234')
    return CHOOSE_TRAIN_NO

def cancel(update, context):
    update.message.reply_text('Spy cancelled')
    return ConversationHandler.END

def done(update, context):
    update.message.reply_text('Somethings error occur, spy cancelled')
    return ConversationHandler.END

new_spy_conv = ConversationHandler(
    entry_points=[CommandHandler('spy', newSpy)],
    states={
        CHOOSE_DEPARTURE: [MessageHandler(Filters.text & ~Filters.command, chooseDeparture)],
        CHOOSE_DESTINATION: [MessageHandler(Filters.text & ~Filters.command, chooseDestination)],
        CHOOSE_DATE: [MessageHandler(Filters.text & ~Filters.command, chooseDate)],
        CHOOSE_TRAIN_NO: [MessageHandler(Filters.text & ~Filters.command, chooseTrainNo)]
    },
    fallbacks=[MessageHandler(Filters.regex('^Done$'), done), CommandHandler('cancel', cancel)]
)