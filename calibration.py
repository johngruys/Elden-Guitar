import pyaudio
import numpy as np
import librosa
import time
import pyperclip

class Calibrator():
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.bit_rate = 44100
        self.stream = self.p.open(
            format=pyaudio.paInt16, 
            channels=1,
            rate=self.bit_rate,
            input=True,
            frames_per_buffer=1024)
        
        # Chord name 
        self.chord_name = ""
        
        # Arr to store
        self.frames = []

        # Buffer count to limit recording time
        self.buffers = 0
        self.buffer_limit = 20
    
        
            
        
    def calibrate(self, chord_name):
        
        self.chord_name = chord_name        
        
        ### Record ###
        try:
            while (self.buffers < self.buffer_limit):
                data = self.stream.read(1024)
                self.frames.append(np.frombuffer(data, dtype=np.int16))
                self.buffers += 1     
        except KeyboardInterrupt:
            print("Stopped recording.")
            
        # Close Stream
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        # print("Done")
        self.convert()
            
            
    def reset(self):
        self.stream = self.p.open(
            format=pyaudio.paInt16, 
            channels=1,
            rate=self.bit_rate,
            input=True,
            frames_per_buffer=1024)
        
        # Reset Frames
        self.frames = []

        # Reset Buffer Count
        self.buffers = 0

    def convert(self):
        audio_data = np.hstack(self.frames)
        audio_data = audio_data.astype(np.float32)
        chroma = librosa.feature.chroma_stft(y=audio_data, sr=self.bit_rate)
        avg_chroma = np.mean(chroma, axis=1)
        
        # Print and return
        formatted_chroma = f'"{self.chord_name}" : {list(avg_chroma)}'
        print(formatted_chroma)
        pyperclip.copy(formatted_chroma)
        return avg_chroma

    
    