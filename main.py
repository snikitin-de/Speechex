import os
import telebot
import logging
import speech_recognition
import handlers
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] %(name)s %(levelname)s %(message)s")
logger = logging.getLogger("speechex")

# Load environment variables
load_dotenv('.env')

root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

# Set bot options
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN, exception_handler=handlers.ExceptionHandler())


# Download audio file
def download_audio_from_message(message):
    file_info = None

    # Get file id to downloading audio from message
    if message.content_type == 'voice':
        file_info = bot.get_file(message.voice.file_id)
    elif message.content_type == 'audio':
        file_info = bot.get_file(message.audio.file_id)
    elif message.content_type == 'video_note':
        file_info = bot.get_file(message.video_note.file_id)
    elif message.content_type == 'video':
        file_info = bot.get_file(message.video.file_id)

    # Download audio file
    downloaded_file = bot.download_file(file_info.file_path)
    audio_path = os.path.join(root_dir, f'audio\\message_{message.date}_{message.id}.ogg')

    try:
        with open(audio_path, 'wb') as audio_file:
            audio_file.write(downloaded_file)
    except OSError as e:
        logger.error(e)

    return audio_path


# Transcribe message into text
def transcribe_message(message):
    # Download audio file
    audio_path = download_audio_from_message(message)

    # Transcribe audio
    message_text = speech_recognition.transcribe_audio(audio_path)
    # Delete audio file
    if os.path.exists(audio_path):
        os.remove(audio_path)
    else:
        logger.error("Audio file not found")

    if message_text == "":
        message_text = "Speech in the audio file is not recognized or is absent."
        logger.info("Speech in the audio file is not recognized or is absent")

    return message_text


@bot.message_handler(commands=['start'])
def send_welcome_message(message):
    bot.send_message(message.chat.id,
                     'Hi! I will help you to transcribe audio, video messages and video notes into text. Let\'s go!')


def split_message(message, message_text):
    if len(message_text) > 4096:
        for x in range(0, len(message_text), 4096):
            if x == 0:
                bot.edit_message_text(chat_id=message.chat.id,
                                      text=message_text[x:x + 4096],
                                      message_id=message.id + 1)
            else:
                bot.send_message(chat_id=message.chat.id,
                                 text=message_text[x:x + 4096])
    else:
        bot.edit_message_text(chat_id=message.chat.id,
                              text=message_text,
                              message_id=message.id + 1)


# Transcribe message into text automatically
@bot.message_handler(content_types=['voice', 'video_note'])
def transcribe_message_auto(message):
    duration = getattr(message, message.content_type).duration
    file_size = getattr(message, message.content_type).file_size
    if duration < 900 and file_size < 20000000:  # 15 minutes and 20 MB
        bot.reply_to(message, "[...]")
        logger.info(f"Start message {message.id} processing in chat {message.chat.id}")
        message_text = transcribe_message(message)
        split_message(message, message_text)
        logger.info(f"End message {message.id} processing in chat {message.chat.id} ")
    else:
        bot.reply_to(message, "Audio in this message is big long.")
        logger.info(f"Audio with duration of {duration} seconds and size of {file_size} bytes in "
                    f"message {message.id} in chat {message.chat.id} is too big")


# Transcribe message into text manually
@bot.message_handler(commands=['transcribe'])
def transcribe_message_manually(message):
    if message.reply_to_message is not None:
        content_type = message.reply_to_message.content_type
        if content_type in ("voice", "audio", "video_note", "video"):
            duration = getattr(message.reply_to_message, content_type).duration
            file_size = getattr(message.reply_to_message, message.reply_to_message.content_type).file_size
            if duration < 900 and file_size < 20000000:  # 15 minutes and 20 MB
                bot.reply_to(message.reply_to_message, "[...]")
                logger.info(f"Start message {message.reply_to_message.id} processing in chat {message.chat.id}")
                message_text = transcribe_message(message.reply_to_message)
                split_message(message, message_text)
                logger.info(f"End message {message.reply_to_message.id} processing in chat {message.chat.id}")
            else:
                bot.reply_to(message.reply_to_message, "Audio in this message is too big.")
                logger.info(f"Audio with duration of {duration} seconds and size of {file_size} bytes in "
                            f"message {message.reply_to_message.id} in chat {message.chat.id} is too big")
        else:
            bot.reply_to(message.reply_to_message, "Incorrect message type for speech recognition.")
            logger.info(f"Incorrect message {message.reply_to_message.id} type in chat {message.chat.id} "
                        f"for speech recognition")
    else:
        bot.reply_to(message, "Incorrect message type for speech recognition.")
        logger.info(f"Incorrect message {message.id} type in chat {message.chat.id} for speech recognition")


if __name__ == '__main__':
    audio_path = f'{root_dir}\\audio'

    if not os.path.exists(audio_path):
        os.mkdir(audio_path)

    bot.infinity_polling()
