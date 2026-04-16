import csv
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


class Logger:
    def __init__(self, filename="log.csv"):
        run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.run_dir = f"runs/run_{run_id}"

        os.makedirs(self.run_dir, exist_ok=True)
        self.file=open(f"{self.run_dir}/{filename}", "w", newline="")
        
        self.writer=csv.writer(self.file)
        self.writer.writerow(["time", "altitude", "velocity", "fuel_mass"])
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    def close(self):
        self.file.close()
        self.plot()
        self.analyze()
    def log(self, time, altitude, velocity, fuel_mass):
        self.writer.writerow([time, altitude, velocity, fuel_mass])
    def analyze(self):
        data = pd.read_csv(os.path.join(self.run_dir, "log.csv"))

        # analyze data

        t = data["time"]
        max_altitude = data["altitude"].max()
        max_altitude_time = data.loc[data["altitude"].idxmax(), "time"]
        max_velocity = data["velocity"].max()
        max_velocity_time = data.loc[data["velocity"].idxmax(), "time"]

        # save analysis results

        with open(os.path.join(self.run_dir, "analysis.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["max_altitude", "max_altitude_time", "max_velocity", "max_velocity_time"])
            writer.writerow([max_altitude, max_altitude_time, max_velocity, max_velocity_time])

    def plot(self):
        data = pd.read_csv(os.path.join(self.run_dir, "log.csv"))

        t = data["time"]
        y = data["altitude"]
        v = data["velocity"]
        fuel = data["fuel_mass"]

        # altitude
        plt.figure()
        plt.plot(t, y)
        plt.xlabel("Time (s)")
        plt.ylabel("Altitude (m)")
        plt.title("Altitude vs Time")
        plt.grid()
        plt.savefig(os.path.join(self.run_dir, "altitude.png"))
        plt.close()

        # velocity
        plt.figure()
        plt.plot(t, v)
        plt.xlabel("Time (s)")
        plt.ylabel("Velocity (m/s)")
        plt.title("Velocity vs Time")
        plt.grid()
        plt.savefig(os.path.join(self.run_dir, "velocity.png"))
        plt.close()

        # fuel
        plt.figure()
        plt.plot(t, fuel)
        plt.xlabel("Time (s)")
        plt.ylabel("Fuel Mass (kg)")
        plt.title("Fuel vs Time")
        plt.grid()
        plt.savefig(os.path.join(self.run_dir, "fuel.png"))
        plt.close()