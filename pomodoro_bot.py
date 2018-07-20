import os
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

updater = Updater(token="561331830:AAHhFS7djySz2NB0JasXv7sVto8OCCKAExA")
dispatcher = updater.dispatcher

logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hola, soy el robot pomodoro de Rocio"
    )

def bot_help(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="""
            Usa /set para dar los segundos
            Usa /unset para desactivar
        """
    )

def alarm(bot, job):
    bot.send_message(job.context, text='Beep! Esta es tu alarma ')

def set_timer(bot, update, args, job_queue, chat_data):
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            update.message.reply_text(
                'No tengo a Doc cerca!'
            )
            return
        identi = str(args[0])
        job = job_queue.run_once(alarm, due, context=chat_id)
        chat_data['job'] = job
        update.message.reply_text('Has activado la alarma, el tiempo corre')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set seconds')

def unset_timer(bot, update, chat_data):
    if 'job' not in chat_data:
        update.message.reply_text('Hey, no has activado la alarma')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Mejor,que me da palo')

def error(bot, update, error):
    logger.warning(
        'Update "%s" caused error "%s"',
        update,
        error,
    )

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', bot_help))
dispatcher.add_handler(CommandHandler(
    'set',
    set_timer,
    pass_args=True,
    pass_job_queue=True,
    pass_chat_data=True,
))
dispatcher.add_handler(CommandHandler(
    'unset',
    unset_timer,
    pass_chat_data=True,
))
dispatcher.add_error_handler(error)

updater.start_polling()
updater.idle()
