from calibration import Calibrator
import tkinter as tk
import pygame as py
import time

### Initialize ###
py.init()

### Chord Input
chord_input = input("Chord Name: ")

# Run condition
running = True

### Screen (Object) ###
screen = py.display.set_mode((600, 250))

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

# Vars
calibration_start = 0
calibrating = False
calibrated = False

# Calibrator
C = Calibrator()

while running:
    
    screen.fill(tan)
    
    ### Draw Instructions
    title = "Calibration"
    title_font = py.font.SysFont("ariel", 35)
    title_disp = title_font.render(title, True, black)
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
    chord_text = "Creating a profile for "
    input_text = chord_input
    chord_font = py.font.SysFont("ariel", 35)
    input_disp = chord_font.render(input_text, True, blue)
    chord_disp = chord_font.render(chord_text, True, black)
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
            C.calibrate(chord_input)
            calibrating = False
            calibrated = True
            
    if calibrated:
        result_text = "Done"
    
    
    
    cd_font = py.font.SysFont("ariel", 35)
    cd_disp = cd_font.render(cd_text, True, black)
    result_disp = cd_font.render(result_text, True, black)
    screen.blit(cd_disp, (270, 155))
    screen.blit(result_disp, (260, 155))
        
    ### Update Screen ###
    clock.tick(20)
    py.display.update()