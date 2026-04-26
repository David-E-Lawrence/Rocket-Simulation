import os
import numpy as np
import csv
import logging

def analyze(run_dir):
        logger=logging.getLogger("Rocket_Simulation.Analyze")
        logger.info("Analyzing flight data")


        logger.debug("Loading flight data for analysis")

        data = np.load(os.path.join(run_dir, "flight_log.npy"), allow_pickle=True)

        t = data[:, 0]
        altitude = data[:, 7]
        vx = data[:, 3]
        vy = data[:, 4]
        speed = np.linalg.norm(np.column_stack((vx, vy)))

        # analyzing flight

        logger.debug("Performing flight analysis on data")

        max_altitude = np.max(altitude)
        max_altitude_time = t[np.argmax(altitude)]
        max_speed = np.max(speed)
        max_speed_time = t[np.argmax(speed)]

        # save analysis results

        logger.info("Saving analysis results")

        with open(os.path.join(run_dir, "analysis.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["max_altitude", "max_altitude_time", "max_speed", "max_velocity_time"])
            writer.writerow([max_altitude, max_altitude_time, max_speed, max_speed_time])