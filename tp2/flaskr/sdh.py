#!/usr/bin/python3
# coding=utf-8

import pyaudio
import wave
import os

from gateway.OmdbGateway import OmdbGateway
from parsers.Parser import Parser
from services.OmdbService import OmdbService
from TTS_and_STT import text_to_speech, speech_to_text
from watson_developer_cloud import SpeechToTextV1, TextToSpeechV1


CHUNK = 1024
FORMAT = pyaudio.paInt16  # paInt8
CHANNELS = 2
RATE = 44100  # sample rate
RECORD_SECONDS = 5
# WAVE_OUTPUT_FILENAME = "pedido_usuario.wav"

omdb_gateway = OmdbGateway()
omdb_service = OmdbService(omdb_gateway=omdb_gateway)

stt = SpeechToTextV1(username='6f01e8bb-2faa-42a6-bec3-c1e236337b05', password='wRfZa13pn5Ke')
tts = TextToSpeechV1(username='823bf474-b3a1-454c-9daa-f39f1fe7fba8', password='UgSusuE0f3PZ')


def record(output):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)  # buffer

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)  # 2 bytes(16 bits) per channel

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(output, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def transformar_pedido(pedido):
    return pedido["results"][0]["alternatives"][0]["transcript"]


def main():
    fin = False
    while (not fin):
        # text_to_speech("pregunta_maquina_inicial.wav", "Buenos Días, ¿Desea obtener información de una película, o bien, reservar una película?", rate_change="+0%", f0mean_change="+0%")
        os.system("play sounds/pregunta_maquina_inicial.wav")

        record("pedido_usuario_incial.wav")

        pedido_usuario = speech_to_text("pedido_usuario_incial.wav".encode('utf-8'))
        pedido_usuario = transformar_pedido(pedido_usuario)

        if("reservar" in pedido_usuario or "reserva" in pedido_usuario):
            ########### PELICULAS ###################
            # text_to_speech("pregunta_maquina_pelicula.wav", "Las películas actualmente en cartelera son: El círculo, la momia, mi villano favorito tres, mujer maravilla y el hombre araña. Por favor elija una o bien diga la palabra repetir para escuchar nuevamente las opciones",
                            # rate_change="+0%", f0mean_change="+0%")
            repetir = True
            while(repetir):
                os.system("play sounds/pregunta_maquina_pelicula.wav")
                record("pelicula.wav")
                pelicula = speech_to_text("pelicula.wav".encode('utf-8'))
                pelicula = transformar_pedido(pelicula)

                if("repetir" not in pelicula):
                    repetir = False
            ########### CINES ###################
            # text_to_speech("pregunta_maquina_cines.wav", "Listo, Los cines disponibles para la pelicula " +str(pelicula)+ " son: Cinemark caballito, joyts abasto, y vilash recoleta. Por favor elija uno o bien diga repetir",
                            # rate_change="+0%", f0mean_change="+0%")
            repetir = True

            while(repetir):
                os.system("play sounds/pregunta_maquina_cines.wav")
                record("cines.wav")
                cines = speech_to_text("cines.wav".encode('utf-8'))
                cines = transformar_pedido(cines)

                if("repetir" not in cines):
                    print("Fin cines")
                    repetir = False
            ########### HORARIOS ###################
            # text_to_speech("pregunta_maquina_horarios.wav", "Perfecto, los horarios disponibles en ese cine son: tres y media, cuatro y media, o, diez y cuarto. Elija uno o bien diga repetir",
                            # rate_change="+0%", f0mean_change="+0%")
            repetir = True

            while(repetir):
                os.system("play sounds/pregunta_maquina_horarios.wav")
                record("horario.wav")
                horario = speech_to_text("horario.wav".encode('utf-8'))
                horario = transformar_pedido(horario)

                if("repetir" not in horario):
                    print("Fin Horario")
                    repetir = False
            ########### BUTACAS ###################
            # text_to_speech("pregunta_maquina_butaca.wav", "Finalmente diga un número de butaca del uno al quince",
                            # rate_change="+0%", f0mean_change="+0%")
            os.system("play sounds/pregunta_maquina_butaca.wav")
            record("butaca.wav")
            butaca = speech_to_text("butaca.wav".encode('utf-8'))
            butaca = transformar_pedido(butaca)

            ######### FIN #######################
            text_to_speech("fin_reserva.wav", "Su reserva para la película " + str(pelicula) + " en el cine " + str(cines) + " a las " +str(horario) + " en la butaca número " +str(butaca) + " ha sido realizada con éxito",
                            rate_change="+0%", f0mean_change="+0%")
            os.system("play fin_reserva.wav")

        elif("información" in pedido_usuario):
                # text_to_speech("pregunta_maquina_informacion.wav", "¿Sobre qué película desea obtener información?", rate_change="+0%", f0mean_change="+0%")
                os.system("play sounds/pregunta_maquina_informacion.wav")

                record("pelicula_info.wav")
                pelicula = speech_to_text("pelicula_info.wav".encode('utf-8'))
                pelicula = transformar_pedido(pelicula)

                pregunta = "¿Que información desea buscar sobre la pelicula " + str(pelicula)
                text_to_speech("pregunta_maquina_tipo_info.wav", pregunta, rate_change="+0%", f0mean_change="+0%")

                os.system("play pregunta_maquina_tipo_info.wav")

                record("usuario_tipo_info.wav")
                tipo_info = speech_to_text("usuario_tipo_info.wav".encode('utf-8'))
                tipo_info = transformar_pedido(tipo_info)

                rta = Parser.parse(pelicula, tipo_info)

                text_to_speech("maquina_respuesta_consulta.wav", rta, rate_change="+0%", f0mean_change="+0%")
                os.system("play maquina_respuesta_consulta.wav")

        elif("nada" in pedido_usuario or "fin" in pedido_usuario):
            fin = True
            # text_to_speech("chau.wav", "Muchas gracias por utilizar nuestros servicios, hasta luego", rate_change="+0%", f0mean_change="+0%")
            os.system("play sounds/chau.wav")


main()
