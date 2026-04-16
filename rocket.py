class Rocket:
    def __init__(self, y_start, dry_mass, fuel_mass, max_thrust, mass_flow_rate):
        self.y=y_start # m
        self.vy=0 # m/s
        self.dry_mass=dry_mass # kg
        self.fuel_mass=fuel_mass # kg
        self.max_thrust=max_thrust # N
        self.mass_flow_rate=mass_flow_rate # kg/s
        self.throttle=0 # [0, 1]