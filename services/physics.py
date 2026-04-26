import numpy as np
import logging

class Physics:
    def __init__(self):
        self.G=6.67430e-11 # m^3 kg^-1 s^-2
        self.logger=logging.getLogger("Rocket_Simulation.Physics")
        print(__name__)
    def step(self, dt, rocket, env):

        # collecting relevant data

        self.logger.debug("Collecting relevant data for physics step")

        pos=rocket.pos.copy() # vector (x, y) in m
        v=rocket.v.copy() # vector (vx, vy) in m/s
        fuel_mass=rocket.fuel_mass # kg
        m=rocket.dry_mass+fuel_mass # kg
        max_thrust=rocket.max_thrust # N
        mass_flow_rate=rocket.mass_flow_rate # kg/s
        throttle=rocket.throttle # [0, 1] with 1 being full throttle
        fuel_consumption=throttle*mass_flow_rate # kg/s
        fuel_consumed=min(fuel_consumption*dt, fuel_mass) # kg; this is utilized to ensure thrust stops before fuel goes negative
        thrust_scalar=fuel_consumed/(mass_flow_rate*dt)*max_thrust # N
        thrust=np.array([thrust_scalar*np.cos(rocket.heading), thrust_scalar*np.sin(rocket.heading)]) # vector (tx, ty) in N
        # evaluate forces acting on rocket
        v+=dt*thrust/m
        drag=self.find_drag(rocket, env)
        v+=dt*drag/m
        v+=dt*self.gravity(rocket, env)
        # update position
        pos+=v*dt

        # update fuel mass

        self.logger.debug("Updating fuel mass for physics step")

        fuel_mass-=fuel_consumed

        # update rocket state

        self.logger.debug("Updating rocket state for physics step")

        rocket.pos=pos
        rocket.v=v
        rocket.fuel_mass=fuel_mass
        
        return np.linalg.norm(drag)
    def find_drag(self,rocket, env):

        self.logger.debug("Calculating drag for physics step")

        # collecting relevant variables
        air_density=env.air_density(rocket.pos)
        cross_sectional_area=rocket.get_cross_sectional_area()
        cd=rocket.Cd(np.linalg.norm(rocket.v)/env.mach(rocket.pos))

        # this is based on a basic drag equation: https://en.wikipedia.org/wiki/Drag_equation
        drag=-(1/2)*air_density*cd*cross_sectional_area*np.linalg.norm(rocket.v)*rocket.v

        return drag
    
    # this is based on the gravity equation, utilized to account for diminishing gravity as the rocket gets further from the center of the earth
    def gravity(self, rocket, env):

        self.logger.debug("Calculating gravity for physics step")
        r=np.linalg.norm(rocket.pos)
        direction=-(rocket.pos/np.linalg.norm(rocket.pos))
        m1=env.m
        g=direction*self.G*m1/(r**2)

        return g