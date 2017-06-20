#!/usr/bin/python3
# coding=utf-8

import pyaudio
import wave

from Services.OmdbService import OmdbService
from TTS_and_STT import text_to_speech, speech_to_text
from watson_developer_cloud import SpeechToTextV1, TextToSpeechV1
import os

from gateway.OmdbGateway import OmdbGateway

CHUNK = 1024
FORMAT = pyaudio.paInt16  # paInt8
CHANNELS = 2
RATE = 44100  # sample rate
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "pedido_usuario.wav"

omdb_gateway = OmdbGateway()
omdb_service = OmdbService(omdb_gateway=omdb_gateway)

stt = SpeechToTextV1(username='6f01e8bb-2faa-42a6-bec3-c1e236337b05', password='wRfZa13pn5Ke')
tts = TextToSpeechV1(username='823bf474-b3a1-454c-9daa-f39f1fe7fba8', password='UgSusuE0f3PZ')


def record():
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

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def resolver_pedido(pedido):
    actors = omdb_service.actors(movie='inception')
    print("hola")
    if (pedido[1] == "actores"):
        actors = omdb_service.actors(movie='Fargo')
        print("hola")
    elif (pedido[1] == "duración" or pedido[1] == "duracion"):
        pass
    elif (pedido[1] == "genero" or pedido[1] == "género"):
        pass


def transformar_pedido(pedido):
    return pedido["results"][0]["alternatives"][0]["transcript"]


def main():
    fin = False
    while (not fin):
        text_to_speech("pregunta_maquina.wav", "Diga lo que desea buscar", rate_change="+0%", f0mean_change="+0%")
        os.system("play pregunta_maquina.wav")
        record()
        pedido_usuario = speech_to_text("pedido_usuario.wav".encode('utf-8'))
        pedido_usuario = transformar_pedido(pedido_usuario)

        respuesta_pedido = resolver_pedido(pedido_usuario)


        #
        # text_to_speech("respuesta_pedido.wav", respuesta_pedido, rate_change="+0%", f0mean_change="+0%")
        # os.system("play respuesta_pedido.wav")


main()
