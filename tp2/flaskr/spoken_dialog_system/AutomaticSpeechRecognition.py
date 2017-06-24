import io
from google.cloud import speech


class AutomaticSpeechRecognition(object):
    def recognize(self, audio_file_name):
        speech_client = speech.Client()
        file_name = audio_file_name

        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            sample = speech_client.sample(
                content,
                source_uri=None,
                encoding='LINEAR16',
                sample_rate_hertz=16000)

        alternatives = sample.recognize('es-AR')
        return alternatives
