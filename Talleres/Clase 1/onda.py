#!/usr/bin/python
# coding=utf-8

import numpy as np
import matplotlib.pyplot as pyplot
import scipy.io.wavfile
import pylab

class funcionSenoidal(object):
    def __init__(self, amplitud, frecuencia, fase):
        self.amplitud = amplitud
        self.frecuencia = frecuencia
        self.fase = fase

    def evaluar(self, punto):
        return self.amplitud * np.sin(2 * np.pi * self.frecuencia * punto + self.fase)


class funcionCuadrada(object):
    def __init__(self, amplitud, frecuencia, fase):
        self.amplitud = amplitud
        self.frecuencia = frecuencia
        self.fase = fase

    def evaluar(self, punto):
        valor_funcion = np.sin(2 * np.pi * self.frecuencia * punto + self.fase)
        if valor_funcion > 0:
            return self.amplitud
        elif valor_funcion == 0:
            return 0
        else:
            return -self.amplitud


class funcionRandom(object):
    def evaluar(self, punto):
        return np.random.uniform(-1, 1)


class funcionCompuesta(object):
    def __init__(self, lista_de_funciones):
        self.lista_de_funciones = lista_de_funciones
    
    def evaluar(self, punto):
        punto_compuesto = 0
        for funcion in self.lista_de_funciones:
            punto_compuesto += funcion.evaluar(punto)
        return punto_compuesto

class generadorDeOnda(object):
    def __init__(self, funcion, rango_de_sampleo):
        self.funcion = funcion
        self.rango_de_sampleo = rango_de_sampleo

    def get_rango_de_sampleo(self):
        return self.rango_de_sampleo

    def generar(self):
        onda = []
        for punto in rango_de_sampleo:
            onda.append(self.funcion.evaluar(punto))
        return np.array(onda)

class graficadorDeOnda(object):
    def graficar_onda(self, generador_de_onda, path, nombre_de_archivo):
        pyplot.clf()
        pyplot.plot(generador_de_onda.get_rango_de_sampleo()[0:100], generador_de_onda.generar()[0:100])
        pyplot.savefig(path + nombre_de_archivo)

    def graficar_espectograma(self, generador_de_onda, path, nombre_de_archivo):
        pyplot.clf()
        #Estaria bueno que el generador de onda tenga el rango de sampleo
        sgram = pylab.specgram(generador_de_onda.generar(), Fs=16000.0)
        pyplot.savefig(path + nombre_de_archivo)



def generar_rango_de_sampleo(cantidad_de_puntos, frecuencia_de_sampleo):
    return np.arange(cantidad_de_puntos) / frecuencia_de_sampleo

def guardar_onda_como_wav(generador_de_nota, nombre_de_archivo='mionda.wav'):
    wavdata = np.array(generador_de_nota.generar() * 10000.0, dtype=np.int16)
    scipy.io.wavfile.write(nombre_de_archivo, 16000, wavdata)


# Generamos 16000 puntos a 16kHz.
CANTIDAD_DE_PUNTOS = 16000.0
FRECUENCIA_DE_SAMPLEO = 16000.0

do = funcionSenoidal(amplitud=1, frecuencia=261.63, fase=0)
#re = funcionSenoidal(amplitud=1, frecuencia=293.66, fase=0)
#mi = funcionSenoidal(amplitud=1, frecuencia=329.63, fase=0)
#fa = funcionSenoidal(amplitud=1, frecuencia=349.23, fase=0)
#sol = funcionSenoidal(amplitud=1, frecuencia=392.00, fase=0)
#la = funcionSenoidal(amplitud=1, frecuencia=440.0, fase=0)
#si = funcionSenoidal(amplitud=1, frecuencia=493.88, fase=0)

rango_de_sampleo = generar_rango_de_sampleo(CANTIDAD_DE_PUNTOS, FRECUENCIA_DE_SAMPLEO)

generador_do = generadorDeOnda(do, rango_de_sampleo)
#generador_re = generadorDeOnda(re, rango_de_sampleo)
#generador_mi = generadorDeOnda(mi, rango_de_sampleo)
#generador_fa = generadorDeOnda(fa, rango_de_sampleo)
#generador_sol = generadorDeOnda(sol, rango_de_sampleo)
#generador_la = generadorDeOnda(la, rango_de_sampleo)
#generador_si = generadorDeOnda(si, rango_de_sampleo)

graficador = graficadorDeOnda()

#graficador.graficar_onda(generador_do, "", "do.png")
#graficador.graficar_onda(generador_re, "", "re.png")
#graficador.graficar_onda(generador_mi, "", "mi.png")
#graficador.graficar_onda(generador_fa, "", "fa.png")
#graficador.graficar_onda(generador_sol, "", "sol.png")
#graficador.graficar_onda(generador_la, "", "la.png")
#graficador.graficar_onda(generador_si, "", "si.png")

# Ejercicios:
#
# 1. Generar un archivo wav para cada nota musical Do, Re, Mi,
#    Fa, Sol, La, Si. Consultar las frecuencias en
#    http://www.phy.mtu.edu/~suits/notefreqs.html
#    Tomar como referencia La = 440Hz.

#guardar_onda_como_wav(generador_do, 'do.wav')
#guardar_onda_como_wav(generador_re, 're.wav')
#guardar_onda_como_wav(generador_mi, 'mi.wav')
#guardar_onda_como_wav(generador_fa, 'fa.wav')
#guardar_onda_como_wav(generador_sol, 'sol.wav')
#guardar_onda_como_wav(generador_la, 'la.wav')
#guardar_onda_como_wav(generador_si, 'si.wav'

# 2. Buscar la frecuencia más aguda y más grave que pueden percibir.
#
# 3. Percepcion relativa. Escuchar la diferencia entre dos tonos graves
#    separados por 100Hz (ej: 200 y 300Hz) y dos tonos agudos separados
#    también por 100Hz (ej: 1200 y 1300Hz).



# 4. Crear una onda cuadrada a 500 Hz, modificando ondasimple(t) de modo
#    que devuelva solamente 1 o -1. Generar un wav y comparar con una
#    senoidal de la misma frecuencia.

#funcion_cuadrada = funcionCuadrada(amplitud=1, frecuencia=500, fase=0)
#funcion_senoidal = funcionSenoidal(amplitud=1, frecuencia=500, fase=0)
#generador_cuadrada = generadorDeOnda(funcion_cuadrada, rango_de_sampleo)
#generador_senoidal = generadorDeOnda(funcion_senoidal, rango_de_sampleo)

#graficador.graficar_onda(generador_cuadrada, "", "cuadrada.png")
#graficador.graficar_onda(generador_senoidal, "", "senoidal.png")
#guardar_onda_como_wav(generador_cuadrada, 'cuadrada.wav')
#guardar_onda_como_wav(generador_senoidal, 'senoidal.wav')


# 5. Repetir el punto anterior para 100Hz y para 1000Hz. ¿En algún caso
#    suenan parecidas las ondas senoidales y cuadradas? (Más allá de las
#    diferencias de volumen).

#funcion_cuadrada = funcionCuadrada(amplitud=1, frecuencia=100, fase=0)
#funcion_senoidal = funcionSenoidal(amplitud=1, frecuencia=100, fase=0)
#generador_cuadrada = generadorDeOnda(funcion_cuadrada, rango_de_sampleo)
#generador_senoidal = generadorDeOnda(funcion_senoidal, rango_de_sampleo)

#graficador.graficar_onda(generador_cuadrada, "", "cuadrada.png")
#graficador.graficar_onda(generador_senoidal, "", "senoidal.png")
#guardar_onda_como_wav(generador_cuadrada, 'cuadrada.wav')
#guardar_onda_como_wav(generador_senoidal, 'senoidal.wav')

# 6. Crear una onda de ruido blanco y mostrar su espectrograma.
#    Ayuda: Usar 'random.uniform(-1, 1)' del módulo random.

ruido_blanco = funcionRandom()
#generador_random = generadorDeOnda(ruido_blanco, rango_de_sampleo)

# 7. Crear una senoidal simple y combinarla con ruido blanco. Mostrar su
#    espectrograma.

funcion_compuesta = funcionCompuesta(lista_de_funciones=[do, ruido_blanco])
generador_compuesto = generadorDeOnda(funcion_compuesta, rango_de_sampleo)
graficador.graficar_espectograma(generador_compuesto, "", "espectograma.png")

# 8. Crear una senoidal simple con frecuencia ascendente y mostrar su
#    espectrograma.

# que es con frecuencia ascendente?

# 9. Combinar dos senoidales con frecuencias 1000 y 100Hz con distintas
#    fases (ej: 0 y pi), y comparar las formas de onda. ¿Tiene algún efecto
#    perceptual el cambio de fase?

senoidal_1000 = funcionSenoidal(amplitud=1, frecuencia=1000, fase=90)
senoidal_100 = funcionSenoidal(amplitud=1, frecuencia=100, fase=0)
funcion_compuesta_seno_100_1000 = funcionCompuesta(lista_de_funciones=[senoidal_100, senoidal_1000])
generador_compuesto_100_1000 = generadorDeOnda(funcion_compuesta_seno_100_1000, rango_de_sampleo)
graficador.graficar_onda(generador_compuesto_100_1000, "", "compuesto_100_1000.png")
 
# 10. Crear dos senoidales simples con la misma frecuencia pero distintas
#    fases, de modo que al combinarlas se anulen.
#    http://en.wikipedia.org/wiki/Active_noise_control
senoidal_1 = funcionSenoidal(amplitud=1, frecuencia=180, fase=0)
senoidal_2 = funcionSenoidal(amplitud=1, frecuencia=180, fase=3.14)
funcion_compuesta_seno_1_2 = funcionCompuesta(lista_de_funciones=[senoidal_1, senoidal_2])
generador_compuesto_1_2 = generadorDeOnda(funcion_compuesta_seno_1_2, rango_de_sampleo)
graficador.graficar_onda(generador_compuesto_1_2, "", "compuesto_1_2.png")

