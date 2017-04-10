#!/usr/bin/python
# -*- coding: latin-1 -*-

import numpy as np

# Definimos una función senoidal simple.
def ondasimple(t):
  A = 1.0    # amplitud
  f = 500.0  # frequencia
  Phi = 0.0  # fase
  return A * np.sin(2 * np.pi * f * t + Phi)


# Generamos 16000 puntos a 16kHz.
ts = np.arange(16000.0) / 16000.0


# Armamos una onda senoidal discretizada.
mionda = []
for t in ts:
  mionda.append(ondasimple(t))
mionda = np.array(mionda)


# Graficamos la onda.
import matplotlib.pyplot as pyplot
pyplot.clf()
pyplot.plot(ts[0:100], mionda[0:100])
pyplot.savefig('mionda.png')


# La guardamos como wav.
import scipy.io.wavfile
#MAL: wavdata = np.array(mionda, dtype=np.int16) * 10000
wavdata = np.array(mionda * 10000.0, dtype=np.int16)
scipy.io.wavfile.write('mionda.wav', 16000, wavdata)


# Ejercicios:
#
# 1. Generar un archivo wav para cada nota musical Do, Re, Mi,
#    Fa, Sol, La, Si. Consultar las frecuencias en
#    http://www.phy.mtu.edu/~suits/notefreqs.html
#    Tomar como referencia La = 440Hz.
#
# 2. Buscar la frecuencia más aguda y más grave que pueden percibir.
#
# 3. Percepcion relativa. Escuchar la diferencia entre dos tonos graves
#    separados por 100Hz (ej: 200 y 300Hz) y dos tonos agudos separados
#    también por 100Hz (ej: 1200 y 1300Hz).
#
# 4. Crear una onda cuadrada a 500 Hz, modificando ondasimple(t) de modo
#    que devuelva solamente 1 o -1. Generar un wav y comparar con una
#    senoidal de la misma frecuencia.
#
# 5. Repetir el punto anterior para 100Hz y para 1000Hz. ¿En algún caso
#    suenan parecidas las ondas senoidales y cuadradas? (Más allá de las
#    diferencias de volumen).

