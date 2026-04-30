import os
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np
import logging

def plot(run_dir, plot_dir):

        #logger=logging.getLogger("Rocket_Simulation.Plotting")

        #logger.info("Plotting flight data")

        #logger.debug("Loading flight data for plotting")

        data = np.load(os.path.join(run_dir, "flight_log.npy"), allow_pickle=True)

        t = data[:, 0]
        altitude = data[:, 7]
        speed = np.linalg.norm(np.column_stack((data[:, 3], data[:, 4])), axis=1)
        fuel = data[:, 5]

        # altitude

        #logger.debug("Plotting altitude vs time")

        plt.figure()
        plt.plot(t, altitude)
        plt.xlabel("Time (s)")
        plt.ylabel("Altitude (m)")
        plt.title("Altitude vs Time")
        plt.grid()
        plt.savefig(os.path.join(plot_dir, "altitude.png"))
        plt.close()

        # velocity
        #logger.debug("Plotting speed vs time")
        plt.figure()
        plt.plot(t, speed)
        plt.xlabel("Time (s)")
        plt.ylabel("Speed (m/s)")
        plt.title("Speed vs Time")
        plt.grid()
        plt.savefig(os.path.join(plot_dir, "speed.png"))
        plt.close()

        # fuel
        #logger.debug("Plotting fuel vs time")
        plt.figure()
        plt.plot(t, fuel)
        plt.xlabel("Time (s)")
        plt.ylabel("Fuel Mass (kg)")
        plt.title("Fuel vs Time")
        plt.grid()
        plt.savefig(os.path.join(plot_dir, "fuel.png"))
        plt.close()

        # trajectory
        #logger.debug("Plotting trajectory")
        plt.figure()
        plt.plot(data[:, 1], data[:, 2], lw=1)

        circle = Circle((0, 0), radius=6380000, fill=False)
        plt.gca().add_patch(circle)

        xmin, xmax = data[:,1].min(), data[:,1].max()
        ymin, ymax = data[:,2].min(), data[:,2].max()

        xrange = xmax - xmin
        yrange = ymax - ymin

        # Find the larger range
        max_range = max(xrange, yrange)

        # Find centers
        xmid = (xmin + xmax) / 2
        ymid = (ymin + ymax) / 2

        # Set both axes to same size, centered
        plt.xlim(xmid - max_range/2, xmid + max_range/2)
        plt.ylim(ymid - max_range/2, ymid + max_range/2)
        
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Trajectory")
        plt.grid()
        #plt.axis("equal")
        plt.savefig(os.path.join(plot_dir, "trajectory.svg"))
        plt.close()

        # drag

        #logger.debug("Plotting drag vs time")

        plt.figure()
        plt.xlabel("Time (s)")
        plt.ylabel("Drag (N)")
        plt.yscale("log")
        plt.title("Drag vs Time")
        plt.grid()
        plt.plot(t, np.clip(data[:, 6], 1e-3, np.inf))
        plt.savefig(os.path.join(plot_dir, "drag.png"))
        plt.close()

        #logger.debug("Finished plotting flight data")

        # heading

        #logger.debug("Plotting heading")

        plt.figure()
        plt.xlabel("Time (s)")
        plt.ylabel("Heading (rad)")
        plt.title("Heading vs Time")
        plt.grid()
        plt.plot(t, data[:,8])
        plt.savefig(os.path.join(plot_dir, "heading.png"))
        plt.close()
def plot_all(run_dir, rocket_count):

        plt.figure()

        xmax=-1000
        xmin=1000
        ymax=-1000
        ymin=1000

        for i in range(rocket_count):
                print(f"{i} out of {rocket_count}")
                data=np.load(os.path.join(run_dir, f"rocket_{i}", "flight_log.npy"), allow_pickle=True)
                plt.plot(data[:, 1], data[:, 2], lw=1)

                for x in data[:,1]:
                        xmax=max(x, xmax)
                        xmin=min(x, xmin)
                for y in data[:,2]:
                        ymax=max(y,ymax)
                        ymin=min(y,ymin)

        circle = Circle((0, 0), radius=6380000, fill=False)
        plt.gca().add_patch(circle)

        xrange = (xmax - xmin)*1.3
        yrange = (ymax - ymin)*1.3

        # Find the larger range
        max_range = max(xrange, yrange)

        # Find centers
        xmid = (xmin + xmax) / 2
        ymid = (ymin + ymax) / 2

        # Set both axes to same size, centered
        plt.xlim(xmid - max_range/2, xmid + max_range/2)
        plt.ylim(ymid - max_range/2, ymid + max_range/2)
        
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Trajectory")
        plt.grid()
        #plt.axis("equal")
        plt.savefig(os.path.join(run_dir, "trajectory.svg"))
        plt.close()