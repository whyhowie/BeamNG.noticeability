import PySimpleGUI as sg
import numpy as np
import time
import random
import pygame
import keyboard

DEVICE_NUM = 1

pygame.init()

import logitech_steering_wheel as lsw
import pygetwindow as gw


layout = [[sg.Button('Play Sound', key='-play-sound-')],
          [sg.Button('Check steering wheel', key='-check-sw-')]]
font = (16)
window = sg.Window('Sound Test', layout, size=(800, 250), font=font,
    element_justification='c') 


# ---------------- Sample ----------------------------------
# for event in pygame.event.get():  # For Loop
#         if event.type == pygame.QUIT:
#             exit_game = True
  
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RIGHT:
#                 print("You have pressed right arrow key")
#             elif event.key == pygame.K_LEFT:
#                 print("You have pressed left arrow key")
# ----------------------------------------------------------

j = pygame.joystick.Joystick(0)
j.init()




def play_sound():
    print("Play sound button pressed!")

def check_steering_wheel():
    w = gw.getActiveWindow()
    print(gw.getActiveWindowTitle())
    print(w)
    initialized = lsw.initialize_with_window(True, w._hWnd)
    # initialized = lsw.initialize(True)

    print("SDK version is: " + str(lsw.get_sdk_version()))

    if initialized:
        print('initialized successfully')
    else:
        exit()

    if lsw.is_connected(DEVICE_NUM):
        print(f'connected to a steering wheel at index {DEVICE_NUM}')
    else:
        print('Connection failed')
        exit()

    # Must get current properties to run things
    print(lsw.get_current_controller_properties(DEVICE_NUM)) 


    for i in range(20):
        lsw.update()
        s = lsw.get_state(DEVICE_NUM)
        time.sleep(0.25)
        print(s.lX)

    lsw.play_bumpy_road_effect(DEVICE_NUM, 20)
    time.sleep(2)
    lsw.stop_bumpy_road_effect(DEVICE_NUM)

    lsw.shutdown()
    
   


if __name__ == "__main__":
 

    while True:
        
        time.sleep(0.2)
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
        if event == '-check-sw-':
            print('Check steering wheel!!')
            window.perform_long_operation(check_steering_wheel, "-check-sw-done-")
        if event == '-play-sound-':
            window['-play-sound-'].update(disabled=True)
            print("Play sound")
            window.perform_long_operation(play_sound, "-sound-stopped-")
        if event == '-sound-stopped-' or event == '-check-sw-done-':
            print('All good!')
            window['-play-sound-'].update(disabled=False)
        
pygame.quit()

