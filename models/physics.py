import numpy as np

class Physics:
    def __init__(self):
        self.G=6.67430e-11 # m^3 kg^-1 s^-2
    def step(self, dt, rocket, env):

        # collecting relevant data

        m=rocket.state["dry_mass"]+rocket.state["fuel_mass"] # kg
        fuel_consumption=rocket.state["throttle"]*rocket.state["mass_flow_rate"] # kg/s
        fuel_consumed=min(fuel_consumption*dt, rocket.state["fuel_mass"]) # kg; this is utilized to ensure thrust stops before fuel goes negative
        thrust_scalar=fuel_consumed/(rocket.state["mass_flow_rate"]*dt)*rocket.state["max_thrust"] # N
        thrust=np.array([thrust_scalar*np.cos(rocket.state["heading"]), thrust_scalar*np.sin(rocket.state["heading"])]) # vector (tx, ty) in N
        v=rocket.state["v"]
        pos=rocket.state["pos"]
        fuel_mass=rocket.state["fuel_mass"]

        # evaluate forces acting on rocket
        v+=dt*thrust/m
        drag=self.find_drag(rocket, env)
        v+=dt*drag/m
        v+=dt*self.gravity(rocket, env)
        # update position
        pos+=v*dt

        # update fuel mass

        fuel_mass-=fuel_consumed

        # update rocket state

        rocket.state["pos"]=pos
        rocket.state["v"]=v
        rocket.state["fuel_mass"]=fuel_mass
        
        return np.linalg.norm(drag)
    def find_drag(self,rocket, env):

        # collecting relevant variables
        air_density=env.air_density(rocket.state["pos"])
        if air_density<1e-11:
            return 0
        cross_sectional_area=rocket.get_cross_sectional_area()
        cd=rocket.Cd(np.linalg.norm(rocket.state["v"])/env.mach(rocket.state["pos"]))

        # this is based on a basic drag equation: https://en.wikipedia.org/wiki/Drag_equation
        drag=-(1/2)*air_density*cd*cross_sectional_area*np.linalg.norm(rocket.state["v"])*rocket.state["v"]

        return drag
    
    # this is based on the gravity equation, utilized to account for diminishing gravity as the rocket gets further from the center of the earth
    def gravity(self, rocket, env):
        r=np.linalg.norm(rocket.state["pos"])
        direction=-(rocket.state["pos"]/np.linalg.norm(rocket.state["pos"]))
        m1=env.m
        g=direction*self.G*m1/(r**2)

        return g