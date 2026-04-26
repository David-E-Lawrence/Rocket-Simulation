import os
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np
import logging

def plot(run_dir, plot_dir):

        logger=logging.getLogger("Rocket_Simulation.Plotting")

        logger.info("Plotting flight data")

        logger.debug("Loading flight data for plotting")

        data = np.load(os.path.join(run_dir, "flight_log.npy"), allow_pickle=True)

        t = data[:, 0]
        altitude = data[:, 7]
        speed = np.linalg.norm(np.column_stack((data[:, 3], data[:, 4])), axis=1)
        fuel = data[:, 5]

        # altitude

        logger.debug("Plotting altitude vs time")

        plt.figure()
        plt.plot(t, altitude)
        plt.xlabel("Time (s)")
        plt.ylabel("Altitude (m)")
        plt.title("Altitude vs Time")
        plt.grid()
        plt.savefig(os.path.join(plot_dir, "altitude.png"))
        plt.close()

        # velocity
        logger.debug("Plotting speed vs time")
        plt.figure()
        plt.plot(t, speed)
        plt.xlabel("Time (s)")
        plt.ylabel("Speed (m/s)")
        plt.title("Speed vs Time")
        plt.grid()
        plt.savefig(os.path.join(plot_dir, "speed.png"))
        plt.close()

        # fuel
        logger.debug("Plotting fuel vs time")
        plt.figure()
        plt.plot(t, fuel)
        plt.xlabel("Time (s)")
        plt.ylabel("Fuel Mass (kg)")
        plt.title("Fuel vs Time")
        plt.grid()
        plt.savefig(os.path.join(plot_dir, "fuel.png"))
        plt.close()

        # trajectory
        logger.debug("Plotting trajectory")
        plt.figure()
        plt.plot(data[:, 1], data[:, 2], lw=1)

        circle = Circle((0, 0), radius=6380000, fill=False)
        plt.gca().add_patch(circle)

        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Trajectory")
        plt.grid()
        plt.axis("equal")
        plt.savefig(os.path.join(plot_dir, "trajectory.svg"))
        plt.close()

        # drag

        logger.debug("Plotting drag vs time")

        plt.figure()
        plt.xlabel("Time (s)")
        plt.ylabel("Drag (N)")
        plt.yscale("log")
        plt.title("Drag vs Time")
        plt.grid()
        plt.plot(t, np.clip(data[:, 6], 1e-3, np.inf))
        plt.savefig(os.path.join(plot_dir, "drag.png"))
        plt.close()

        logger.debug("Finished plotting flight data")