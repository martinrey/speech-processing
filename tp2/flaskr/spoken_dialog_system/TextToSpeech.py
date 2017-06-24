from watson_developer_cloud import TextToSpeechV1


class TextToSpeech(object):
    # Síntesis del texto 'text', especificando cambios en tasa de habla y f0, ambos en
    # porcentaje respecto del default del sistema. El resultado se guarda en 'filename'.
    # Es posible que el wav generado tenga mal el header, lo cual se arregla con:
    # sox -r 22050 filename.wav tmp.wav && mv tmp.wav filename.wav
    def speak(self, filename, text, rate_change="+0%", f0mean_change="+0%"):
        tts = TextToSpeechV1(username='823bf474-b3a1-454c-9daa-f39f1fe7fba8', password='UgSusuE0f3PZ')
        ssml_text = '<prosody rate="%s" pitch="%s"> %s </prosody>' % (rate_change, f0mean_change, text)
        with open(filename, 'wb') as audio_file:
            audio_file.write(tts.synthesize(ssml_text,
                                            accept='audio/wav',
                                            voice="es-US_SofiaVoice"))
            audio_file.close()
