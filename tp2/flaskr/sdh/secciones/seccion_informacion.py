import os

from gateway.OmdbGateway import OmdbGateway
from parsers.Parser import Parser
from TTS_and_STT import text_to_speech
from sdh.secciones.seccion import Seccion
from sdh.paso.paso import Paso
from services.OmdbService import OmdbService

INFORMACION_DISPONIBLE = ["actores", "género", "año", "duración", "director", "idioma", "productor"]
parser = Parser()
gateway = OmdbGateway()
service = OmdbService(gateway)


def movie_not_found(json):
    if "Error" in json:
        return True
    else:
        return False


class SeccionInformacion(Seccion):
    @classmethod
    def puede_procesar(cls, pedido_de_usuario):
        return "información" in pedido_de_usuario

    def ejecutar(self):
        pelicula = Paso(path_a_audio_de_mensaje_inicial="sounds/pregunta_maquina_informacion.wav",
                        secciones=[SeccionPreguntarInfoDePelicula],
                        path_a_audio_de_mensaje_erroneo="sounds/error_pelicula_no_encontrada.wav").comenzar()

        pregunta = "¿Que información desea buscar sobre la película " + str(pelicula)
        text_to_speech("pregunta_maquina_tipo_info.wav", pregunta, rate_change="+0%", f0mean_change="+0%")

        debe_preguntar = True

        while debe_preguntar:
            tipo_info = Paso(path_a_audio_de_mensaje_inicial="pregunta_maquina_tipo_info.wav",
                             secciones=[SeccionPedirInformacionDisponible],
                             path_a_audio_de_mensaje_erroneo="sounds/error_informacion_no_encontrada.wav").comenzar()

            rta = parser.parse(pelicula, tipo_info)
            text_to_speech("maquina_respuesta_consulta.wav", rta, rate_change="+0%", f0mean_change="+0%")
            os.system("play maquina_respuesta_consulta.wav")

            respuesta = Paso(path_a_audio_de_mensaje_inicial="sounds/mas_info.wav",
                             secciones=[SeccionContinuarPidiendoInformacion],
                             path_a_audio_de_mensaje_erroneo="sounds/error_butaca_reserva.wav").comenzar()
            debe_preguntar = respuesta in ['si', 'sí']


class SeccionPedirInformacionDisponible(Seccion):
    def ejecutar(self):
        self.sistema_de_dialogo.finalizar()

    @classmethod
    def puede_procesar(cls, pedido_de_usuario):
        return pedido_de_usuario in INFORMACION_DISPONIBLE


class SeccionPreguntarInfoDePelicula(Seccion):
    def ejecutar(self):
        self.sistema_de_dialogo.finalizar()

    @classmethod
    def puede_procesar(cls, pedido_de_usuario):
        json = service.movie(pedido_de_usuario)
        return not movie_not_found(json=json)


class SeccionContinuarPidiendoInformacion(Seccion):
    def ejecutar(self):
        self.sistema_de_dialogo.finalizar()

    @classmethod
    def puede_procesar(cls, pedido_de_usuario):
        return pedido_de_usuario in ["si", "sí", "no"]
