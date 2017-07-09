#!/usr/bin/env python
# coding=utf-8

# Es necesario instalar esto: pip install --upgrade watson-developer-cloud
from watson_developer_cloud import SpeechToTextV1, TextToSpeechV1
import subprocess
import copy

# Estas credenciales se informarán por mail. Para obtener nuevas:
# 1: entrar a https://www.ibm.com/cloud-computing/bluemix/
# 2: En el dashboard ir a create apps
# 3: Hacer clic a la izquierda en Watson (en la sección 'services').
# 4: Ahora deberían verse en el listado las app "Text to Speech" y "Speech to text",
#    para cada una apretar 'create'.
# 5: Una vez creadas, acceder a las mismas desde el dashboard, hacer clic en
#    'service credentials' y después en 'view credentials'.
stt = SpeechToTextV1(username='6f01e8bb-2faa-42a6-bec3-c1e236337b05', password='wRfZa13pn5Ke')
tts = TextToSpeechV1(username='823bf474-b3a1-454c-9daa-f39f1fe7fba8', password='UgSusuE0f3PZ')


# Reconocimiento del archivo de audio 'filename'.
# 'max_alternatives' es la cantidad de hipótesis más probables a devolver.
def speech_to_text(filename, stt=stt):
  audio_file = open(filename, "rb")
  ibm_recognized = stt.recognize(audio_file,
                                 content_type="audio/wav",
                                 model="es-ES_BroadbandModel",
                                 timestamps="true",
                                 max_alternatives="1",
                                 continuous="true")
  return(ibm_recognized)

def speech_to_text_EN(filename, stt=stt):
  audio_file = open(filename, "rb")
  ibm_recognized = stt.recognize(audio_file,
                                 content_type="audio/wav",
                                 model="en-US_BroadbandModel",
                                 timestamps="true",
                                 max_alternatives="1",
                                 continuous="true")
  return(ibm_recognized)

# Síntesis del texto 'text', especificando cambios en tasa de habla y f0, ambos en
# porcentaje respecto del default del sistema. El resultado se guarda en 'filename'.
# Es posible que el wav generado tenga mal el header, lo cual se arregla con:
# sox -r 22050 filename.wav tmp.wav && mv tmp.wav filename.wav
def text_to_speech(filename, text, rate_change="+0%", f0mean_change="+0%", tts=tts):
  ssml_text = '<prosody rate="%s" pitch="%s"> %s </prosody>' % (rate_change, f0mean_change, text)
  with open(filename, 'wb') as audio_file:
    audio_file.write(tts.synthesize(ssml_text,
                                    accept='audio/wav',
                                    voice="es-US_SofiaVoice"))
    audio_file.close()

def text_to_speech_EN(filename, text, rate_change="+0%", f0mean_change="+0%", tts=tts):
  ssml_text = '<prosody rate="%s" pitch="%s"> %s </prosody>' % (rate_change, f0mean_change, text)
  with open(filename, 'wb') as audio_file:
    audio_file.write(tts.synthesize(ssml_text,
                                    accept='audio/wav',
                                    voice="en-US_LisaVoice"))
    audio_file.close()

if __name__ == "__main__":
  # Probamos la síntesis...
	text_to_speech("prueba.wav", "quiero genero fargo", rate_change="+0%", f0mean_change="+0%")

	# Y ahora probamos el reconocimiento...
	print(speech_to_text("prueba.wav"))
