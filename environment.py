import numpy as np

class Earth():
    def __init__(self):
        self.planetary_radius=6380000.0
        self.m=5.972e24
    # returns altitude in m
    def alt(self, pos):
        return np.linalg.norm(pos)-self.planetary_radius
    # this returns air density in kg/m^3
    def air_density(self, pos):
        h = self.alt(pos)

        # constants
        g = 9.80665
        R = 287.05

        # ISA base conditions
        T0 = 288.15     # K
        p0 = 101325.0   # Pa

        h = np.maximum(h, 0.0)

        # Troposphere (0–11 km)
        if h < 11000:
            L = 0.0065
            T = T0 - L * h
            p = p0 * (T / T0) ** (g / (R * L))

        # Lower stratosphere (11–20 km)
        elif h < 20000:
            T = 216.65
            p11 = p0 * (216.65 / T0) ** (g / (R * 0.0065))
            p = p11 * np.exp(-g * (h - 11000) / (R * T))

        # Above (simple continuation)
        else:
            T = 216.65
            p11 = p0 * (216.65 / T0) ** (g / (R * 0.0065))
            p20 = p11 * np.exp(-g * (20000 - 11000) / (R * T))
            p = p20 * np.exp(-g * (h - 20000) / (R * T))

        return p / (R * T)
    # this returns the speed of sound in m/s
    def mach(self, pos):
        rho = self.air_density(pos)
        return 340 * np.sqrt(rho / 1.225)