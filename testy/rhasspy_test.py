from vosk import Model, KaldiRecognizer
import wave

# Nastavení modelu
model = Model("/home/oldbot/.config/rhasspy/profiles/cs/vosk")
rec = KaldiRecognizer(model, 16000)

# Načtení zvukového souboru
with wave.open("test.wav", "rb") as wf:
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            print(rec.Result())
        else:
            print(rec.PartialResult())
