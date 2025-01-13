from vosk import Model, KaldiRecognizer
import wave

# Cesta k českému modelu
model_path = "/opt/vosk-models/vosk-models"
model = Model(model_path)

# Načtení zvukového souboru
audio_file = "test_16k.wav"
wf = wave.open(audio_file, "rb")

# Ujisti se, že zvuk má správnou vzorkovací frekvenci
if wf.getframerate() != 16000:
    raise ValueError("Zvukový soubor musí mít frekvenci 16kHz")

# Inicializace rozpoznávače
rec = KaldiRecognizer(model, wf.getframerate())

# Rozpoznávání řeči
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())

# Výsledky
print(rec.FinalResult())
