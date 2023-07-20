import os
import main
from faster_whisper import WhisperModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

# Set whisper options
model = WhisperModel(os.environ.get('WHISPER_MODEL'),
                     device=os.environ.get('WHISPER_DEVICE'),
                     compute_type=os.environ.get('WHISPER_COMPUTE_TYPE'))


# Transcribe audio
def transcribe_audio(audio_path):
    transcripted_text = ""

    try:
        # Transcribe audio
        segments, info = model.transcribe(audio_path, beam_size=int(os.environ.get('WHISPER_BEAM_SIZE')))

        if info.language_probability > 0.7:
            transcripted_text = ''.join([segment.text for segment in segments]).strip()
    except (Exception,) as e:
        main.logger.exception(e)
    finally:
        return transcripted_text
