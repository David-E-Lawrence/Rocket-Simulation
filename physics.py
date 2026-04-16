class Physics:
    def __init__(self):
        pass
    def step(self, dt, rocket, env):

        # collecting relevant data

        # m/s^2
        g=env.g
        # m
        y=rocket.y
        # m/s
        vy=rocket.vy
        # kg
        fuel_mass=rocket.fuel_mass
        # kg
        m=rocket.dry_mass+fuel_mass
        # N
        max_thrust=rocket.max_thrust
        # kg/s
        mass_flow_rate=rocket.mass_flow_rate
        # [0, 1] with 0 being no throttle and 1 being full throttle
        throttle=rocket.throttle
        # kg/s
        fuel_consumption=throttle*mass_flow_rate
        # kg
        fuel_consumed=min(fuel_consumption*dt, fuel_mass)
        # N
        thrust=fuel_consumed/(mass_flow_rate*dt)*max_thrust

        # evaluate forces acting on rocket
        vy-=g*dt
        vy+=dt*thrust/m
        # update position
        y+=vy*dt

        # update fuel mass

        fuel_mass-=fuel_consumed

        # update rocket state
        rocket.y=y
        rocket.vy=vy
        rocket.fuel_mass=fuel_mass