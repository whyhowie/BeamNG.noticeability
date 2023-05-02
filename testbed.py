# Testbed

import numpy as np

from beamngpy import BeamNGpy, Scenario, Vehicle, set_up_simple_logging


BEAMNG_HOME = 'D:/BeamNG/BeamNG.tech.v0.28.1.0'
BEAMNG_USER = 'D:/BeamNG/BeamNGpy.testbed'

'''
.. module:: checkpoints
    :platform: Windows
    :synopsis: Simple demo on how to use checkpoints in a scenario.

.. moduleauthor:: Pascale Maul <pmaul@beamng.gmbh>
'''
from beamngpy import BeamNGpy, Scenario, Vehicle

if __name__ == '__main__':
    with BeamNGpy('localhost', 64256, home=BEAMNG_HOME, user=BEAMNG_USER) as bng:
        scenario = Scenario('smallgrid', 'waypoint demo')
        vehicle = Vehicle('test_car', model='etk800', rot_quat=(0, 0, 0, 1))
        scenario.add_vehicle(vehicle)

        positions = [(0, -10, 0), (0, -20, 0), (0, -30, 0)]
        scales = [(1.0, 1.0, 1.0)] * 3
        scenario.add_checkpoints(positions, scales)
        scenario.make(bng)

        bng.scenario.load(scenario)
        bng.scenario.start()
        input('press \'Enter\' to exit demo')