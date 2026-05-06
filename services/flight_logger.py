import os
import numpy as np


class Flight_Logger:
    def __init__(self, run_dir, instance):
        self.run_dir = run_dir
        self.instance=instance

        # store raw data in memory first
        self.data = []

    def log(self, time, pos, v, fuel_mass, drag, alt, heading):
        self.data.append([
            time,
            pos[0], pos[1],
            v[0], v[1],
            fuel_mass,
            drag,
            alt, 
            heading
        ])

    def save(self):
        filename=f"flight_log.npy"

        np.save(os.path.join(self.run_dir, filename), np.asarray(self.data))
        
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()