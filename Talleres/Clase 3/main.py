from __future__ import division
from IPython.display import Audio, Image
import matplotlib.pyplot as plt
import pitch
import midi
import wav
import signal_processing
import visualizations

from pylab import rcParams
rcParams['figure.figsize'] = 16, 5

sample_rate = 44100
freq = 440

sinu_signal = signal_processing.sin(sampleRate = sample_rate, duration = 0.05, freq = freq)
filename = wav.save_as_wav(sinu_signal, sample_rate)

visualizations.wave(0, 0.02, sample_rate, sinu_signal)

T = (1/freq)
print("T", T)
print("T (samples)", int(T * sample_rate))

print("freq", freq)
print("sample_rate", sample_rate)
print("length signal", len(sinu_signal))

pitch_step = 0.001

pitch_times, pitch_points = pitch.track(signal=sinu_signal, step=pitch_step, sample_rate=sample_rate, method=pitch.freq_from_autocorrelation)
visualizations.pitch_track(sinu_signal, pitch_times, pitch_points, 0, 1000)