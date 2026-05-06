import numpy as np

class Rocket:
    def __init__(self, state, controller):
        self.state={
            "pos": state["pos"],
            "v": np.array([0.0,0.0]),
            "dry_mass": state["dry_mass"],
            "fuel_mass": state["fuel_mass"],
            "max_thrust": state["max_thrust"],
            "mass_flow_rate": state["mass_flow_rate"],
            "throttle": 0.3,
            "heading": np.pi/2,
        }

        self.cross_section=10.5 # m^2
        self.side_area=256 # m^2

        self.controller=controller

    # this determines the cross sectional area of the rocket based on its directional travel in relation to the angle at which it is facing
    def get_cross_sectional_area(self):

        assert not np.isnan(np.cos(self.state["heading"]))
        assert not np.isnan(np.sin(self.state["heading"]))

        heading_vector=np.array([np.cos(self.state["heading"]), np.sin(self.state["heading"])])

        if np.linalg.norm(self.state["v"])==0:
            return 0
        theta=np.abs(
            np.arccos(
                np.clip(
                    np.dot(self.state["v"], heading_vector)/(np.linalg.norm(self.state["v"])*np.linalg.norm(heading_vector)),
                    -1, 1
        )))
        
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
    def assert_heading(self):
        self.state["heading"]=self.controller(self.state)