import PySimpleGUI as sg
import numpy as np
import time
import random
import pygame
import keyboard


noticed_flag = False

layout = [[sg.Button('Play Sound', key='-play-sound-')]]
font = (16)
window = sg.Window('Sound Test', layout, size=(800, 250), font=font,
    element_justification='c')    

pygame.init()


def signal_noticed():
    global noticed_flag
    noticed_flag = True
    print("Signal Noticed!")

# Callback function when "-" key is pressed, showing signal noticed by user
keyboard.add_hotkey('-', signal_noticed)

volume = 0.001
notification_sound = pygame.mixer.Sound("assets/mixkit-interface-hint-notification-911.wav")
# def play_sound():
#     global noticed_flag, volume
#     if noticed_flag == False:
#         notification_sound.set_volume(volume)
#         channel = notification_sound.play()
        
        
#         # https://stackoverflow.com/questions/11691452/in-pygame-or-even-in-python-in-general-how-would-i-create-a-loop-that-keeps-e
#         # while channel.get_busy():
#         #     continue
#         time.sleep(2)   # wait for 2 seconds
#         print("Sound played at volume %.2f" % (volume))

#         volume = volume + 0.05  # update volume
#         play_sound()
#     print("Playing stopped.")
#     noticed_flag = False

def play_sound():
    global noticed_flag, volume
    while noticed_flag == False:
        notification_sound.set_volume(volume)
        notification_sound.play()
        print("Sound played at volume %.3f" % (volume))
        time.sleep(2)   # wait for 2 seconds

        volume = np.clip(volume + 0.001, 0, 1)  # update volume
        continue
    print("Playing stopped.")
    volume = 0.001
    noticed_flag = False





if __name__ == "__main__":
    while True:
        

        
        # The Event Loop
        event, values = window.read() 
        

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





