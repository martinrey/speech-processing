import os

from sdh.utils import record_new
from spoken_dialog_system.AutomaticSpeechRecognition import AutomaticSpeechRecognition

asr = AutomaticSpeechRecognition()


class Paso(object):
    def __init__(self, path_a_audio_de_mensaje_inicial, secciones, path_a_audio_de_mensaje_erroneo, datos_extra=None):
        self.debe_seguir_repitiendo = True
        self.path_a_audio_de_mensaje_inicial = path_a_audio_de_mensaje_inicial
        self.path_a_audio_de_mensaje_erroneo = path_a_audio_de_mensaje_erroneo
        self.secciones = secciones or []
        self.respuesta = None

        if datos_extra is None:
            datos_extra = {}

        self.datos_extra = datos_extra

    def comenzar(self):
        while self.debe_seguir_repitiendo:
            self.reproducir_mensaje_inicial()
            self.grabar_respuesta()
            self.reconocer_respuesta()
            print(self.respuesta)
            for seccion in self.secciones:
                if seccion.puede_procesar(self.respuesta):
                    seccion(sistema_de_dialogo=self).ejecutar()
                    break
            else:
                if self.path_a_audio_de_mensaje_erroneo:
                    os.system("play " + self.path_a_audio_de_mensaje_erroneo)

        return self.respuesta

    def finalizar(self):
        self.debe_seguir_repitiendo = False

    def reproducir_mensaje_inicial(self):
        if self.path_a_audio_de_mensaje_inicial:
            os.system("play " + self.path_a_audio_de_mensaje_inicial)

    def grabar_respuesta(self):
        record_new("respuesta.wav")

    def reconocer_respuesta(self):
        alternatives = asr.recognize(audio_file_name="respuesta.wav")
        self.respuesta = alternatives[0].transcript.lower()