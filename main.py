import os
import telebot
import pydub
import speech
import utils

from datetime import datetime
from dotenv import load_dotenv

load_dotenv('.env')

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))


@bot.message_handler(commands=['start', 'hi'])
def send_echo(message):
    bot.send_message(message.chat.id, 'Hi!')


@bot.message_handler(content_types=['voice'])
def echo_message(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filepath = os.path.join(root_dir, r'audio\message_' + datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
    wav_file = filepath + '.wav'

    try:
        utils.convert_ogg_to_wav(filepath, downloaded_file)
    except pydub.exceptions.CouldntDecodeError:
        bot.reply_to(message, "I can't transform this audio!")

    try:
        recognized_text = speech.speech_to_text(wav_file)

        utils.delete_audio_file(filepath + '.ogg')
        utils.delete_audio_file(wav_file)

        bot.reply_to(message, recognized_text)
    except FileNotFoundError:
        bot.reply_to(message, "I can't transform this audio!")


if __name__ == '__main__':
    audio_path = f'{root_dir}\\audio'

    if not os.path.exists(audio_path):
        os.mkdir(audio_path)

    bot.polling(none_stop=True)
