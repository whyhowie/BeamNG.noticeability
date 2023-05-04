import PySimpleGUI as sg
import numpy as np
import time
import random
import pygame
import keyboard


pygame.init()

j = pygame.joystick.Joystick(0)
j.init()

try:
    while True:
        time.sleep(0.2)
        events = pygame.event.get()
        for event in events:
            print(event)

except KeyboardInterrupt:
    print("EXITING NOW")
    j.quit()
    pygame.quit()





