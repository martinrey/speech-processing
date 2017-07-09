#!/usr/bin/python3
# coding=utf-8

import pyaudio
import wave
import os

from gateway.OmdbGateway import OmdbGateway
from parsers.Parser import Parser
from services.OmdbService import OmdbService
from TTS_and_STT import text_to_speech, speech_to_text, speech_to_text_EN, text_to_speech_EN
from watson_developer_cloud import SpeechToTextV1, TextToSpeechV1


import sounddevice as sd
import soundfile as sf

def record_new(filename):
    samplerate = 44100  # Hertz
    duration = 5  # seconds

    print("* recording")
    mydata = sd.rec(int(samplerate * duration), samplerate=samplerate,
                    channels=2, blocking=True)
    print("* done recording")
    sf.write(filename, mydata, samplerate)


CHUNK = 1024
FORMAT = pyaudio.paInt16  # paInt8
CHANNELS = 2
RATE = 44100  # sample rate
RECORD_SECONDS = 5
# WAVE_OUTPUT_FILENAME = "pedido_usuario.wav"

#########
parser = Parser()
gateway = OmdbGateway()
service = OmdbService(gateway)
INFORMACION_DISPONIBLE = ["actores", "género", "año", "duración", "director", "idioma", "productor"]
#########

stt = SpeechToTextV1(username='6f01e8bb-2faa-42a6-bec3-c1e236337b05', password='wRfZa13pn5Ke')
tts = TextToSpeechV1(username='823bf474-b3a1-454c-9daa-f39f1fe7fba8', password='UgSusuE0f3PZ')

#
# def record_old(output):
#     p = pyaudio.PyAudio()
#
#     stream = p.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK)  # buffer
#
#     print("* recording")
#
#     frames = []
#
#     for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#         data = stream.read(CHUNK)
#         frames.append(data)  # 2 bytes(16 bits) per channel
#
#     print("* done recording")
#
#     stream.stop_stream()
#     stream.close()
#     p.terminate()
#
#     wf = wave.open(output, 'wb')
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(p.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(b''.join(frames))
#     wf.close()

def transformar_pedido(pedido):
    return str(pedido["results"][0]["alternatives"][0]["transcript"]).strip()

# GENERALIZARLO EN UN ERROR HANDLER
def movie_not_found(json):
    if("Error" in json):
        return True
    else:
        return False


def main():
    fin = False
    #text_to_speech("pregunta_maquina_intro.wav", "Buenos días, bienvenidos al trabajo " +
                    #"práctico número dos de la materia, procesamiento del habla. En este sistema usted podrá reservar entradas de cine para una película, y también podrá obtener información de una película en particular"
                    #, rate_change="+0%", f0mean_change="+0%")
    #os.system("play sounds/pregunta_maquina_intro.wav")


    while (not fin):
        #text_to_speech("sounds/pregunta_maquina_inicial.wav", "Si desea obtener información de una película, diga información, o bien, si quiere reservar entradas de cine diga reservar. En caso de no querer nada, simplemente diga la palabra nada", rate_change="+0%", f0mean_change="+0%")
        #os.system("play sounds/pregunta_maquina_inicial.wav")

        record_new("pedido_usuario_incial.wav")

        os.system("play sounds/espera.wav")

        pedido_usuario = speech_to_text("pedido_usuario_incial.wav".encode('utf-8'))
        pedido_usuario = transformar_pedido(pedido_usuario)

        print(pedido_usuario)


        if("reservar" in pedido_usuario or "reserva" in pedido_usuario):

            ########### PELICULAS ###################
            #text_to_speech("pregunta_maquina_pelicula.wav", "Las películas actualmente en cartelera son: El círculo, la momia, mi villano favorito tres, y, mujer maravilla. Por favor elija una o bien diga la palabra repetir para escuchar nuevamente las opciones",
                             #rate_change="+0%", f0mean_change="+0%")
            repetir = True
            while(repetir):
                os.system("play sounds/pregunta_maquina_pelicula.wav")
                record_new("pelicula.wav")
                pelicula = speech_to_text("pelicula.wav".encode('utf-8'))
                pelicula = transformar_pedido(pelicula)

                print(pelicula)

                if("repetir" in pelicula):
                    repetir = True
                elif (not ((pelicula == "el círculo") or (pelicula == "la momia") or (pelicula == "mi villano favorito tres") or (pelicula == "mujer maravilla"))):
                    #text_to_speech("error_pelicula_reserva.wav", "Lo siento, no he comprendido, o la película que nombró no se encuentra en cartelera. Por favor diga el nombre exacto de alguna de las películas en cartelera",
                                     #rate_change="+0%", f0mean_change="+0%")
                    os.system("play sounds/error_pelicula_reserva.wav")
                else:
                    repetir = False


            ########### FECHAS ###################
            text_to_speech("pregunta_maquina_fechas.wav", "Las fechas disponibles para la película " +str(pelicula)+ " son: lunes diez de julio, miércoles doce de julio, o, jueves trece de julio. Por favor elija una o bien diga repetir",
                            rate_change="+0%", f0mean_change="+0%")
            repetir = True

            while(repetir):
                os.system("play pregunta_maquina_fechas.wav")
                record_new("fechas.wav")
                fecha = speech_to_text("fechas.wav".encode('utf-8'))
                fecha = transformar_pedido(fecha)

                print(fecha)

                if("repetir" in fecha):
                    repetir = True
                elif(fecha not in ["lunes diez de julio", "miércoles doce de julio", "jueves trece de julio"]):
                    #text_to_speech("error_fecha_reserva.wav", "Lo siento, no he comprendido, o la fecha que usted eligió no es correcta. Por favor diga la fecha exacta de alguna de las siguientes",
                                    #rate_change="+0%", f0mean_change="+0%")
                    os.system("play sounds/error_fecha_reserva.wav")
                else:
                    repetir = False
            ########### CINES ###################
            #
            # text_to_speech("pregunta_maquina_cines_1.wav", "Listo, ahora necesito saber en que cine desea ver la película",
            #                  rate_change="+0%", f0mean_change="+0%")
            # os.system("play pregunta_maquina_cines_1.wav")
            #
            # text_to_speech("pregunta_maquina_cines_2.wav", "Los cines disponibles para la pelicula " +str(pelicula)+ ", el día " + str(fecha) + ", son: cinemark, atlas, y dot. Por favor elija uno o bien diga repetir",
            #                  rate_change="+0%", f0mean_change="+0%")
            # repetir = True
            #
            # while(repetir):
            #     os.system("play pregunta_maquina_cines_2.wav")
            #     record_new("cines.wav")
            #     cines = speech_to_text("cines.wav".encode('utf-8'))
            #     cines = transformar_pedido(cines)
            #     print(cines)
            #     if("repetir" not in cines and cines in ["cinemark","atlas","cine mark", "dot"]):
            #         repetir = False
            #     else:
            #         text_to_speech("error_cine_reserva.wav", "Lo siento, el cine que usted eligió no es correcto. Por favor nombre alguno de las siguientes",
            #                         rate_change="+0%", f0mean_change="+0%")
            #         os.system("play error_cine_reserva.wav")

            ########### HORARIOS ###################
            #text_to_speech("pregunta_maquina_horarios.wav", "Los horarios disponibles para ese cine son: tres y media, cuatro y media, o, diez y cuarto. Elija uno, o bien diga repetir",
                            #rate_change="+0%", f0mean_change="+0%")
            repetir = True
            while(repetir):
                os.system("play sounds/pregunta_maquina_horarios.wav")
                record_new("horario.wav")
                horario = speech_to_text("horario.wav".encode('utf-8'))
                horario = transformar_pedido(horario)

                print(horario)

                if("repetir" in horario):
                    pass
                elif(horario not in ["tres y media", "cuatro y media", "diez y cuarto"]):
                    #text_to_speech("error_horario_reserva.wav", "Lo siento, el horario que usted eligó no es correcto. Por favor diga exactamente alguno de los siguientes horarios.",
                                    #rate_change="+0%", f0mean_change="+0%")
                    os.system("play sounds/error_horario_reserva.wav")
                else:
                    repetir = False

            ########### BUTACAS ###################
            #text_to_speech("pregunta_maquina_butaca.wav", "Por favor, diga un número de butaca del uno al quince",
                            #rate_change="+0%", f0mean_change="+0%")
            repetir = True
            while(repetir):
                os.system("play sounds/pregunta_maquina_butaca.wav")
                record_new("butaca.wav")
                butaca = speech_to_text("butaca.wav".encode('utf-8'))
                butaca = transformar_pedido(butaca)

                print(butaca)

                if(butaca not in ["uno","dos","tres","cuatro","cinco","seis","siete","ocho","nueve","diez","once","doce","trece","catorce","quince"]):
                        #text_to_speech("error_butaca_reserva.wav", "Lo siento, no he comprendido", rate_change="+0%", f0mean_change="+0%")
                        os.system("play sounds/error_butaca_reserva.wav")
                else:
                    repetir = False

            ######### FIN #######################
            text_to_speech("fin_reserva.wav", "Su reserva para la película " + str(pelicula) + " en el cine  el día " + str(fecha) + " a las " +str(horario) + " en la butaca número " +str(butaca) + " ha sido realizada con éxito",
                            rate_change="+0%", f0mean_change="+0%")
            os.system("play fin_reserva.wav")

        elif("información" in pedido_usuario):
                no_encontre_la_pelicula = True
                while(no_encontre_la_pelicula):
                    # text_to_speech("pregunta_maquina_informacion.wav", "¿Sobre qué película desea obtener información?", rate_change="+0%", f0mean_change="+0%")
                    os.system("play sounds/pregunta_maquina_informacion.wav")

                    record_new("pelicula_info.wav")

                    os.system("play sounds/espera.wav")

                    #pelicula = speech_to_text("pelicula_info.wav".encode('utf-8'))
                    pelicula = speech_to_text_EN("pelicula_info.wav".encode('utf-8'))

                    pelicula = transformar_pedido(pelicula)
                    print(pelicula)

                    json = service.movie(pelicula)

                    if movie_not_found(json=json):
                        text_to_speech("error_pelicula_no_encontrada.wav", "Disculpe, no pudimos encontrar la película. Por favor pruebe diciendo el título en inglés.", rate_change="+0%", f0mean_change="+0%")
                        os.system("play sounds/error_pelicula_no_encontrada.wav")
                    else:
                        no_encontre_la_pelicula = False

                quiero_mas_info = True
                while(quiero_mas_info):
                    no_encontre_informacion = True
                    while(no_encontre_informacion):
                        pregunta = "¿Que información desea buscar sobre la película " + str(pelicula)
                        text_to_speech("pregunta_maquina_tipo_info.wav", pregunta, rate_change="+0%", f0mean_change="+0%")

                        os.system("play pregunta_maquina_tipo_info.wav")

                        record_new("usuario_tipo_info.wav")
                        tipo_info = speech_to_text("usuario_tipo_info.wav".encode('utf-8'))
                        tipo_info = transformar_pedido(tipo_info)
                        print(tipo_info)

                        if tipo_info not in INFORMACION_DISPONIBLE:
                            text_to_speech("sounds/error_informacion_no_encontrada.wav", "Disculpe, no pudimos realizar el pedido. Diga alguna de las siguientes opciones. actores. género. año. duración. director. idioma, o productor.", rate_change="+0%", f0mean_change="+0%")
                            os.system("play sounds/error_informacion_no_encontrada.wav")
                            print("if")
                        else:
                            print("else")
                            no_encontre_informacion = False

                        print("antes parser")
                        rta = parser.parse(pelicula, tipo_info)
                        print("despues parser")
                        text_to_speech("maquina_respuesta_consulta.wav", rta, rate_change="+0%", f0mean_change="+0%")

                        os.system("play maquina_respuesta_consulta.wav")


                        no_entendi = True
                        while(no_entendi):
                            text_to_speech("sounds/mas_info.wav", "Si desea obtener mas información sobre la película, diga sí. En caso contrario diga, no", rate_change="+0%", f0mean_change="+0%")

                            os.system("play sounds/mas_info.wav")
                            record_new("new_info.wav")
                            new_info = speech_to_text("new_info.wav".encode('utf-8'))
                            new_info = transformar_pedido(new_info)

                            print(new_info)

                            if(new_info == "si" or new_info == "sí"):
                                no_entendi = False
                            elif(new_info == "no"):
                                no_entendi = False
                                quiero_mas_info = False
                            else:
                                os.system("play sounds/error_butaca_reserva.wav")

        elif("nada" in pedido_usuario or "fin" in pedido_usuario):
            fin = True
            # text_to_speech("chau.wav", "Muchas gracias por utilizar nuestros servicios, hasta luego", rate_change="+0%", f0mean_change="+0%")
            os.system("play sounds/chau.wav")

        else:
            #text_to_speech("error_seleccion_de_servicio.wav", "Disculpe, no entendi el comando elegido.", rate_change="+0%", f0mean_change="+0%")
            os.system("play sounds/error_seleccion_de_servicio.wav")
main()
