import logging

from flask import Flask, render_template

from spoken_dialog_system.AutomaticSpeechRecognition import AutomaticSpeechRecognition
from spoken_dialog_system.TextToSpeech import TextToSpeech

app = Flask(__name__)


@app.route('/')
def hello():
    recorder_service = RecorderService()
    recorder_service.record()
    asr = AutomaticSpeechRecognition()
    tts = TextToSpeech()
    tts.speak("prueba.wav", "quiero genero fargo", rate_change="+0%", f0mean_change="+0%")

    alternatives = asr.recognize(audio_file_name="pedido_usuario.wav")
    return render_template('main.html', alternatives=alternatives)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
