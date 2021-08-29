import os

from pydub import AudioSegment


def convert_ogg_to_wav(filepath, file):
    with open(filepath + '.ogg', 'wb') as new_file:
        new_file.write(file)

        sound = AudioSegment.from_ogg(filepath + '.ogg')
        sound.export(filepath + '.wav', format="wav")


def delete_audio_file(filepath):
    os.remove(filepath)
