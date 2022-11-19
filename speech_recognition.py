import os
import whisper
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

# Set whisper options
model = whisper.load_model(os.environ.get('WHISPER_MODEL'))


# Detect the spoken language
def detect_language(audio_path):
    try:
        # Load audio and pad/trim it to fit 30 seconds
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)

        # Make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        # Detect the spoken language
        _, probs = model.detect_language(mel)

        return max(probs, key=probs.get)
    except Exception:
        return "en"


# Transcribe audio
def transcribe_audio(audio_path, language):
    try:
        # Set whisper options
        options = dict(language=language)
        transcribe_options = dict(task="transcribe", **options)

        # Transcribe audio
        transcribed_text = model.transcribe(audio_path, **transcribe_options)["text"]

        return transcribed_text
    except Exception:
        return ""
