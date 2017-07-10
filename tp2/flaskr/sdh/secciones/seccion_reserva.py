import os

from TTS_and_STT import text_to_speech
from sdh.secciones.seccion import Seccion, SeccionRepetirPregunta
from sdh.paso.paso import Paso


class SeccionPreguntarPelicula(Seccion):
    def ejecutar(self):
        self.sistema_de_dialogo.finalizar()

    @classmethod
    def puede_procesar(cls, pedido_de_usuario):
        return (pedido_de_usuario == "el círculo") or (pedido_de_usuario == "la momia") or (
            pedido_de_usuario == "mi villano favorito tres") or (pedido_de_usuario == "mujer maravilla") or (
                   pedido_de_usuario == "Mi Villano Favorito 3")


class SeccionPreguntarFechas(Seccion):
    def ejecutar(self):
        self.sistema_de_dialogo.finalizar()

    @classmethod
    def puede_procesar(cls, pedido_de_usuario):
        return pedido_de_usuario in ["lunes diez de julio", "miércoles doce de julio", "jueves trece de julio",
                                     "lunes 10 de julio", "miércoles 12 de julio", "jueves 13 de julio"]


class SeccionPreguntarCines(Seccion):
    def ejecutar(self):
        self.sistema_de_dialogo.finalizar()

    @classmethod
    def puede_procesar(cls, pedido_de_usuario):
        return pedido_de_usuario in ["cinemark", "atlas", "hoyts", "joyts"]


class SeccionPreguntarHorarios(Seccion):
    def ejecutar(self):
        self.sistema_de_dialogo.finalizar()

    @classmethod
    def puede_procesar(cls, pedido_de_usuario):
        return pedido_de_usuario in ["tres y media", "cuatro y media", "diez y cuarto", "4:30", "3:30",
                                     "10 y cuarto"]


class SeccionPreguntarButacas(Seccion):
    def ejecutar(self):
        self.sistema_de_dialogo.finalizar()

    @classmethod
    def puede_procesar(cls, pedido_de_usuario):
        return pedido_de_usuario in ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez",
                                     "once", "doce", "trece", "catorce", "quince", "1", "2", "3", "4", "5", "6", "7",
                                     "8", "9", "10", "11", "12", "13", "14", "15", ]


class SeccionReserva(Seccion):
    @classmethod
    def puede_procesar(cls, pedido_de_usuario):
        return "reservar" in pedido_de_usuario or "reserva" in pedido_de_usuario

    def ejecutar(self):
        pelicula = Paso(path_a_audio_de_mensaje_inicial="sounds/pregunta_maquina_pelicula.wav",
                        secciones=[SeccionPreguntarPelicula, SeccionRepetirPregunta],
                        path_a_audio_de_mensaje_erroneo="sounds/error_pelicula_reserva.wav").comenzar()

        text_to_speech("pregunta_maquina_fechas.wav", "Las fechas disponibles para la película " + str(
            pelicula) + "son: lunes diez de julio, miércoles doce de julio, o, jueves trece de julio. Por favor elija "
                        "una o bien diga repetir",
                       rate_change="+0%", f0mean_change="+0%")

        fecha = Paso(path_a_audio_de_mensaje_inicial="pregunta_maquina_fechas.wav",
                     secciones=[SeccionPreguntarFechas, SeccionRepetirPregunta],
                     path_a_audio_de_mensaje_erroneo="sounds/error_fecha_reserva.wav").comenzar()

        text_to_speech("pregunta_maquina_cines.wav",
                       "Los cines disponibles para la película " + str(pelicula) + ", el día " + str(
                           fecha) + ", son: cinemark. joyts, y atlas. Por favor elija uno o bien diga repetir",
                       rate_change="+0%", f0mean_change="+0%")

        cines = Paso(path_a_audio_de_mensaje_inicial="pregunta_maquina_cines.wav",
                     secciones=[SeccionPreguntarCines, SeccionRepetirPregunta],
                     path_a_audio_de_mensaje_erroneo="sounds/error_cine_reserva.wav").comenzar()

        horario = Paso(path_a_audio_de_mensaje_inicial="sounds/pregunta_maquina_horarios.wav",
                       secciones=[SeccionPreguntarHorarios, SeccionRepetirPregunta],
                       path_a_audio_de_mensaje_erroneo="sounds/error_horario_reserva.wav").comenzar()

        butaca = Paso(path_a_audio_de_mensaje_inicial="sounds/pregunta_maquina_butaca.wav",
                      secciones=[SeccionPreguntarButacas, SeccionRepetirPregunta],
                      path_a_audio_de_mensaje_erroneo="sounds/error_butaca_reserva.wav").comenzar()

        text_to_speech("fin_reserva.wav", "Su reserva para la película " + str(pelicula) + ", en el cine " + str(
            cines) + ", el día " + str(fecha) + ", a las " + str(horario) + ", en la butaca número " + str(
            butaca) + ", ha sido realizada con éxito",
                       rate_change="+0%", f0mean_change="+0%")
        os.system("play fin_reserva.wav")