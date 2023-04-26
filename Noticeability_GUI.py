
import PySimpleGUI as sg
import keyboard
import random
import time
from beamngpy import BeamNGpy, Scenario, Vehicle, set_up_simple_logging
import matplotlib.pyplot as plt

# beamng = BeamNGpy('localhost', 64256, home='D:/BeamNG/BeamNG.tech.v0.28.1.0', user='BeamNGpy')

# bng = BeamNGpy('localhost', 64256, home='D:/BeamNG/BeamNG.tech.v0.28.1.0', user='BeamNGpy')

# is_beamng_running = False


BEAMNG_PROCESS_NAME = 'BeamNG.tech.x64'
BEAMNG_HOME = 'D:/BeamNG/BeamNG.tech.v0.28.1.0'
BEAMNG_USER = 'D:/BeamNG/BeamNGpy'

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
        bng = BeamNGpy('localhost', 64256, home=BEAMNG_HOME, user=BEAMNG_USER)
        bng.open()  # The process freezes until BeamNG is launched
        print('BeamNG is launched!')
        return

# Run a predefined scenario   
def run_scenario():
    return




################### Noticeability Test ######################

def signal_noticed():
    print("Signal Noticed!")

# Callback function when "-" key is pressed, showing signal noticed by user
keyboard.add_hotkey('-', signal_noticed)



################### Make GUI ################################

launch_frame = sg.Frame('Launch', [[sg.Button('Launch BeamNG!', key='-launch-')]])
scenario_frame = sg.Frame('Scenario', [[sg.Button('Run Scenario')],[sg.Button('Add Traffic')]])
layout = [[sg.Text('')],
          [launch_frame, scenario_frame],
          []          
          [sg.Button('Dummy Button'), sg.Exit()]]      

window = sg.Window('BeamNG.tech Noticeability Test', layout, size=(400, 150))      

while True:                             # The Event Loop
    event, values = window.read() 
           
    if event == sg.WIN_CLOSED or event == 'Exit':
        break      
    if event == '-launch-':
        launch_beamng()

window.close()







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