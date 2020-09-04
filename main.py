from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler)
from conversation.newSpyConversation import new_spy_conv
from inlineKey.submitSpyConfirm import submitSpyConfirm
from inlineKey.mySpyInlineKey import mySpyList, choseSpyInfo, operateSpy, delSpyConfirm
from job.spyJob import spyTicketJob

updater = Updater(token='1390773838:AAGsDmTCvZm-N1YDGbW-uxQJkzldPlUec_s', use_context=True)

def check(update, context):
    update.message.reply_text('user first name: {}'.format(update.message.from_user.first_name) + '\n'\
        'user last name {}'.format(update.message.from_user.last_name) + '\n'\
        'user full name: {}'.format(update.message.from_user.full_name) + '\n'\
        'user username: {}'.format(update.message.from_user.username) + '\n'\
        'user id: {}'.format(update.message.from_user.id) + '\n'\
        'message id: {}'.format(update.message.message_id) + '\n'\
        'chat id: {}'.format(update.message.chat.id) + '\n'\
        'chat type: {}'.format(update.message.chat.type) + '\n'\
        'message: {}'.format(update.message.text))

def start(update, context):
    update.message.reply_text('This bot will help you to check whether 12306 unsellable ticket is release or not.' + '\n'\
        'Enter /spy to spy a ticket' + '\n'\
        'Enter /help to get help docs')

def unknown(update, context):
    update.message.reply_text('Unknown command' + '\n\n'\
        'Enter /spy to spy a ticket' + '\n'\
        'Enter /help to get help.')

def cancel(update, context):
    update.message.reply_text('No active conversation now.')

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', start))
dispatcher.add_handler(CommandHandler('checkConversationInfo', check))
dispatcher.add_handler(new_spy_conv)
dispatcher.add_handler(CommandHandler('myspy', mySpyList))
dispatcher.add_handler(CommandHandler('cancel', cancel))
dispatcher.add_handler(CallbackQueryHandler(submitSpyConfirm, pattern='^SUBMIT_SPY'))
dispatcher.add_handler(CallbackQueryHandler(choseSpyInfo, pattern='^SPY_TICKET'))
dispatcher.add_handler(CallbackQueryHandler(operateSpy, pattern='^OPERATE_SPY'))
dispatcher.add_handler(CallbackQueryHandler(delSpyConfirm, pattern='^DELETE_SPY'))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))

jobs = updater.job_queue
spyTicketJob = jobs.run_repeating(spyTicketJob, interval=1, first=0)

updater.start_polling()
updater.idle()