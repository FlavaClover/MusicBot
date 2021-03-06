import os
import signal

import telegram.error
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup
from mutagen.mp3 import MP3
from musicfunctions import get_random_music, get_current_music, get_music_by_genre


keyboard = [['Найти песню'], ['Найти по жанру']]


def start_command(update: Update, _: CallbackContext):
    update.effective_chat.send_message(text='Привет!', reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


def send_audio(update: Update, music_name: str):
    update.effective_chat.send_audio(
        audio=open(music_name, 'rb'),
        duration=int(MP3(music_name).info.length)
    )


def send_random_audio_command(update: Update, _: CallbackContext):
    name = get_random_music(full_path=True)
    print(name)
    send_audio(update, name)


def get_current_music_command(update: Update, _: CallbackContext):
    message = update.effective_message.text
    result = get_current_music(message, full_path=True)
    if result is None:
        update.effective_chat.send_message(text='Такой песни нет')
    else:
        send_audio(update, result)
    return ConversationHandler.END


def get_music_by_genre_command(update: Update, _: CallbackContext):
    message = update.effective_message.text
    get_music = get_music_by_genre(message, full_path=True)
    if len(get_music) == 0:
        update.effective_chat.send_message(text='Песен с таким жанром нет')
    else:
        for i in get_music:
            send_audio(update, i)
    return ConversationHandler.END


def current_music_command(update: Update, _: CallbackContext):
    update.effective_chat.send_message(text='Отправь название песни')
    return 1


def music_by_genre_command(update: Update, _: CallbackContext):
    update.effective_chat.send_message(text='Отправь название жанра')
    return 2


def send_error(update: Update, _: CallbackContext):
    raise telegram.error.NetworkError("Hello i am test error")


def unknown_command_handler(update: Update, _: CallbackContext):
    update.effective_chat.send_message(text='Такой комманды нет')


def error_handler(update: Update, context: CallbackContext):
    error = context.error
    print(error)
    if isinstance(error, telegram.error.NetworkError):
        os.kill(os.getpid(), signal.SIGINT)


def main(token: str) -> None:
    updater = Updater(token=token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('send_random_audio', send_random_audio_command))
    dispatcher.add_handler(CommandHandler('test_err', send_error))
    dispatcher.add_error_handler(error_handler)

    get_current_music_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Найти песню'), current_music_command)],
        states={
            1: [MessageHandler(Filters.text, get_current_music_command)],
        },
        fallbacks=[]
    )
    get_music_by_genre_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Найти по жанру'), music_by_genre_command)],
        states={
            2: [MessageHandler(Filters.text, get_music_by_genre_command)]
        },
        fallbacks=[]
    )

    dispatcher.add_handler(get_current_music_handler)
    dispatcher.add_handler(get_music_by_genre_handler)
    dispatcher.add_handler(MessageHandler(Filters.regex('/.*'), unknown_command_handler))

    print(updater.bot.get_me())
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    with open('token.txt', 'r') as t:
        m = t.read()

    main(m)
