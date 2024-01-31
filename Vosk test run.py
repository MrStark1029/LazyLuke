#vosk

from vosk import Model, KaldiRecognizer
import pyaudio
import json

model = Model( "C:/Users/Mr. Anurag/Desktop/LLUKE/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)

cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()


while True:
    data = stream.read(4096)
    #if len(data)==0:
       # break

    if rec.AcceptWaveform(data):
        name = ''
        res = rec.Result()

        for i in range(14,5000):
            if res[i] == '"':
                break
            else:
                name = name + res[i]
                i = i+1
        print(name)





