#!/usr/bin/env python
import wave

import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16  # paInt8
CHANNELS = 1
RATE = 16000  # sample rate
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "pedido_usuario.wav"


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


def run_quickstart():
    import io

    # Imports the Google Cloud client library
    from google.cloud import speech

    # Instantiates a client
    speech_client = speech.Client()

    # The name of the audio file to transcribe
    file_name = "pedido_usuario.wav"

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        sample = speech_client.sample(
            content,
            source_uri=None,
            encoding='LINEAR16',
            sample_rate_hertz=16000)

    # Detects speech in the audio file
    alternatives = sample.recognize('es-AR')

    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))

if __name__ == '__main__':
    #record()
    run_quickstart()
