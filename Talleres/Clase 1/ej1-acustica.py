#!/usr/bin/python
# coding=utf-8

import numpy as np
import matplotlib.pyplot as pyplot
import scipy.io.wavfile


# Definimos una función senoidal simple.
def ondasimple(punto):
    return punto_en_la_onda(amplitud=1.0, frecuencia=500.0, fase=0.0, punto=punto)


def punto_en_la_onda(amplitud, frecuencia, fase, punto):
    return amplitud * np.sin(2 * np.pi * frecuencia * punto + fase)


def generar_rango_de_sampleo(cantidad_de_puntos, frecuencia_de_sampleo):
    return np.arange(cantidad_de_puntos) / frecuencia_de_sampleo


def generar_onda_a_partir_de(amplitud, frecuencia, fase, rango_de_sampleo):
    onda = []
    for punto in rango_de_sampleo:
        onda.append(punto_en_la_onda(amplitud, frecuencia, fase, punto))
    return np.array(onda)


def generar_nota(frecuencia, rango_de_sampleo):
    amplitud = 1.0
    fase = 0.0
    return generar_onda_a_partir_de(amplitud, frecuencia, fase, rango_de_sampleo)


def graficar_onda(rango_de_sampleo, onda, nombre_archivo='mionda.png'):
    pyplot.clf()
    pyplot.plot(rango_de_sampleo[0:100], onda[0:100])
    pyplot.savefig(nombre_archivo)


def guardar_onda_como_wav(onda, nombre_de_archivo='mionda.wav'):
    wavdata = np.array(onda * 10000.0, dtype=np.int16)
    scipy.io.wavfile.write(nombre_de_archivo, 16000, wavdata)


# Generamos 16000 puntos a 16kHz.
CANTIDAD_DE_PUNTOS = 16000.0
FRECUENCIA_DE_SAMPLEO = 16000.0

rango_de_sampleo = generar_rango_de_sampleo(CANTIDAD_DE_PUNTOS, FRECUENCIA_DE_SAMPLEO)
nota = generar_nota(261.63, rango_de_sampleo)
graficar_onda(rango_de_sampleo, nota, 'do.png')
guardar_onda_como_wav(nota, 'do.wav')

nota = generar_nota(293.66, rango_de_sampleo)
graficar_onda(rango_de_sampleo, nota, 're.png')
guardar_onda_como_wav(nota, 're.wav')

nota = generar_nota(329.63, rango_de_sampleo)
graficar_onda(rango_de_sampleo, nota, 'mi.png')
guardar_onda_como_wav(nota, 'mi.wav')

nota = generar_nota(349.23, rango_de_sampleo)
graficar_onda(rango_de_sampleo, nota, 'fa.png')
guardar_onda_como_wav(nota, 'fa.wav')

nota = generar_nota(392.00, rango_de_sampleo)
graficar_onda(rango_de_sampleo, nota, 'sol.png')
guardar_onda_como_wav(nota, 'sol.wav')

nota = generar_nota(440.0, rango_de_sampleo)
graficar_onda(rango_de_sampleo, nota, 'la.png')
guardar_onda_como_wav(nota, 'la.wav')

nota = generar_nota(493.88, rango_de_sampleo)
graficar_onda(rango_de_sampleo, nota, 'si.png')
guardar_onda_como_wav(nota, 'si.wav')


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
