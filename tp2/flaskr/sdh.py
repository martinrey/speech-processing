#!/usr/bin/python3
# coding=utf-8

from sdh.secciones.seccion_finalizar import SeccionFinalizar
from sdh.secciones.seccion_informacion import SeccionInformacion
from sdh.secciones.seccion_reserva import SeccionReserva
from sdh.paso.paso import Paso

if __name__ == '__main__':
    Paso(path_a_audio_de_mensaje_inicial="sounds/pregunta_maquina_inicial.wav",
         path_a_audio_de_mensaje_erroneo="sounds/error_seleccion_de_servicio.wav",
         secciones=[SeccionReserva, SeccionInformacion, SeccionFinalizar]).comenzar()
