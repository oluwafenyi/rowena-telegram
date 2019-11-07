import re

from telegram.ext import ConversationHandler
from telegram.error import TelegramError

from utils.doc import (
    present_options,
    get_documents_bookateria,
    download_choice_bookateria,
    get_documents_genesis,
    download_choice_genesis
)


class DocDownload:

    def doc(update, context):
        query = context.args
        if not query:
            return
        query_str = ' '.join(context.args)
        update.message.reply_text(f'Getting results for "{query_str}"')

        bookateria_options = get_documents_bookateria(query)
        genesis_options = get_documents_genesis(query)

        text = 'Text "Done" at anytime to end\n'\
            'Here are your options, pick one by number:\n\n'

        if bookateria_options:
            context.user_data['options'] = bookateria_options
            context.user_data['service'] = 'bookateria'
            text += present_options(bookateria_options, None)
            update.message.reply_text(text)
            return 0

        elif genesis_options:
            context.user_data['options'] = genesis_options
            context.user_data['service'] = 'genesis'
            text += present_options(None, genesis_options)
            update.message.reply_text(text)
            return 0

        update.message.reply_text('No results found')
        return ConversationHandler.END

    def choice(update, context):
        selected = update.message.text
        text = f'You have chosen {selected}. Give me a sec...'
        update.message.reply_text(text)

        service = context.user_data['service']
        options = context.user_data['options']

        try:
            choice = options[int(selected)-1]
        except IndexError:
            update.message.reply_text('Option not available.')
            return 0

        if service == 'bookateria':
            link = choice[0]['href']
            doc = download_choice_bookateria(link)
            update.message.reply_document(doc)

        elif service == 'genesis':
            td = choice.select_one('td:nth-child(3)')
            link = td.find('a', href=re.compile(r'book/.*'))['href']
            doc = download_choice_genesis(link)
            try:
                update.message.reply_document(doc)
            except TelegramError:
                update.message.reply_text('Link here:\n' + doc)

        return ConversationHandler.END
