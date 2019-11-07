import os
import logging

from telegram.ext import Updater, CommandHandler, ConversationHandler,\
    MessageHandler, Filters

from handlers.song import SongDownload
from handlers.doc import DocDownload
from handlers.error import error_callback


formatter = '[%(asctime)s] %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=formatter,
                    datefmt='%d-%m-%Y %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def start(update, context):
    update.message.reply_text('Hey, I\'m Rowena! Type /help for commands.')


def help_me(update, context):
    help_text = 'Commands:\n'
    help_text += ' /help: to view help commands.\n'
    help_text += ' /song [title artiste]: to get me to send a '\
        'song that matches your query\n'
    help_text += ' /doc [document name]: to get me to send a doc that matches'\
        ' your query\n'
    update.message.reply_text(help_text)


def done(update, context):
    update.message.reply_text('K')
    driver = context.user_data.get('driver', '')
    if driver:
        driver.quit()
    return ConversationHandler.END


if __name__ == '__main__':

    TOKEN = os.environ.get('ROWENA_KEY')
    PORT = int(os.environ.get('PORT', '5000'))

    updater = Updater(token=TOKEN,
                      use_context=True)

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', help_me)
    dispatcher.add_handler(help_handler)

    song_handler = CommandHandler('song', SongDownload.song)
    song_conversation = ConversationHandler(
        entry_points=[song_handler],

        states={
            0: [MessageHandler(Filters.regex('^\d$'), SongDownload.choice)]
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )

    document_handler = CommandHandler('doc', DocDownload.doc)
    document_coversation = ConversationHandler(
        entry_points=[document_handler],

        states={
            0: [MessageHandler(Filters.regex('^\d$'), DocDownload.choice)]
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )

    dispatcher.add_handler(song_conversation)
    dispatcher.add_handler(document_coversation)
    dispatcher.add_error_handler(error_callback)

    updater.start_webhook(
        listen='0.0.0.0',
        port=PORT,
        url_path=TOKEN
    )
    updater.bot.set_webhook('https://rowena-ravenbot.herokuapp.com/' + TOKEN)

    updater.idle()
