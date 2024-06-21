import pyaudio
import numpy as np
import librosa
import time

# INIT pyaudio
p = pyaudio.PyAudio()

# Import chord dict
# from Assets import chords
# chords = chords.chords
# print(chords["Test Chord"])

### Mic ###
stream = p.open(
    format=pyaudio.paInt16, 
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=1024)

# Input chord name
chord_name = input("Input Chord Name: ")

# CD
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)
print("Go!")
time.sleep(0.5)

# Arr to store
frames = []

# Buffer count to limit recording time
buffers = 0

try:
    while (buffers < 20):
        data = stream.read(1024)
        frames.append(np.frombuffer(data, dtype=np.int16))
        buffers += 1     
except KeyboardInterrupt:
    print("Stopped recording.")
        
    
# Close Stream
stream.stop_stream()
stream.close()
p.terminate()

# Convert to NP arr
audio_data = np.hstack(frames)
print("Done")

# Convert to float p array for librosa
audio_data = audio_data.astype(np.float32)

# Get chroma
chroma = librosa.feature.chroma_stft(y=audio_data, sr=44100)
avg_chroma = np.mean(chroma, axis=1)

print(f'"{chord_name}" : {list(avg_chroma)}')



