import matplotlib.pyplot as plt
import numpy as np
from physics import Physics
from rocket import Rocket
import environment
from logger import Logger


if __name__ == "__main__":

    # setting constants

    t=0
    dt=0.001

    # instantiate classes

    rocket=Rocket(y_start=0, dry_mass=156500, fuel_mass=410900, max_thrust=7562000, mass_flow_rate=2300)
    physics=Physics()
    env=environment.Earth()

    # setting starting state

    rocket.throttle=1

    # simulation loop
    with Logger() as logger:
        while rocket.y>=0:
            physics.step(dt=0.001, rocket=rocket, env=env)
            logger.log(t, rocket.y, rocket.vy, rocket.fuel_mass)
            t+=dt