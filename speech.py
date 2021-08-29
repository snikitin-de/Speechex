import speech_recognition as speech_recog


def speech_to_text(audio):
    recog = speech_recog.Recognizer()

    with speech_recog.WavFile(audio) as source:
        audio = recog.record(source)

        try:
            recognized_text = recog.recognize_google(audio, language='ru-RU')
        except speech_recog.UnknownValueError as e:
            return "I can't transform this audio!"

    return recognized_text
