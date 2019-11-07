import logging

from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)


def error_callback(update, error):
    try:
        raise error
    except Unauthorized:
        logging.error('Unauthorized request made.')
    except BadRequest:
        logging.error('Bad request made.')
    except TimedOut:
        logging.error('Request Timed Out.')
    except NetworkError:
        logging.error('Network error occurred.')
    except ChatMigrated:
        logging.error('Chat id has changed.')
    except TelegramError:
        logging.error('An error has occurred.')
