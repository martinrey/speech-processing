#!/usr/bin/python
# -*- coding: latin-1 -*-

import numpy as np

def ondasimple(t, f):
  return np.sin(2 * np.pi * f * t)


# Generamos 16000 puntos a 16kHz.
ts = np.arange(16000.0) / 16000.0


# Armamos una onda senoidal discretizada con f=1000Hz.
mionda1 = []
for t in ts:
  mionda1.append(ondasimple(t, 1000))
mionda1 = np.array(mionda1)


# Armamos una onda senoidal discretizada con f=100Hz.
mionda2 = []
for t in ts:
  mionda2.append(ondasimple(t, 100))
mionda2 = np.array(mionda2)


# Combinamos ambas ondas periódicas simples, para
# formar una onda periódica compuesta.
mionda = mionda1 + mionda2


# Graficamos la onda.
import matplotlib.pyplot as pyplot
pyplot.clf()
pyplot.plot(ts[0:500], mionda[0:500])
pyplot.savefig('mionda.png')


# La guardamos como wav.
import scipy.io.wavfile
wavdata = np.array(mionda * 10000.0, dtype=np.int16)
scipy.io.wavfile.write('mionda.wav', 16000, wavdata)


# Mostramos su espectrograma.
import pylab
pyplot.clf()
sgram = pylab.specgram(mionda, Fs=16000.0)
pyplot.savefig('espectrograma.png')


# Ejercicios:
#
# 1. Crear una onda de ruido blanco y mostrar su espectrograma.
#    Ayuda: Usar 'random.uniform(-1, 1)' del módulo random.
#
# 2. Crear una senoidal simple y combinarla con ruido blanco. Mostrar su
#    espectrograma.
#
# 3. Crear una senoidal simple con frecuencia ascendente y mostrar su
#    espectrograma.
#
# 4. Combinar dos senoidales con frecuencias 1000 y 100Hz con distintas
#    fases (ej: 0 y pi), y comparar las formas de onda. ¿Tiene algún efecto
#    perceptual el cambio de fase?
# 
# 5. Crear dos senoidales simples con la misma frecuencia pero distintas
#    fases, de modo que al combinarlas se anulen.
#    http://en.wikipedia.org/wiki/Active_noise_control

