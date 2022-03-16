from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update
from mutagen.mp3 import MP3
from musicfunctions import get_random_music, get_current_music


def start_command(update: Update, _: CallbackContext):
    update.effective_chat.send_message(text='Привет!')


def send_audio(update: Update, music_name: str):
    update.effective_chat.send_audio(
        audio=open(music_name, 'rb'),
        duration=int(MP3(music_name).info.length)
    )


def send_random_audio_command(update: Update, _: CallbackContext):
    send_audio(update, get_random_music(full_path=True))


def get_current_music_command(update: Update, _: CallbackContext):
    message = update.effective_message.text
    send_audio(update, get_current_music(message, full_path=True))


def main(token: str) -> None:
    updater = Updater(token=token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('send_random_audio', send_random_audio_command))
    dispatcher.add_handler(MessageHandler(Filters.text, get_current_music_command))

    print(updater.bot.get_me())
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    with open('token.txt', 'r') as t:
        m = t.read()

    main(m)
