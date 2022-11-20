import os
import telebot
import speech_recognition
from dotenv import load_dotenv


# Load environment variables
load_dotenv('.env')

# Set bot options
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))


@bot.message_handler(commands=['start'])
def send_echo(message):
    bot.send_message(message.chat.id,
                     'Hi! I will help you to transcribe audio, video messages and video notes into text. Let\'s go!')


@bot.message_handler(content_types=['voice', 'video_note'])
def transcribe_message_auto(message):
    bot.reply_to(message, "[...]")

    audio_path = os.path.join(root_dir, f'audio\\message_{message.date}_{message.id}.ogg')

    # Get file id
    if message.content_type == 'voice':
        file_info = bot.get_file(message.voice.file_id)
    else:
        file_info = bot.get_file(message.video_note.file_id)

    # Download file
    try:
        downloaded_file = bot.download_file(file_info.file_path)

        with open(audio_path, 'wb') as audio_file:
            audio_file.write(downloaded_file)
    except Exception:
        bot.edit_message_text(chat_id=message.chat.id,
                              text="An error occurred while downloading an audio file.",
                              message_id=message.id + 1)

    # Detect the spoken language
    language = speech_recognition.detect_language(audio_path)
    # Transcribe audio
    message_text = speech_recognition.transcribe_audio(audio_path, language)

    if message_text == "":
        message_text = "No words recognized."

    bot.edit_message_text(chat_id=message.chat.id,
                          text=message_text,
                          message_id=message.id + 1)

    os.remove(audio_path)


if __name__ == '__main__':
    audio_path = f'{root_dir}\\audio'

    if not os.path.exists(audio_path):
        os.mkdir(audio_path)

    bot.polling(none_stop=True)
