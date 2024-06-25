import pygame as py
import numpy as np
import librosa
import pyaudio
from tuner import Tuner
from Assets import chords

# Copy chord dictionary + mappings
known_chords = chords.chords
chord_mappings = chords.chord_mappings

# Create tuner object
T = Tuner(44100, 10, 500)

# Confidence threshold (Implement if doesn't work otherwise)
# confidence = 0.85

### Function to compare audio to known chords ###
def match_chroma(chroma):
    similarities = {}
    for chord, template in known_chords.items():
        similarities[chord] = np.dot(chroma, template)
        # print(similarities[chord])
        
    return max(similarities, key=similarities.get)
    
### Pygame section ###
# Initialize #
py.init()
running = True
screen = py.display.set_mode((300, 450))

# Title and Logo #
py.display.set_caption("Elden Guitar")
icon = py.image.load("Assets/guitar.png")
py.display.set_icon(icon)
big_font = py.font.SysFont("ariel", 35)
small_font =  py.font.SysFont("ariel", 28)

# Clock #
clock = py.time.Clock()

# Colors #
white = (255, 255, 255)
black = (0, 0, 0)
lblue = (0, 255, 255)
blue = (0, 0, 255)
tan = (200, 180, 140)
green = (4,128,4)
red = (255, 155, 155)

# Pre Rendered text
input_title_text = "Input Mapped:"
input_title_disp = big_font.render(input_title_text, True, black)
chord_title_text = "Chord Detected:"
chord_title_disp = big_font.render(chord_title_text, True, black)

while (running):
    
    # Background
    screen.fill(tan)
    
    ### User Input ###
    for event in py.event.get():
        # Closing Window #
        if event.type == py.QUIT:
            running = False
    
    chroma = T.sample()
    chord_detected = match_chroma(chroma)
    print(chroma)

    #### Optimize by not updating constant titles
    # Display the chord
    chord_disp = small_font.render(chord_detected, True, blue)
    screen.blit(chord_title_disp, (10, 10))
    screen.blit(chord_disp, (10, 40))
    
    # Display the respective input 
    input_text = chord_mappings[chord_detected]
    input_disp = small_font.render(input_text, True, blue)
    screen.blit(input_title_disp, (10, 80))
    screen.blit(input_disp, (10, 110))
    
    # Update Screen
    py.display.flip()