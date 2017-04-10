#!/usr/bin/env python
# coding=utf-8
from __future__ import division

import matplotlib.pyplot as plt
import numpy as np


def autocorr(x):
    """
    Compute the autocorrelation of the signal, based on the properties of the
    power spectral density of the signal.
    """
    xp = x - np.mean(x)
    f = np.fft.fft(xp)
    p = np.array([np.real(v)**2 + np.imag(v)**2 for v in f])
    pi = np.fft.ifft(p)
    return np.real(pi)[:x.size / 2] / np.sum(xp**2)


def freq_from_autocorr(signal, sample_rate, show_plot=False):
    corr = autocorr(signal)
    
    primer_minimo = np.argmin(corr)
    corr_cortado = corr[primer_minimo:]
    maximo = np.argmax(corr_cortado)
    frequency = 1 / (len(corr_cortado) / sample_rate)
    
    if show_plot:
        plt.plot(corr, "-r", label=u"correlación")
        plt.ylim([-2, 2])
        plt.title("correlation")
        plt.legend()
    return frequency


def freq_from_zcr(signal, sample_rate):
    no_lo_encuentra = True
    i = 0
    while no_lo_encuentra:
        p1 = signal[i]
        p2 = signal[i+1]
        
        if p1 < 0 and p2 > 0:
            no_lo_encuentra = False
        i += 1
    return 1.0 / (float(i) / sample_rate)    
       

def track(signal, step, sample_rate, method):
    times = []
    pitch_track = []
    
    tamanio_ventana = (1/(50 * 2)) * sample_rate 
    mitad_ventana = tamanio_ventana // 2
    puntos_entre_steps = int(step * sample_rate)
    
    index_punto = puntos_entre_steps - 1
    
    while index_punto < len(signal)-1:
        ventana = signal[max(index_punto - mitad_ventana, 0): min(index_punto + mitad_ventana, len(signal))]
        pitch = method(ventana, sample_rate)
        pitch_track.append(pitch)
        times.append(index_punto)
        index_punto += puntos_entre_steps
    
    return times, pitch_track


def smooth_pitch(pitch_track, window):
    # COMPLETAR
    pass
