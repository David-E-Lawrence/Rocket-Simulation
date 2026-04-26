import os
from services.physics import Physics
from models.rocket import Rocket
import models.environment as environment
from services.flight_logger import Flight_Logger
from services.plot_flight import plot
from datetime import datetime
from services.analyze_flight import analyze
import numpy as np
import json
from services.logger import get_logger

if __name__ == "__main__":

    start_time=datetime.now()

    # importing config

    with open("config.json", "r") as f:
        config=json.load(f)

    # initializing logger

    run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = f"runs/run_{run_id}"

    try:
        os.makedirs(run_dir)

        run_dir_exists = False
    except FileExistsError:
        run_dir_exists = True

    logger, listener = get_logger(config, run_dir)

    if run_dir_exists:
        logger.warning("Run directory already exists, logs may be overwritten")

    del run_dir_exists

    # setting constants

    logger.debug("Setting constants for simulation")

    t=0
    dt=config["dt"]
    progress_interval=config["progress_interval"]

    # instantiate classes

    logger.debug("Instantiating classes for simulation")

    physics=Physics()
    env=environment.Earth()
    rocket=Rocket(start_position=np.array([0.0, env.planetary_radius+1]), dry_mass=156500, fuel_mass=410900, max_thrust=(7562000*2.578), mass_flow_rate=2300)

    # setting starting state

    logger.debug("Setting starting state for simulation")

    rocket.throttle=1

    # simulation loop

    logger.info("Starting simulation")

    with Flight_Logger(run_dir) as flight_logger:
        while True:
 
            # this is a guidance algorithm that attempts to reach a low earth orbit where drag will eventually cause the rocket to deorbit
            rocket.heading=np.pi/2-1.5*((np.pi/2)*(min(t,700)/170))

            # this is to log drag each step; it will be made more streamline in future versions as to not require recording it seperately from the rocket
            drag = physics.step(dt=dt, rocket=rocket, env=env)

            # this closes out each simulation loop
            flight_logger.log(t, rocket.pos.copy(), rocket.v.copy(), rocket.fuel_mass, drag, np.linalg.norm(rocket.pos)-env.planetary_radius)
            t+=dt
            if t%progress_interval<=dt:
                logger.info(f"Simulation time: {round(t)}s")
            logger.debug(f"Simulation time: {t}")
    
            if env.alt(rocket.pos) < 0:
                logger.info("Rocket has impacted the ground")
                break
            if (datetime.now()-start_time).total_seconds() >= config["max_run_time"]:
                logger.info("Maximum runtime reached")
                break
            if t >= config["max_sim_time"]:
                logger.info("Maximum time simulated reached")
                break

    logger.info("Simulation complete")

    # plot the results

    plot_dir=os.path.join(run_dir, "plots")

    try:
        os.mkdir(plot_dir)
    except FileExistsError:
        logger.warning("Plot directory already exists")

    plot(run_dir, plot_dir)

    # analyze the results

    analyze(run_dir)

    logger.info(f"Total runtime: {datetime.now()-start_time}")

    # Stop the logging listener
    logger.info("Stopping logging listener")

    listener.stop()