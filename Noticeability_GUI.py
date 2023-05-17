
import PySimpleGUI as sg
import keyboard
import pygame
import numpy as np
import random
import time
from beamngpy import BeamNGpy, Scenario, Vehicle, set_up_simple_logging
from beamngpy.sensors import (
    IMU, Camera, Damage, Electrics, Lidar, State, Timer, Ultrasonic)
import logitech_steering_wheel as lsw
import pygetwindow as gw

# https://github.com/BeamNG/BeamNGpy/blob/master/examples/feature_overview.ipynb
# beamng = BeamNGpy('localhost', 64256, home='D:/BeamNG/BeamNG.tech.v0.28.1.0', user='BeamNGpy')
# bng = BeamNGpy('localhost', 64256, home='D:/BeamNG/BeamNG.tech.v0.28.1.0', user='BeamNGpy')

# is_beamng_running = False


BEAMNG_PROCESS_NAME = 'BeamNG.tech.x64'
BEAMNG_HOME = 'D:/BeamNG/BeamNG.tech.v0.28.1.0'
BEAMNG_USER = 'D:/BeamNG/BeamNGpy'

# These are just initialized values - to make sure other functions are working
# Change settings in the run_scenario() function
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

        # Set deterministic mode
        bng.settings.set_deterministic(60)

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
steering_frame = sg.Frame('Steering Feedback', [[sg.Button('Initialize steering wheel', key='-init-sw-')],
          [sg.Button('Check steering wheel', key='-check-sw-')],
          [sg.Text('------------------------------------------------------------------\n' + 
                   '------------------------------------------------------------------\n' + 
                   '------------------------------------------------------------------', key='-sw-status-')],])


layout = [[sg.Text('')],
          [launch_frame, scenario_frame, driving_frame, signal_frame],
          [],
          [sg.HorizontalSeparator()],
          [steering_frame],
          [sg.HorizontalSeparator()],
          [sg.Button('Dummy Button'), sg.Button('Get Status', key='-status-'), 
          sg.Button('Get Vehicle Config', key='-vehicle-config-'),
          sg.Button('Get Game State', key='-game-state-'), sg.Exit()]]      


font = (16)
window = sg.Window('BeamNG.tech Noticeability Test', layout, size=(800, 600), font=font,
    element_justification='c')      





########### Key Binding using keyboard ##########
# Callback function when "=" key is pressed, starting audio test
keyboard.add_hotkey('=', lambda: window['-audio-test-'].click())

# Callback function when "-" key is pressed, showing signal noticed by user
keyboard.add_hotkey('-', signal_noticed)



########### Steering wheel stuff ###############################################################
########### Steering wheel constants
SW_NUM = 0  # Device number (todo: find device number)
AV_BUTTON_NUM = 22  # Button 22 for driving mode switching
SW_READING_RANGE = 31700    # Approximate maximum reading of the steering wheel (sw_state.lX)
SW_ANGLE_RANGE = 450    # Approximate maximum turning angle of the steering wheel


sw_initialized = False


# Initialize steering wheel
def initialize_sw(device_num):
    global sw_initialized
    
    try:
        # w = gw.getWindowsWithTitle('BeamNG.drive - 0')[0]
        w = gw.getActiveWindow()
        print(gw.getActiveWindowTitle())
        print(w)
        lsw.initialize_with_window(True, w._hWnd)

        print("SDK version is: " + str(lsw.get_sdk_version()))


        if lsw.is_connected(device_num):
            print(f'connected to a steering wheel at index {device_num}')
        else:
            print('Connection failed')

        # lsw.update()
        lsw.get_current_controller_properties(device_num)

        sw_initialized = True
    except Exception as e:
        print(e)


def get_sw_angle(device_num):
    if sw_initialized:
        lsw.update()
        sw_state = lsw.get_state(device_num)
        # Find current physical steering wheel angle
        sw_angle = sw_state.lX / SW_READING_RANGE * SW_ANGLE_RANGE
        # print(sw_angle)
        return sw_angle


########### Constants for PID controller ################################
K_P = .2 # K_p of PID controller
K_I = .3 # K_i of PID controller
K_D = .05 # K_d of PID controller

PID_MAX_FORCE = 15

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

################ Steering wheel feedback output #####################
def sw_default_output(device_num=SW_NUM):
    lsw.play_spring_force(device_num, 0, 20, 20)    
        # 0: centering offset; 20: saturation force; 20: slope/spring constant
    lsw.play_damper_force(device_num, 10)

def stop_sw_default_output(device_num=SW_NUM):
    if lsw.is_playing(device_num, lsw.ForceType.SPRING):
        lsw.stop_spring_force(device_num)
    if lsw.is_playing(device_num, lsw.ForceType.DAMPER):
        lsw.stop_damper_force(device_num)


def sw_feedback_output(device_num=SW_NUM, vehicle_id="ego_vehicle"):
    global sw_error, prev_sw_error, prev_PID_time, now_PID_time, PID_p, PID_i, PID_d
    try:
        if sw_initialized and bng.get_gamestate()['state'] == 'scenario':
            
            sw_angle = get_sw_angle(device_num)    # Physical steering wheel angle
            
            # Get virtual steering wheel angle
            vehicle = bng.scenario.get_vehicle(vehicle_id)
            vehicle.sensors.poll()
            # Virtual steering input (*-1 because of opposite to physical wheel)
            steering_input = -1 * vehicle.sensors['electrics']['steering_input']
            # Virtual steering wheel angle (*-1 because of direction opposite to physical wheel):
            steering_angle = -1 * vehicle.sensors['electrics']['steering']   
            
            if driving_mode == 'autonomous':
                stop_sw_default_output(device_num)  # default behavior
                lsw.play_damper_force(device_num, 10) # add some friction force

                # PID Proportional term
                sw_error = steering_angle - sw_angle    # find angle difference
                now_PID_time = time.time()
                time_interval = (now_PID_time - prev_PID_time)
                prev_PID_time = now_PID_time    # update prev time for next iteration
                PID_p = PID_DIR * K_P * sw_error

                # PID Integral term
                PID_i = PID_i + (PID_DIR * K_I * sw_error * time_interval)  # update integral
                PID_i = max(-15, min(PID_i, 15))   # limit the integral term output to +/-80


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


                if (abs(sw_error) > 0):  # if physical-virtual difference larger than 0 deg
                    lsw.play_constant_force(SW_NUM, PID_output)
                else:
                    lsw.stop_constant_force(SW_NUM)

            else:   # if not autonomous driving
                if lsw.is_playing(device_num, lsw.ForceType.CONSTANT):
                    lsw.stop_constant_force(SW_NUM)
                sw_default_output(device_num)
                window['-sw-status-'].Update(f"Physical: ------ degrees" + 
                    f", Virtual: {round(steering_angle,2)} degrees, \n" +
                    f"Error: ------, " + 
                    f"P: ------, I: ------, D: ------,\n"
                    f"Output: Not in autonomous driving mode!")
                
    except Exception as e:
        print(e)




################ Steering wheel button handling ############################
#################### steering wheel buttons ###############
# Not using pygame
def get_sw_button_state(device_num, button_num):
    if sw_initialized:
        lsw.update()
        s = lsw.get_state(device_num)

        return s.rgbButtons[button_num]
# Use Button 22 to change driving mode ("return" button on steering wheel)
# This first trigger GUI events. then the game will make the switch accordingly
button_down = False
button_up = False
driving_mode_button_pressed = False

def driving_mode_button_handler(device_num=SW_NUM, button_num=AV_BUTTON_NUM):
    global driving_mode, driving_mode_button_pressed, button_down, button_up
    # Check if button pressed (button 22 in this case)
    button_state = get_sw_button_state(device_num, button_num)
    if button_state != 0:
        button_down = True
    if (button_down == True) and (button_state == 0):
        button_up = True
        button_down = False
    if button_up == True:
        driving_mode_button_pressed = True
        print(f'Button {button_num} pressed.')
        button_up = False
        if driving_mode == 'autonomous':
            # driving_mode = 'manual'
            print(f'Button pressed, switching driving mode to {driving_mode}')
            window['-manual-driving-'].Update(value=True)
            window.write_event_value('-manual-driving-', True)
        else:
            # driving_mode = 'autonomous'
            print(f'Button pressed, switching driving mode to {driving_mode}')
            window['-auto-driving-'].Update(value=True)
            window.write_event_value('-auto-driving-', True)





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







################### main() ####################
if __name__ == "__main__":
    

    while True:                             # The Event Loop
        event, values = window.read(timeout=100) 


        update_based_on_state() # update GUI options based on state
        
        if sw_initialized:
            driving_mode_button_handler() # change driving mode
            sw_feedback_output()

            
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
        if (event == '-manual-driving-') or (driving_mode_button_pressed == True\
            and values['-manual-driving-']==True):
            driving_mode_button_pressed = False
            print('=======Manual driving=========')
            manual_driving('ego_vehicle')
            update_driving_mode_radio(driving_mode) # In case mode switch fails


        # Steering wheel buttons
        if event == '-check-sw-':
            print('Check steering wheel!!')
            window.perform_long_operation(lambda: print(get_sw_angle(SW_NUM)), "-check-sw-done-")
        if event == '-init-sw-':
            window.perform_long_operation(lambda: initialize_sw(SW_NUM), "-init-sw-done-")
            window['-init-sw-'].update(disabled=True)
        if event == '-init-sw-done-':
            window['-init-sw-'].update(disabled=False)
            print('All good!')

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