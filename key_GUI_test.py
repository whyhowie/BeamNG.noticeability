import PySimpleGUI as sg
import numpy as np
import time
import random
import pygame
import keyboard


pygame.init()


layout = [[sg.Button('Play Sound', key='-play-sound-')]]
font = (16)
window = sg.Window('Sound Test', layout, size=(800, 250), font=font,
    element_justification='c') 



for event in pygame.event.get():  # For Loop
        if event.type == pygame.QUIT:
            exit_game = True
  
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                print("You have pressed right arrow key")
            elif event.key == pygame.K_LEFT:
                print("You have pressed left arrow key")


j = pygame.joystick.Joystick(0)
j.init()


    



def play_sound():
    print("Play sound button pressed!")


if __name__ == "__main__":
    while True:
        
        # time.sleep(0.2)
        pygame_events = pygame.event.get()
        for event in pygame_events:
        #     print(pygame.event.event_name(event.type))
            if pygame.event.event_name(event.type) == 'JoyButtonUp' \
                and event.button == 22:
                print('Switch driving mode')

        # The Event Loop
        event, values = window.read(timeout=100) 
        

        if event == sg.WIN_CLOSED or event == 'Exit':
            break      
        if event == '-play-sound-':
            window['-play-sound-'].update(disabled=True)
            print("Play sound")
            window.perform_long_operation(play_sound, "-sound-stopped-")
        if event == '-sound-stopped-':
            print('All good!')
            window['-play-sound-'].update(disabled=False)
        
pygame.quit()

