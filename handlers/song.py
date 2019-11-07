
from telegram.ext import ConversationHandler

from utils.song import download_choice, get_results


class SongDownload:

    def song(update, context):
        new_text = ''
        query = context.args
        if not query:
            return
        query_str = ' '.join(context.args)
        update.message.reply_text(f'Getting results for "{query_str}"')

        try:
            additional_text, options, driver = get_results(query)
        except AttributeError:
            ConversationHandler.END

        text = 'Text "Done" at anytime to end\n' + additional_text
        if not additional_text:
            text = 'Could not find that song.'
            update.message.reply_text(text)
            return ConversationHandler.END

        context.user_data['options'] = options
        context.user_data['driver'] = driver

        update.message.reply_text(text)
        return 0

    def choice(update, context):
        selected = update.message.text
        text = f'You have chosen {selected}. Give me a sec...'

        update.message.reply_text(text)

        options = context.user_data['options']
        driver = context.user_data['driver']
        try:
            choice = options[int(selected)-1]
        except IndexError:
            update.message.reply_text('Option not available.')
            return 0

        song = download_choice(choice, driver)

        update.message.reply_audio(song)
        driver.quit()
        return ConversationHandler.END
