import random
from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Electrics
import keyboard
import PySimpleGUI as sg

import logitech_steering_wheel as lsw
import pygetwindow as gw

import time

SW_NUM = 1  # Device number (todo: find device number)
SW_READING_RANGE = 31700    # Approximate maximum reading of the steering wheel (sw_state.lX)
SW_ANGLE_RANGE = 450    # Approximate maximum turning angle of the steering wheel

K_P = 1 # K_p of PID controller

sw_initialized = False #

layout = [[sg.Button('Initialize steering wheel', key='-init-sw-')],
          [sg.Button('Check steering wheel', key='-check-sw-')]]
font = (16)
window = sg.Window('Sound Test', layout, size=(800, 250), font=font,
    element_justification='c') 



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
    print(gw.getActiveWindowTitle())
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







if __name__ == "__main__":
    
    try:
        while True:

            ################ Read wheel status #####################
            if sw_initialized:
                sw_angle = get_sw_angle(SW_NUM)    # Physical steering wheel angle
                ego_vehicle.sensors.poll()
                steering_input = ego_vehicle.sensors['electrics']['steering_input']
                steering_angle = ego_vehicle.sensors['electrics']['steering']   # Virtual steering wheel angle
                print(f"Physical: {sw_angle} degrees" + 
                    f", Virtual: {steering_angle} degrees")
                
                
                sw_error = steering_angle - sw_angle    # find angle difference
                print(sw_error)

                if (abs(sw_error) >= 10):  # if physical-virtual difference larger than 10 deg
                    lsw.play_constant_force(SW_NUM, int(K_P*sw_error))
                else:
                    lsw.stop_constant_force(SW_NUM)




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
                window['-init-sw-'].update(disabled=True)
                print('All good!')
            if event == '-check-sw-done-':
                print('Check done!')

    except KeyboardInterrupt:
            # lsw.stop_constant_force(SW_NUM)
            lsw.shutdown()














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
