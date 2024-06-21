import pyaudio
import numpy as np
import librosa
import time

# INIT pyaudio
p = pyaudio.PyAudio()

### Mic ###

stream = p.open(
    format=pyaudio.paInt16, 
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=1024)

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

# Get chroma?
chroma = librosa.feature.chroma_stft(y=audio_data, sr=44100)
avg_chroma = np.mean(chroma, axis=1)

print(avg_chroma)