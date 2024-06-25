from tuner import Tuner
from Assets import chords
import tkinter as tk
import pygame as py
import numpy as np
import pyperclip
import time

### Initialize ###
py.init()

### Chord Input
chord_input = input("Chord Name: ")

# Run condition
running = True

### Screen (Object) ###
screen = py.display.set_mode((600, 400))

### Title and Logo ###
py.display.set_caption("Elden Guitar Calibration")
icon = py.image.load("Assets/guitar.png")
py.display.set_icon(icon)

### Clock ###
clock = py.time.Clock()

# Colors #
white = (255, 255, 255)
black = (0, 0, 0)
lblue = (0, 255, 255)
blue = (0, 0, 255)
tan = (200, 180, 140)
green = (4,128,4)
red = (255, 155, 155)

# Render Text
title_font = py.font.SysFont("ariel", 35)
title = "Calibration"
title_disp = title_font.render(title, True, black)

chord_text = "Creating a profile for: "
input_text = chord_input
input_disp = title_font.render(input_text, True, blue)
chord_disp = title_font.render(chord_text, True, black)

small_font = py.font.SysFont("ariel", 14)

match_title = "Closest Match:"
match_title_disp = title_font.render(match_title, True, black)

similarity_title = "Similarity:"
similarity_title_disp = title_font.render(similarity_title, True, black)

# Vars
calibration_start = 0
calibrating = False
calibrated = False

# Tuner/calibrator
T = Tuner(44100, 10, 500)

# dicts for comparison
known_chords = chords.chords

### Function to compare audio to known chords ###
def match_chroma(chroma):
    similarities = {}
    for chord, template in known_chords.items():
        similarities[chord] = np.dot(chroma, template)
        # print(similarities[chord])
        
    return max(similarities.items(), key=lambda item: item[1])
    
### Function for similarity rating
def match_score(chroma):
    similarities = {}
    for chord, template in known_chords.items():
        similarities[chord] = np.dot(chroma, template)
        
    return max(similarities)
        
def sample():
    chroma = T.sample()
    
    return chroma
    
chroma = None

while running:
    
    screen.fill(tan)
    
    ### Draw Instructions
    screen.blit(title_disp, (220, 30))
    
    ### User Input ###
    for event in py.event.get():
        # Closing Window #
        if event.type == py.QUIT:
            running = False
            
        if event.type == py.KEYDOWN:
                # Start Calibration
                if event.key == py.K_SPACE:
                    calibration_start = time.time()
                    calibrating = True
                    
    ### Calibration text ###
    screen.blit(chord_disp, (165, 70))
    screen.blit(input_disp, (245, 110))
    
    # CD
    cd_text = ""
    result_text = ""
    elapsed = time.time() - calibration_start
    
    if (calibrating):
        if (elapsed < 1):
            cd_text = "3"
            py.draw.rect(screen, red, (260, 145, 34, 45), 0, 2)
        elif (elapsed < 2):
            cd_text = "2"
            py.draw.rect(screen, red, (260, 145, 34, 45), 0, 2)
        elif (elapsed < 3):
            cd_text = "1"
            py.draw.rect(screen, red, (260, 145, 34, 45), 0, 2)
        elif (elapsed < 3.1):
            cd_text = "Go!"
            py.draw.rect(screen, green, (260, 145, 65, 45), 0, 2)
        else:
            chroma = sample()
            print(chroma)
            calibrating = False
            calibrated = True
            
            ### Format out
            formatted_chroma = f'"{chord_input}" : {list(chroma)}'
            print(formatted_chroma)
            pyperclip.copy(formatted_chroma)    
            
    if calibrated:
        result_text = "Done"
    
    
    cd_font = py.font.SysFont("ariel", 35)
    cd_disp = cd_font.render(cd_text, True, black)
    result_disp = cd_font.render(result_text, True, black)
    screen.blit(cd_disp, (270, 155))
    screen.blit(result_disp, (260, 155))
    
    if calibrated:
        # chroma_text = f"{list(chroma)}"
        # chroma_disp = small_font.render(chroma_text, True, black)
        # screen.blit(chroma_disp, (10, 200))
        
        
        screen.blit(match_title_disp, (50, 250))
        match_text = (match_chroma(chroma))[0]
        match_disp = title_font.render(match_text, True, green)
        screen.blit(match_disp, (230, 250))
        
        screen.blit(similarity_title_disp, (50, 290))
        similarity_text = str((match_chroma(chroma))[1])
        similarity_disp = title_font.render(similarity_text, True, red)
        screen.blit(similarity_disp, (185, 290))
        

    ### Update Screen ###
    clock.tick(20)
    py.display.update()