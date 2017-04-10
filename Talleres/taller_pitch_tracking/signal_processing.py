#!/usr/bin/env python
# coding=utf-8
from __future__ import division
import numpy as np


def data_between(t0, tf, data, sample_rate):
    signal = data[int(t0 * sample_rate): int(tf * sample_rate)]
    times = (np.arange(len(signal)) / sample_rate) + t0
    return (times, signal)


def sin(sampleRate=44100.0, duration=1.0, freq=440.0):
    return np.array([np.sin(2 * np.pi * freq * i / sampleRate) for i in range(int(duration * sampleRate))])


def rms(x):
    return np.sqrt(x.dot(x) / x.size)
