import random
from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Electrics
import keyboard

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
    

keyboard.add_hotkey('0', toggle_data_logging)

print('Press 0 key to start logging')

if __name__ == "__main__":
    while True:
        while data_logging:
            ego_vehicle.sensors.poll()
            print(f"{ego_vehicle.sensors['electrics']['steering_input']}" + 
                  f" at {ego_vehicle.sensors['electrics']['steering']} degrees")

        continue