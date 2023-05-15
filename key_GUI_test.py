import PySimpleGUI as sg
import numpy as np
import time
import random
# import pygame
import keyboard
import logitech_steering_wheel as lsw
import pygetwindow as gw

DEVICE_NUM = 0
BUTTON_NUM = 22

# pygame.init()




layout = [[sg.Button('Play Sound', key='-play-sound-')],
          [sg.Button('Check steering wheel', key='-check-sw-')],
          [sg.Input('K_i', size=(10,1), key='-k-i-')]]
font = (16)
window = sg.Window('Key GUI Test', layout, size=(800, 250), font=font,
    element_justification='c', finalize=True)   # must set finalize to True, making system wait till window loaded 


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


# pygame.joystick.init()
# joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
# print(joysticks)
# joysticks[1].init()
# j = pygame.joystick.Joystick(0)
# j.init()
# j.rumble(0.2, 0.5, 3)

def initialize_sw(device_num):
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

    if lsw.is_connected(device_num):
        print(f'connected to a steering wheel at index {device_num}')
    else:
        print('Connection failed')
        exit()

    # Must get current properties to run things
    print(lsw.get_current_controller_properties(device_num)) 

def get_sw_button_state(device_num, button_num):
    lsw.update()
    s = lsw.get_state(device_num)

    return s.rgbButtons[button_num]

def play_sound():
    print("Play sound button pressed!")

def check_steering_wheel():
    # w = gw.getActiveWindow()
    # print(gw.getActiveWindowTitle())
    # print(w)
    # initialized = lsw.initialize_with_window(True, w._hWnd)
    # # initialized = lsw.initialize(True)

    # print("SDK version is: " + str(lsw.get_sdk_version()))

    # if initialized:
    #     print('initialized successfully')
    # else:
    #     exit()

    # if lsw.is_connected(DEVICE_NUM):
    #     print(f'connected to a steering wheel at index {DEVICE_NUM}')
    # else:
    #     print('Connection failed')
    #     exit()

    # # Must get current properties to run things
    # print(lsw.get_current_controller_properties(DEVICE_NUM)) 


    for i in range(100):
        lsw.update()
        s = lsw.get_state(DEVICE_NUM)
        time.sleep(0.05)
        print(f'Steering: {s.lX}')

    lsw.play_dirt_road_effect(DEVICE_NUM, 20)
    time.sleep(2)
    lsw.stop_dirt_road_effect(DEVICE_NUM)

    # lsw.shutdown()
    
   

button_down = False
button_up = False

if __name__ == "__main__":
    
    initialize_sw(DEVICE_NUM)

    while True:
        

        # time.sleep(0.2)
        # pygame_events = pygame.event.get()
        # for event in pygame_events:
        #     print(pygame.event.event_name(event.type))
        #     if pygame.event.event_name(event.type) == 'JoyButtonUp' \
        #         and event.button == 22:
        #         print('Switch driving mode')

        # Check if button pressed (button 22 in this case)
        button_state = get_sw_button_state(DEVICE_NUM, BUTTON_NUM)
        if button_state != 0:
            button_down = True
        if (button_down == True) and (button_state == 0):
            button_up = True
            button_down = False
        if button_up == True:
            print(f'Button {BUTTON_NUM} pressed.')
            button_up = False



        # The GUI Event Loop
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

    window.close()
    lsw.shutdown()    
    # pygame.quit()

