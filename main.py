from telegram.ext import Updater, CallbackContext, CommandHandler
from telegram import Update
from mutagen.mp3 import MP3
from musicfunctions import get_random_music


def start_command(update: Update, _: CallbackContext):
    update.effective_chat.send_message(text='Привет!')


def send_random_audio_command(update: Update, _: CallbackContext):
    update.effective_chat.send_audio(
        audio=open(get_random_music(full_path=True), 'rb'),
        duration=int(MP3(get_random_music(full_path=True)).info.length)
    )


def main(token: str) -> None:
    updater = Updater(token=token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('send_random_audio', send_random_audio_command))

    print(updater.bot.get_me())
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    with open('token.txt', 'r') as t:
        m = t.read()

    main(m)

