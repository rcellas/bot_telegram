import os
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

updater = Updater(token="aquí va token")
dispatcher = updater.dispatcher

def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hola, soy el robot de Rocio"
    )

def bot_help(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Rocio me ha pedido que te lo repita todo, todito, todo."
    )

def echo(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=update.message.text
    )

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', bot_help))
dispatcher.add_handler(MessageHandler(Filters.text, echo))

updater.start_polling()
