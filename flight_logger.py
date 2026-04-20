import os
import numpy as np


class Flight_Logger:
    def __init__(self, run_dir):
        self.run_dir = run_dir

        # store raw data in memory first
        self.data = []

    def log(self, time, pos, v, fuel_mass, drag, alt):
        self.data.append([
            time,
            pos[0], pos[1],
            v[0], v[1],
            fuel_mass,
            drag,
            alt
        ])

    def save(self, filename="flight_log.npy"):
        arr = np.array(self.data)
        np.save(os.path.join(self.run_dir, filename), arr)
        
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()