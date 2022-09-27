import os

from pydub import AudioSegment


def convert_ogg_to_wav(filepath):
    sound = AudioSegment.from_ogg(filepath + '.ogg')
    sound.export(filepath + '.wav', format="wav")


def delete_audio_file(filepath):
    os.remove(filepath)
