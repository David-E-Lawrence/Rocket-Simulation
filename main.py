import os
from physics import Physics
from rocket import Rocket
import environment
from flight_logger import Flight_Logger
from plot_flight import plot
from datetime import datetime
from analyze_flight import analyze
import numpy as np
import json


if __name__ == "__main__":

    start_time=datetime.now()

    # importing config

    with open("config.json", "r") as f:
        config=json.load(f)

    # setting constants

    t=0
    dt=0.01

    # instantiate classes

    physics=Physics()
    env=environment.Earth()
    rocket=Rocket(start_position=np.array([0.0, env.planetary_radius+1]), dry_mass=156500, fuel_mass=410900, max_thrust=(7562000*2.578), mass_flow_rate=2300)

    # setting starting state

    rocket.throttle=1

    # determining run folder

    run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = f"runs/run_{run_id}"
    os.makedirs(run_dir, exist_ok=True)

    # simulation loop
    with Flight_Logger(run_dir) as flight_logger:
        while env.alt(rocket.pos) >= 0 and t < config["max_sim_time"]:  # Adjust the condition as needed

            # this is a guidance algorithm that attempts to reach a low earth orbit where drag will eventually cause the rocket to deorbit
            rocket.heading=np.pi/2-1.5*((np.pi/2)*(min(t,700)/170))

            # this is to log drag each step; it will be made more streamline in future versions as to not require recording it seperately from the rocket
            drag = physics.step(dt=dt, rocket=rocket, env=env)

            # this closes out each simulation loop
            flight_logger.log(t, rocket.pos.copy(), rocket.v.copy(), rocket.fuel_mass, drag, np.linalg.norm(rocket.pos)-env.planetary_radius)
            t+=dt
            if t%1000<=dt:
                print(f"t={round(t)}")
    # plot the results
    plot(run_dir)
    analyze(run_dir)

    print(f"Total runtime: {datetime.now()-start_time}")