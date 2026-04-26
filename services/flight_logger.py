import os
import numpy as np
import logging


class Flight_Logger:
    def __init__(self, run_dir):
        self.run_dir = run_dir

        # store raw data in memory first
        self.data = []

        self.logger=logging.getLogger("Rocket_Simulation.Flight_Logger")

    def log(self, time, pos, v, fuel_mass, drag, alt):
        self.logger.debug("Logging flight data")
        self.data.append([
            time,
            pos[0], pos[1],
            v[0], v[1],
            fuel_mass,
            drag,
            alt
        ])

    def save(self, filename="flight_log.npy"):
        self.logger.info("Saving flight data")

        arr = np.array(self.data)
        np.save(os.path.join(self.run_dir, filename), arr)
        
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()