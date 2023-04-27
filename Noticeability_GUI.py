
import PySimpleGUI as sg
import keyboard
import random
import time
from beamngpy import BeamNGpy, Scenario, Vehicle, set_up_simple_logging
from beamngpy.sensors import (
    IMU, Camera, Damage, Electrics, Lidar, State, Timer, Ultrasonic)
import matplotlib.pyplot as plt

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
        scenario = Scenario('west_coast_usa', 'Example')
        # Create an ETK800 with the licence plate 'PYTHON'
        vehicle = Vehicle('ego_vehicle', model='etk800', license='NOTICE')
        # Add it to our scenario at this position and rotation
        scenario.add_vehicle(vehicle, pos=(-724, 100, 118), rot_quat=(0, 0, 0.3826834, 0.9238795))
        

        # Place files defining our scenario for the simulator to read
        scenario.make(bng)

        # Load and start our scenario
        bng.scenario.load(scenario) 
        bng.scenario.start() # Blocking until loaded
        return True
    except Exception as e: 
        print(e)
        return False


def add_traffic():
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
        vehicle.sensors.poll()
        return vehicle
    except Exception as e: 
        print(e)
        return None

def ai_driving(vehicle_id):
    try:
        vehicle = bng.scenario.get_vehicle(vehicle_id)
        vehicle.ai.drive_in_lane(True)
        vehicle.ai.set_aggression(0.1)
        vehicle.ai.set_mode('span')
        bng.display_gui_message('Autonomous Driving')
    except Exception as e: 
        print(e)

def manual_driving(vehicle_id):
    try:
        vehicle = bng.scenario.get_vehicle(vehicle_id)
        vehicle.ai.set_mode('disabled')
        bng.display_gui_message('Manual Driving')
    except Exception as e: 
        print(e)


################### Noticeability Test ######################

def signal_noticed():
    print("Signal Noticed!")

# Callback function when "-" key is pressed, showing signal noticed by user
keyboard.add_hotkey('-', signal_noticed)



################### Make GUI ################################

launch_frame = sg.Frame('Launch', [[sg.Button('Launch BeamNG!', key='-launch-')]])
scenario_frame = sg.Frame('Scenario', [[sg.Button('Run Scenario', key='-scenario-', disabled=False)],
                [sg.Button('End Scenario', key='-end-scenario-', disabled=False)],
                [sg.Button('Add Traffic', key='-traffic-', disabled=True)]])
driving_frame = sg.Frame('Driving Mode',[[sg.Radio('AI', 'drive-mode', key='-auto-driving-', enable_events=True, disabled=True)],
            [sg.Radio('Manual', 'drive-mode', key='-manual-driving-', enable_events=True, default=True, disabled=True)]])
layout = [[sg.Text('')],
          [launch_frame, scenario_frame, driving_frame],
          [],          
          [sg.Button('Dummy Button'), sg.Button('Get Position', key='-position-'), sg.Exit()]]      


font = (16)
window = sg.Window('BeamNG.tech Noticeability Test', layout, size=(500, 250), font=font)      


########### Helper GUI Functions ########
# Enable driving mode and other options
def enable_options():
    window['-auto-driving-'].update(disabled=False)
    window['-manual-driving-'].update(disabled=False)

def disable_options():
    window['-auto-driving-'].update(disabled=True)
    window['-manual-driving-'].update(disabled=True)
#######################################




while True:                             # The Event Loop
    event, values = window.read() 
           
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
    if event == '-position-':
        try:
            print(get_vehicle_status('ego_vehicle'), get_vehicle_status('ego_vehicle').state)
        except Exception as e:
            print(e)

    if event == '-auto-driving-' and values['-auto-driving-']==True:
        print('======Autonomous driving======')
        ai_driving('ego_vehicle')
    if event == '-manual-driving-' and values['-manual-driving-']==True:
        print('======Manual driving======')
        manual_driving('ego_vehicle')

window.close()
bng.close() # Terminate simulator





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