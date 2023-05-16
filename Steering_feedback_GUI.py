import random
from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Electrics
import keyboard
import PySimpleGUI as sg

import logitech_steering_wheel as lsw
import pygetwindow as gw

import time

########### Steering wheel constants
SW_NUM = 0  # Device number (todo: find device number)
AV_BUTTON_NUM = 22  # Button 22 for driving mode switching
SW_READING_RANGE = 31700    # Approximate maximum reading of the steering wheel (sw_state.lX)
SW_ANGLE_RANGE = 450    # Approximate maximum turning angle of the steering wheel

########### Constants for PID controller ################################
K_P = .2 # K_p of PID controller
K_I = .3 # K_i of PID controller
K_D = .05 # K_d of PID controller

PID_MAX_FORCE = 15

sw_initialized = False #





# Run this script while the main client is open
client_log = BeamNGpy('localhost', 64256)
client_log.open(launch=False)

running_scenario = client_log.scenario.get_current()
active_vehicles = client_log.vehicles.get_current()

print('Here is a list of active vehicles:')
print(active_vehicles)


vehicle_name = ''
active_vehicle_names = list(active_vehicles.keys())

while vehicle_name not in active_vehicle_names:
    vehicle_name = input('\nWhich vehicle? ')

    if vehicle_name == '':
        vehicle_name = 'ego_vehicle'
    continue    


try:
    ego_vehicle = active_vehicles[vehicle_name]
    print('Vehicle selected!')
    ego_vehicle.connect(client_log)
    ego_vehicle.sensors.attach('electrics', Electrics()) # electrics sensor

except Exception as e:
    print(e)

data_logging = False


def toggle_data_logging():
    global data_logging
    data_logging = not data_logging
    if data_logging:
        print('Logging started!')
    else:
        print('Logging terminated.')
    




def initialize_sw(device_num):
    global sw_initialized
    w = gw.getActiveWindow()
    # print(gw.getActiveWindowTitle())
    # w = gw.getWindowsWithTitle('BeamNG.drive - 0')[0]
    print(w)
    lsw.initialize_with_window(True, w._hWnd)

    print("SDK version is: " + str(lsw.get_sdk_version()))


    if lsw.is_connected(device_num):
        print(f'connected to a steering wheel at index {device_num}')
    else:
        print('Connection failed')
        exit()

    # lsw.update()
    lsw.get_current_controller_properties(device_num)

    sw_initialized = True



def get_sw_angle(device_num):
    if sw_initialized:
        lsw.update()
        sw_state = lsw.get_state(device_num)
        # Find current physical steering wheel angle
        sw_angle = sw_state.lX / SW_READING_RANGE * SW_ANGLE_RANGE
        # print(sw_angle)
        return sw_angle


def get_sw_button_state(device_num, button_num):
    if sw_initialized:
        lsw.update()
        s = lsw.get_state(device_num)

        return s.rgbButtons[button_num]



PID_frame = sg.Frame('PID', [[sg.Input(size=(10,1), key='-k-p-', default_text=f'{K_P}')],
    [sg.Input(size=(10,1), key='-k-i-', default_text=f'{K_I}')],
    [sg.Input(size=(10,1), key='-k-d-', default_text=f'{K_D}')],
    [sg.Submit()]])

default_frame = sg.Frame('Steering Feedback', [[sg.Button('Initialize steering wheel', key='-init-sw-')],
          [sg.Button('Check steering wheel', key='-check-sw-')],
          [sg.Text('------------------------------------------------------------------\n' + 
                   '---------------------------------------------------------', key='-sw-status-')]])

layout = [[default_frame, PID_frame]]

font = (16)
window = sg.Window('Sound Test', layout, size=(800, 300), font=font,
    element_justification='c', finalize=True) 




################# More PID Stuff #############################


sw_error = 0
prev_sw_error = 0
prev_PID_time = time.time()
now_PID_time = time.time()

button_down = False
button_up = False

PID_p = 0
PID_i = 0
PID_d = 0

PID_DIR = -1



if __name__ == "__main__":
    
    try:
        while True:

            ################ Steering wheel feedback output #####################
            if sw_initialized:
                sw_angle = get_sw_angle(SW_NUM)    # Physical steering wheel angle
                ego_vehicle.sensors.poll()
                
                # Virtual steering input (*-1 because of opposite to physical wheel)
                steering_input = -1 * ego_vehicle.sensors['electrics']['steering_input']

                # Virtual steering wheel angle (*-1 because of direction opposite to physical wheel):
                steering_angle = -1 * ego_vehicle.sensors['electrics']['steering']   
                
                
                # PID Proportional term
                sw_error = steering_angle - sw_angle    # find angle difference
                now_PID_time = time.time()
                time_interval = (now_PID_time - prev_PID_time)
                prev_PID_time = now_PID_time    # update prev time for next iteration
                PID_p = PID_DIR * K_P * sw_error

                # PID Integral term
                PID_i = PID_i + (PID_DIR * K_I * sw_error * time_interval)  # update integral
                PID_i = max(-80, min(PID_i, 80))   # limit the integral term output to +/-80


                # PID Derivative term
                PID_d = PID_DIR * K_D * (sw_error - prev_sw_error) / time_interval
                prev_sw_error = sw_error



                # PID control input (Clip within range)
                PID_output = max(-PID_MAX_FORCE, min(int(PID_p + PID_i + PID_d), PID_MAX_FORCE))

                window['-sw-status-'].Update(f"Physical: {round(sw_angle,2)} degrees" + 
                    f", Virtual: {round(steering_angle,2)} degrees, \n" +
                    f"Error: {round(sw_error,2)}, " + 
                    f"P: {round(PID_p, 2)}, I: {round(PID_i, 2)}, D: {round(PID_d, 2)},\n"
                    f"Output: {PID_output}")


                if (abs(sw_error) > 0):  # if physical-virtual difference larger than 1 deg
                    lsw.play_constant_force(SW_NUM, PID_output)
                else:
                    lsw.stop_constant_force(SW_NUM)

                
                ################ Steering wheel button handling ############################
                # Check if button pressed (button 22 in this case)
                button_state = get_sw_button_state(SW_NUM, AV_BUTTON_NUM)
                if button_state != 0:
                    button_down = True
                if (button_down == True) and (button_state == 0):
                    button_up = True
                    button_down = False
                if button_up == True:
                    print(f'Button {AV_BUTTON_NUM} pressed.')
                    button_up = False


            ################ The GUI Events ############################################
            event, values = window.read(timeout=100) 
            

            if event == sg.WIN_CLOSED or event == 'Exit':
                break     
            if event == '-check-sw-':
                print('Check steering wheel!!')
                window.perform_long_operation(lambda: get_sw_angle(SW_NUM), "-check-sw-done-")
                
            if event == '-init-sw-':
                window.perform_long_operation(lambda: initialize_sw(SW_NUM), "-init-sw-done-")
                window['-init-sw-'].update(disabled=True)
            if event == '-init-sw-done-':
                window['-init-sw-'].update(disabled=False)
                print('All good!')
            if event == '-check-sw-done-':
                print('Check done!')

            if event == 'Submit':
                print('PID updated!')
                K_P = float(values['-k-p-'])
                K_I = float(values['-k-i-'])
                K_D = float(values['-k-d-'])
                print(f'{K_P}, {K_I}, {K_D}')
        
        


    except KeyboardInterrupt:
            try:
                lsw.stop_constant_force(SW_NUM)
            except Exception as e:
                print(e)
            lsw.shutdown()

try:
    lsw.stop_constant_force(SW_NUM)
except Exception as e:
    print(e)
lsw.shutdown()

BeamNG_window = gw.getWindowsWithTitle('BeamNG.drive - 0')[0]
try:
    lsw.initialize_with_window(True, BeamNG_window._hWnd)
    print("Back to game")
except Exception as e:
    print(e)












# if __name__ == "xxxxx":

#     try:
#         w = gw.getActiveWindow()._hWnd
#         initialized = lsw.initialize_with_window(True, w)

#         while initialized:
#             while data_logging:

                
#                 sw_angle = get_sw_angle(SW_NUM)    # Physical steering wheel angle


#                 ego_vehicle.sensors.poll()
#                 steering_input = ego_vehicle.sensors['electrics']['steering_input']
#                 steering_angle = ego_vehicle.sensors['electrics']['steering']   # Virtual steering wheel angle
#                 print(f"Physical: {sw_angle} degrees" + 
#                     f", Virtual: {steering_angle} degrees")
                
#                 sw_error = steering_angle - sw_angle    # find angle difference
#                 if (abs(sw_error) >= 10):  # if physical-virtual difference larger than 10 deg
#                     lsw.play_constant_force(SW_NUM, int(K_P*sw_error))
#                 else:
#                     lsw.stop_constant_force(SW_NUM)
#             continue

#     except KeyboardInterrupt:
#         lsw.stop_constant_force(SW_NUM)
#         lsw.shutdown()
