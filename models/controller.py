import numpy as np
import logging

class Controller:
    def __init__(self, instance_index, instance_count, env):
        self.instance_standing=instance_index/instance_count
        self.logger=logging.getLogger("Rocket_Simulation.Controller")
        self.instance_index=instance_index
        self.env=env

        self.logger.debug(f"Controller instance {instance_index} of {instance_count} initialized")
    def __call__(self, state):

        self.logger.debug(f"Controller instance {self.instance_index} called")

        if np.linalg.norm(state["v"]) <= 1e-3:
            direction=np.arctan2(state["v"][1], state["v"][0])
        else:
            direction=np.pi/2

        if self.env.alt(state["pos"])<10000:
            theta=np.pi/2
        else:
            theta=direction-(self.instance_standing*np.pi/1.9)

        return theta