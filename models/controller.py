import numpy as np

class Controller:
    def __init__(self, instance_index, instance_count, env):
        self.instance_standing=instance_index/instance_count
        self.instance_index=instance_index
        self.env=env
    def __call__(self, state):


        if np.linalg.norm(state["v"]) <= 1e-3:
            direction=np.arctan2(state["v"][1], state["v"][0])
        else:
            direction=np.pi/2

        if self.env.alt(state["pos"])<112000*self.instance_standing:
            theta=np.pi/2
        else:
            theta=direction-(np.pi/2)

        return theta