import numpy as np

class Rocket:
    def __init__(self, start_position, dry_mass, fuel_mass, max_thrust, mass_flow_rate):
        self.pos=start_position # m
        self.v=np.array([0.0,0.0]) # m/s
        self.dry_mass=dry_mass # kg
        self.fuel_mass=fuel_mass # kg
        self.max_thrust=max_thrust # N
        self.mass_flow_rate=mass_flow_rate # kg/s
        self.throttle=0 # [0, 1]
        self.heading=np.pi/2 # radians
        self.cross_section=10.5 # m^2
        self.side_area=256 # m^2
    # this determines the cross sectional area of the rocket based on its directional travel in relation to the angle at which it is facing
    def get_cross_sectional_area(self):
        heading_vector=np.array([np.cos(self.heading), np.sin(self.heading)])
        
        if np.linalg.norm(self.v)==0:
            return 0
        theta=np.abs(np.arccos(
            np.dot(self.v, heading_vector)/
            (np.linalg.norm(self.v)*np.linalg.norm(heading_vector))
            ))
        
        end_area=self.cross_section*np.abs(np.cos(theta))
        side_area=self.side_area*np.abs(np.sin(theta))
        area=end_area+side_area
        return area
    # this finds the constant for drag based on the rocket's speed relative to sound, modeled with significant drag at transonic speeds
    def Cd(self, mach):
        return (
        0.25
        + 0.3 * np.exp(-((mach - 1.0)/0.25)**2)
        + 0.05 / (1 + mach)
        )