import numpy as np
import time
from beamngpy import BeamNGpy, Scenario, Vehicle, set_up_simple_logging

import matplotlib.pyplot as plt
import numpy as np

from beamngpy import BeamNGpy, Scenario, Vehicle

# beamng = BeamNGpy('localhost', 64256, home='D:/BeamNG/BeamNG.tech.v0.28.1.0', user='BeamNGpy')

bng = BeamNGpy('localhost', 64256, home='D:/BeamNG/BeamNG.tech.v0.28.1.0', user='BeamNGpy')
# Launch BeamNG.tech
bng.open()
# Create a scenario in west_coast_usa called 'Example'
scenario = Scenario('west_coast_usa', 'Example')
# Create an ETK800 with the licence plate 'PYTHON'
vehicle = Vehicle('ego_vehicle', model='etk800', license='NOTICEABILITY')
# Add it to our scenario at this position and rotation
scenario.add_vehicle(vehicle, pos=(-700, 100, 118), rot_quat=(0, 0, 0.3826834, 0.9238795))

# Place files defining our scenario for the simulator to read
scenario.make(bng)





# Load and start our scenario
bng.scenario.load(scenario)
# bng.scenario.start()
# Make the vehicle's AI span the map
vehicle.ai.drive_in_lane(True)
vehicle.ai.set_aggression(0.3)
vehicle.ai.set_mode('span')

# Add traffic
bng.traffic.spawn(max_amount=15)

# time.sleep(30)
# print(bng.scenario.find_objects_class('vehicle'))
# bng.traffic.start()