import sounddevice as sd
import soundfile as sf


def record_new(filename):
    samplerate = 16000  # Hertz
    duration = 5  # seconds

    print("* recording")
    mydata = sd.rec(int(samplerate * duration), samplerate=samplerate,
                    channels=1, blocking=True)
    print("* done recording")
    sf.write(filename, mydata, samplerate)