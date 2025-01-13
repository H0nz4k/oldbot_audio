import wave
import os
from vosk import Model, KaldiRecognizer
import pyaudio
import noisereduce as nr
import numpy as np
from scipy.io import wavfile

def record_audio(output_file, record_seconds=10, rate=16000, channels=1):
    """
    Nahraje audio a uloží ho do souboru.
    """
    chunk = 1024  # Velikost bufferu
    format = pyaudio.paInt16  # 16bit audio
    audio = pyaudio.PyAudio()

    # Inicializace nahrávání
    print("TED!! Začínám nahrávat...")
    stream = audio.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    frames = []

    # Nahrávání
    for _ in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Ukončení nahrávání
    print("Nahrávání ukončeno.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Uložení do souboru
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

def remove_noise(input_file, output_file):
    """
    Odstranění šumu ze zvukového souboru.
    """
    rate, data = wavfile.read(input_file)
    if len(data.shape) == 2:
        data = np.mean(data, axis=1)  # Převedení stereo na mono
    reduced_noise = nr.reduce_noise(y=data, sr=rate, stationary=True)
    wavfile.write(output_file, rate, reduced_noise.astype(np.int16))

def transcribe_audio(audio_file, model_path):
    """
    Převod zvuku na text pomocí Vosk.
    """
    if not os.path.exists(model_path):
        print(f"Model nebyl nalezen na cestě: {model_path}")
        return

    print("Načítám model...")
    model = Model(model_path)

    print(f"Zpracovávám soubor: {audio_file}")
    wf = wave.open(audio_file, "rb")

    if wf.getframerate() != 16000:
        raise ValueError("Zvukový soubor musí mít vzorkovací frekvenci 16kHz.")

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    result = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result += rec.Result()

    result += rec.FinalResult()
    wf.close()
    return result

if __name__ == "__main__":
    # Parametry
    audio_file = "recorded_audio.wav"
    cleaned_audio_file = "cleaned_audio.wav"
    model_path = "/opt/vosk-models/vosk-model-small-cs-0.4-rhasspy"

    # Nahraj audio
    record_audio(audio_file)

    # Odstraň šum
    print("Odstraňuji šum...")
    remove_noise(audio_file, cleaned_audio_file)

    # Převod zvuku na text
    print("Převádím zvuk na text...")
    text_output = transcribe_audio(cleaned_audio_file, model_path)

    print("\nRozpoznaný text:")
    print(text_output)
