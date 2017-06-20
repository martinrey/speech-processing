#!/usr/bin/python3
# coding=utf-8

import pyaudio
import wave
from collections import deque
from TTS_and_STT import text_to_speech, speech_to_text
from watson_developer_cloud import SpeechToTextV1, TextToSpeechV1
import subprocess
import copy
import os

CHUNK = 1024
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 2
RATE = 44100 #sample rate
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "pedido_usuario.wav"

stt = SpeechToTextV1(username='6f01e8bb-2faa-42a6-bec3-c1e236337b05', password='wRfZa13pn5Ke')
tts = TextToSpeechV1(username='823bf474-b3a1-454c-9daa-f39f1fe7fba8', password='UgSusuE0f3PZ')

def record():

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK) #buffer

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data) # 2 bytes(16 bits) per channel

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

def listen_for_speech(threshold=2500, num_phrases=-1):
    """
    Listens to Microphone, extracts phrases from it and sends it to
    Google's TTS service and returns response. a "phrase" is sound
    surrounded by silence (according to threshold). num_phrases controls
    how many phrases to process before finishing the listening process
    (-1 for infinite).
    """

    CHUNK = 1024  # CHUNKS of bytes to read each time from mic
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    THRESHOLD = 2500  # The threshold intensity that defines silence
                      # and noise signal (an int. lower than THRESHOLD is silence).

    SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
                       # only silence is recorded. When this time passes the
                       # recording finishes and the file is delivered.

    PREV_AUDIO = 0.5  # Previous audio (in seconds) to prepend. When noise
                      # is detected, how much of previously recorded audio is
                      # prepended. This helps to prevent chopping the beggining
                      # of the phrase.

    #Open stream
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* Listening mic. ")
    audio2send = []
    cur_data = ''  # current chunk  of audio data
    rel = RATE/CHUNK
    slid_win = deque(maxlen=SILENCE_LIMIT * rel)
    #Prepend audio from 0.5 seconds before noise was detected
    prev_audio = deque(maxlen=PREV_AUDIO * rel)
    started = False
    n = num_phrases
    response = []

    while (num_phrases == -1 or n > 0):
        cur_data = stream.read(CHUNK)
        slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
        #print slid_win[-1]
        if(sum([x > THRESHOLD for x in slid_win]) > 0):
            if(not started):
                print("Starting record of phrase")
                started = True
            audio2send.append(cur_data)
        elif (started is True):
            print("Finished")
            # The limit was reached, finish capture and deliver.
            filename = save_speech(list(prev_audio) + audio2send, p)
            # Send file to Google and get response
            # r = stt_google_wav(filename)
            # if num_phrases == -1:
            #     print "Response", r
            # else:
            #     response.append(r)
            # Remove temp file. Comment line to review.
            os.remove(filename)
            # Reset all
            started = False
            slid_win = deque(maxlen=SILENCE_LIMIT * rel)
            prev_audio = deque(maxlen=0.5 * rel)
            audio2send = []
            n -= 1
            print("Listening ...")
        else:
            prev_audio.append(cur_data)

    print("* Done recording")
    stream.close()
    p.terminate()

    return response

def resolver_pedido(pedido):
    if(pedido[1] == "actores"):
        pass
    else if(pedido[1] == "duración" or pedido[1] == "duracion"):
        pass
    else if(pedido[1] == "genero" or pedido[1] == "género"):
        pass

def transformar_pedido(pedido):
    return pedido["results"][0]["alternatives"][0]["transcript"]

def main():
    fin = False
    while(not fin):
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
