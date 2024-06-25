import pyaudio
import numpy as np
import librosa
import time

class Tuner():
    
    def __init__(self, bit_rate, buffer_limit, frames_per_buffer) -> None:
        # Init vars
        self.bit_rate = bit_rate
        self.frames_per_buffer = frames_per_buffer
        self.buffer_limit = buffer_limit
        
        
        # # Frame arr
        # self.frames = []

        # # Buffer count to limit recording time
        # self.buffers = 0
                
    ### Samples the audio from microphone and stores it in buffers ###
    def sample(self):
        
        # Init mic
        self.p = pyaudio.PyAudio()
        # Open channel
        self.stream = self.p.open(
            format=pyaudio.paInt16, 
            channels=1,
            rate=self.bit_rate,
            input=True,
            frames_per_buffer=self.frames_per_buffer)
        
        # Frame arr
        self.frames = []

        # Buffer count to limit recording time
        self.buffers = 0
        
        # Record
        while (self.buffers < self.buffer_limit):
                data = self.stream.read(self.frames_per_buffer)
                self.frames.append(np.frombuffer(data, dtype=np.int16))
                self.buffers += 1 
                
        # Close Stream
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        
        # Convert
        return self.convert()
        
    
    ### Converts the data collected from sample to chroma ###
    def convert(self):
        audio_data = np.hstack(self.frames)
        audio_data = audio_data.astype(np.float32)
        # Create chroma
        chroma = librosa.feature.chroma_stft(y=audio_data, sr=self.bit_rate)
        # Avg it
        avg_chroma = np.mean(chroma, axis=1)
        
        # Reset and return
        self.reset()
        return avg_chroma
        
        
    ### Resets arrays to prepare for a new sample ###
    def reset(self):
        self.buffers = 0
        self.frames = []