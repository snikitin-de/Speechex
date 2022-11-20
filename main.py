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


# Download audio file
def download_audio_from_message(message):
    file_info = None

    # Get file id to downloading audio from message
    if message.content_type == 'voice':
        file_info = bot.get_file(message.voice.file_id)
    elif message.content_type == 'video_note':
        file_info = bot.get_file(message.video_note.file_id)
    elif message.content_type == 'video':
        file_info = bot.get_file(message.video.file_id)

    # Download audio file
    downloaded_file = bot.download_file(file_info.file_path)
    audio_path = os.path.join(root_dir, f'audio\\message_{message.date}_{message.id}.ogg')

    with open(audio_path, 'wb') as audio_file:
        audio_file.write(downloaded_file)

    return audio_path


# Transcribe message into text
def transcribe_message(message):
    # Download audio file
    audio_path = download_audio_from_message(message)
    # Detect the spoken language
    language = speech_recognition.detect_language(audio_path)
    # Transcribe audio
    message_text = speech_recognition.transcribe_audio(audio_path, language)
    # Delete audio file
    os.remove(audio_path)

    if message_text == "":
        message_text = "No words recognized."

    return message_text


@bot.message_handler(commands=['start'])
def send_welcome_message(message):
    bot.send_message(message.chat.id,
                     'Hi! I will help you to transcribe audio, video messages and video notes into text. Let\'s go!')


# Transcribe message into text automatically
@bot.message_handler(content_types=['voice', 'video_note'])
def transcribe_message_auto(message):
    bot.reply_to(message, "[...]")
    message_text = transcribe_message(message)
    bot.edit_message_text(chat_id=message.chat.id, text=message_text, message_id=message.id + 1)


# Transcribe message into text manually
@bot.message_handler(commands=['transcribe'])
def transcribe_message_manually(message):
    if message.reply_to_message is not None:
        if message.reply_to_message.content_type in ("voice", "video_note", "video"):
            bot.reply_to(message.reply_to_message, "[...]")
            message_text = transcribe_message(message.reply_to_message)
            bot.edit_message_text(chat_id=message.chat.id, text=message_text, message_id=message.id + 1)
        else:
            bot.reply_to(message.reply_to_message, "Invalid type to transcribating message.")
    else:
        bot.reply_to(message, "Invalid type to transcribating message.")


if __name__ == '__main__':
    audio_path = f'{root_dir}\\audio'

    if not os.path.exists(audio_path):
        os.mkdir(audio_path)

    bot.polling(none_stop=True)
