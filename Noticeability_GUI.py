
import PySimpleGUI as sg
import keyboard
import pygame
import numpy as np
import random
import time
from beamngpy import BeamNGpy, Scenario, Vehicle, set_up_simple_logging
from beamngpy.sensors import (
    IMU, Camera, Damage, Electrics, Lidar, State, Timer, Ultrasonic)
import matplotlib.pyplot as plt

# https://github.com/BeamNG/BeamNGpy/blob/master/examples/feature_overview.ipynb
# beamng = BeamNGpy('localhost', 64256, home='D:/BeamNG/BeamNG.tech.v0.28.1.0', user='BeamNGpy')
# bng = BeamNGpy('localhost', 64256, home='D:/BeamNG/BeamNG.tech.v0.28.1.0', user='BeamNGpy')

# is_beamng_running = False


BEAMNG_PROCESS_NAME = 'BeamNG.tech.x64'
BEAMNG_HOME = 'D:/BeamNG/BeamNG.tech.v0.28.1.0'
BEAMNG_USER = 'D:/BeamNG/BeamNGpy'

bng = BeamNGpy('localhost', 64256, home=BEAMNG_HOME, user=BEAMNG_USER)
scenario = Scenario('east_coast_usa', 'Example')
vehicle = Vehicle('ego_vehicle', model='etk800', license='NOTICE')

################### BeamNG.tech Functions ###################
import subprocess
# Check if BeamNG is running
def process_exists(process_name):
    progs = str(subprocess.check_output('tasklist'))
    # print(progs)
    if process_name in progs:
        return True
    else:
        return False

# Launch BeamNG 
def launch_beamng():  
    if process_exists(BEAMNG_PROCESS_NAME):
        print('BeamNG.tech already running!')
        return
    else:
        print('Launching BeamNG.tech...')
        # bng = BeamNGpy('localhost', 64256, home=BEAMNG_HOME, user=BEAMNG_USER)
        bng.open()  # The process freezes (blocking) until BeamNG is launched
        print('BeamNG is launched!')

        return

# Run a predefined scenario   
def run_scenario():
    print('Starting a scenario!')
    try:
        # Create a scenario in west_coast_usa called 'Example'

        scenario = Scenario('west_coast_usa', 'Example', description='Hello!!!!!')
        # Create an ETK800 with the licence plate
        vehicle = Vehicle('ego_vehicle', model='etk800')
        # vehicle = Vehicle('ego_vehicle', model='etk800', \
        #     part_config='vehicles/etk800/Etk856tx_A_adas.pc')
        # Add it to our scenario at this position and rotation
        # scenario.add_vehicle(vehicle, pos=(-724, 100, 118), rot_quat=(0, 0, 0.3826834, 0.9238795))
        scenario.add_vehicle(vehicle, pos=(-195, -787, 134), cling=True, rot_quat=(-0.07, -0.07, -0.46, 0.88))

    
        # Place files defining our scenario for the simulator to read
        scenario.make(bng)

        # Load and start our scenario
        bng.scenario.load(scenario) 

        # Find waypoints and print them
        # waypoints = scenario.find_waypoints() # get a list of locations from the simulation
        # waypoints = {w.name: w for w in waypoints}
        # print(waypoints)

        # Initialize electrics sensor
        electrics = Electrics()


        # Run through this whole thing to make sure we have gps in the vehicle
        # Basically respawning the vehicle
        bng.vehicles.despawn(vehicle)
        bng.vehicles.spawn(vehicle, pos=(-195, -787, 134), rot_quat=(-0.07, -0.07, -0.46, 0.88))
        # bng.vehicles.await_spawn('ego_vehicle')
        ego_vehicle = bng.scenario.get_vehicle('ego_vehicle')
        ego_vehicle.set_license_plate('NOTICE')
        ego_vehicle.sensors.attach('electrics', electrics)
    
        # bng.scenario.start()
        ego_vehicle.switch()
        


        return True
    except Exception as e: 
        print(e)
        return False


def add_traffic():
    try:
        bng.display_gui_message('Adding traffic')
        bng.traffic.spawn(max_amount=10)
        print("Traffic Spawned")
    except Exception as e:
        print(e)
    return

def end_scenario():
    try:
        bng.scenario.stop()
        print('Scenario ended!')
    except Exception as e: 
        print(e)

# Vehicle status and control
def get_vehicle_status(vehicle_id):
    try:
        vehicle = bng.scenario.get_vehicle(vehicle_id)
        print('steering sensor info:')
        vehicle.sensors.poll()
        print(f"Steering angle: {vehicle.sensors['electrics']['steering']} \n" + 
            f"Steering input: {vehicle.sensors['electrics']['steering_input']}")
        return vehicle
    except Exception as e: 
        print(e)
        return None

def get_vehicle_config(vehicle_id):
    try:
        vehicle = bng.scenario.get_vehicle(vehicle_id)
        print('part config:')
        print(vehicle.get_part_config())
        return vehicle
    except Exception as e: 
        print(e)
        return None

driving_mode = ''

def ai_driving(vehicle_id):
    global driving_mode
    try:
        vehicle = bng.scenario.get_vehicle(vehicle_id)
        vehicle.ai.drive_in_lane(True)
        vehicle.ai.set_aggression(0.2)
        vehicle.ai.set_mode('traffic') # although not documented, 'traffic' seems more reasonable
        # vehicle.ai.set_mode('span') # not following traffic rules
        bng.display_gui_message('Autonomous Driving')
        driving_mode = 'autonomous'
    except Exception as e: 
        print("Failed to switch driving mode.")
        print(e)

def manual_driving(vehicle_id):
    global driving_mode
    try:
        vehicle = bng.scenario.get_vehicle(vehicle_id)
        vehicle.ai.set_mode('disabled')
        bng.display_gui_message('Manual Driving')
        driving_mode = 'manual'
    except Exception as e:
        print("Failed to switch driving mode.")
        print(e)



################### Noticeability Test ######################
noticed_flag = False
pygame.init()   # Use pygame to play sound
volume = 0.001
notification_sound = pygame.mixer.Sound("assets/mixkit-interface-hint-notification-911.wav")

def play_sound():
    global noticed_flag, volume
    while noticed_flag == False:
        notification_sound.set_volume(volume)
        notification_sound.play()
        print("Sound played at volume %.3f" % (volume))
        time.sleep(2)   # wait for 2 seconds

        volume = np.clip(volume + 0.001, 0, 1)  # update volume
        continue
    print(f"Playing stopped. volume={volume}")
    volume = 0.001
    noticed_flag = False


def signal_noticed():
    global noticed_flag
    noticed_flag = True
    print("Signal Noticed!")



 
################### Make GUI ################################

launch_frame = sg.Frame('Launch', [[sg.Button('Launch BeamNG!', key='-launch-', button_color = ('white','orange red') )]])
scenario_frame = sg.Frame('Scenario', [[sg.Button('Run Scenario', key='-scenario-', disabled=False)],
                [sg.Button('End Scenario', key='-end-scenario-', disabled=False)],
                [sg.Button('Add Traffic', key='-traffic-', disabled=True)]])
driving_frame = sg.Frame('Driving Mode',[[sg.Radio('AI', 'drive-mode', key='-auto-driving-', enable_events=True, disabled=False)],
            [sg.Radio('Manual', 'drive-mode', key='-manual-driving-', enable_events=True, disabled=False)]])
signal_frame = sg.Frame('Signal Detection Test', [[sg.Button('Audio Test (=)', key='-audio-test-', button_color = 'red', disabled=False)],
                [sg.Text('Audio Test Not running', key='-audio-test-text-')]])



layout = [[sg.Text('')],
          [launch_frame, scenario_frame, driving_frame, signal_frame],
          [],
          [sg.HorizontalSeparator()],          
          [sg.Button('Dummy Button'), sg.Button('Get Status', key='-status-'), 
          sg.Button('Get Vehicle Config', key='-vehicle-config-'),
          sg.Button('Get Game State', key='-game-state-'), sg.Exit()]]      


font = (16)
window = sg.Window('BeamNG.tech Noticeability Test', layout, size=(800, 250), font=font,
    element_justification='c')      


########### Helper GUI Functions ########
# Enable driving mode and other options
def enable_options():
    window['-auto-driving-'].update(disabled=False)
    window['-manual-driving-'].update(disabled=False)
    window['-traffic-'].update(disabled=False)

def disable_options():
    window['-auto-driving-'].update(disabled=True)
    window['-manual-driving-'].update(disabled=True)
    window['-traffic-'].update(disabled=True)


def update_based_on_state():
    # current_state = bng.get_gamestate()
    # print(current_state)
    try:
        if bng.get_gamestate()['state'] == 'scenario':    
            enable_options()
            return
        else:
            disable_options()
    except:
        disable_options()
        pass

def update_driving_mode_radio(mode):
    if mode == 'autonomous':
        window['-auto-driving-'].update(value=True)
    if mode == 'manual':
        window['-manual-driving-'].update(value=True)


########### Key Binding using keyboard ##########
# Callback function when "=" key is pressed, starting audio test
keyboard.add_hotkey('=', lambda: window['-audio-test-'].click())

# Callback function when "-" key is pressed, showing signal noticed by user
keyboard.add_hotkey('-', signal_noticed)




#################### steering wheel buttons ###############
SW_NUM = 1  # Steering wheel device number
# steering_wheel = pygame.joystick.Joystick(SW_NUM)
# steering_wheel.init()

# Use Button 22 to change driving mode ("return" button on steering wheel)
# This first trigger GUI events. then the game will make the switch accordingly

driving_mode_button_pressed = False

def driving_mode_button():
    global driving_mode, driving_mode_button_pressed
    # pygame_events = pygame.event.get()
    # for event in pygame_events:
    #     if pygame.event.event_name(event.type) == 'JoyButtonUp' \
    #         and event.button == 22:
    #         driving_mode_button_pressed = True
    #         print('Button 22 pressed.')
            
            # if driving_mode == 'autonomous':
            #     # driving_mode = 'manual'
            #     print(f'Button pressed, switching driving mode to {driving_mode}')
            #     window['-manual-driving-'].Update(value=True)
            #     window.write_event_value('-manual-driving-', True)
            # else:
            #     # driving_mode = 'autonomous'
            #     print(f'Button pressed, switching driving mode to {driving_mode}')
            #     window['-auto-driving-'].Update(value=True)
            #     window.write_event_value('-auto-driving-', True)





################### main() ####################
if __name__ == "__main__":

    while True:                             # The Event Loop
        event, values = window.read(timeout=100) 


        update_based_on_state() # update GUI options based on state
        
        driving_mode_button() # change driving mode using pygame

            
        if event == sg.WIN_CLOSED or event == 'Exit':
            break      
        if event == '-launch-':
            launch_beamng() # Blocking until BeamNG is launched
            window['-scenario-'].update(disabled=False)
        if event == '-scenario-':
            if run_scenario():
                window['-scenario-'].update(disabled=True)
                enable_options()
        if event == '-end-scenario-':
            end_scenario()
            window['-end-scenario-'].update(disabled=False)
            window['-scenario-'].update(disabled=False)
            disable_options()

        if event == '-traffic-':
            add_traffic()
            window['-traffic-'].update(disabled=True)



        # Debug buttons
        if event == '-status-':
            try:
                print(get_vehicle_status('ego_vehicle'))
            except Exception as e:
                print(e)
        if event == '-vehicle-config-':
            try:
                print(get_vehicle_config('ego_vehicle'))
            except Exception as e:
                print(e)
        if event == '-game-state-':
            try:
                update_based_on_state()
            except Exception as e:
                print(e)




        # driving mode radio buttons
        if (event == '-auto-driving-') or (driving_mode_button_pressed == True\
            and values['-auto-driving-']==True):
            driving_mode_button_pressed = False
            print('======Autonomous driving======')
            ai_driving('ego_vehicle')
            update_driving_mode_radio(driving_mode) # In case mode switch fails
            # driving_mode = 'autonomous'
        if (event == '-manual-driving-') or (driving_mode_button_pressed == True\
            and values['-manual-driving-']==True):
            driving_mode_button_pressed = False
            print('=======Manual driving=========')
            manual_driving('ego_vehicle')
            update_driving_mode_radio(driving_mode) # In case mode switch fails
            # driving_mode = 'manual'


        # Audio test
        if event == '-audio-test-':
            window['-audio-test-'].update(disabled=True)
            window['-audio-test-text-'].update(value='Audio Test Running')
            print("Playing sound")
            window.perform_long_operation(play_sound, "-sound-stopped-")
        if event == '-sound-stopped-':
            print('All good! Next audio test available!')
            window['-audio-test-text-'].update(value='Audio Test Not Running')
            window['-audio-test-'].update(disabled=False)


    window.close()
    bng.close() # Terminate simulator

    pygame.quit() # Quit PyGame




# # Launch BeamNG.tech
# bng.open()
# # Create a scenario in west_coast_usa called 'Example'
# scenario = Scenario('west_coast_usa', 'Example')
# # Create an ETK800 with the licence plate 'PYTHON'
# vehicle = Vehicle('ego_vehicle', model='etk800', license='NOTICEABILITY')
# # Add it to our scenario at this position and rotation
# scenario.add_vehicle(vehicle, pos=(-715, 100, 118), rot_quat=(0, 0, 0.3826834, 0.9238795))

# # Place files defining our scenario for the simulator to read
# scenario.make(bng)


# # Load and start our scenario
# bng.scenario.load(scenario)
# # bng.scenario.start()
# # Make the vehicle's AI span the map
# vehicle.ai.drive_in_lane(True)
# vehicle.ai.set_aggression(0.3)
# vehicle.ai.set_mode('span')

# # Add traffic
# bng.traffic.spawn(max_amount=15)

# time.sleep(30)
# print(bng.scenario.find_objects_class('vehicle'))
# bng.traffic.start()