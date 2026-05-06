import os
from models.controller import Controller
from models.physics import Physics
from models.rocket import Rocket
import models.environment as environment
from services.flight_logger import Flight_Logger
from services.plot_flight import plot, plot_all
from datetime import datetime
import numpy as np
import json
from concurrent.futures import ProcessPoolExecutor
from services.analyze_flight import analyze

def step_rocket(physics, rocket, flight_logger, env, dt, t):
    rocket.assert_heading()
    drag = physics.step(dt, rocket, env)
    flight_logger.log(t, rocket.state["pos"].copy(), rocket.state["v"].copy(), rocket.state["fuel_mass"], drag, np.linalg.norm(rocket.state["pos"])-env.planetary_radius, rocket.state["heading"])

def simulate_rocket(i, config, run_dir):
    physics=Physics()
    env=environment.Earth()

    rocket=Rocket(
            {
                "pos": np.array([0.0, env.planetary_radius+1]),
                "dry_mass": 156500,
                "fuel_mass": 410900,
                "max_thrust": 7562000*3.6,
                "mass_flow_rate": 2300,
            },
            controller=Controller(i, config["rocket_count"], env)
        )
    rocket_dir=os.path.join(run_dir, f"rocket_{i}")

    flight_logger=Flight_Logger(rocket_dir, i)
    os.makedirs(rocket_dir)

    start_time=datetime.now()
    t=0
    dt=config["dt"]

    while True:
        step_rocket(physics, rocket, flight_logger, env, dt, t)

        t+=dt
    
        if env.alt(rocket.state["pos"]) < 0:
            break
        if (datetime.now()-start_time).total_seconds() >= config["max_run_time"]:
            break
        if t >= config["max_sim_time"]:
            break
    flight_logger.save()
    del flight_logger.data

    plot_dir=os.path.join(flight_logger.run_dir, "plots")

    try:
        os.mkdir(plot_dir)
    except FileExistsError:
        pass

    plot(flight_logger.run_dir, plot_dir)
    analyze(rocket_dir)

if __name__ == "__main__":

    # importing config

    with open("config.json", "r") as f:
        config=json.load(f)

    run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = f"runs/run_{run_id}"

    os.makedirs(run_dir, exist_ok=True)

    # simulation loop
    print("simulating rockets")
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(
            simulate_rocket,
            range(config["rocket_count"]),
            [config] * config["rocket_count"],
            [run_dir] * config["rocket_count"]
        )

    print("Plotting rocket flights")
    plot_all(run_dir, config["rocket_count"])