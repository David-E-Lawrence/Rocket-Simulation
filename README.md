# Rocket Flight Simulator (v0.1)

1D rocket flight simulation using Euler integration, thrust, gravity, and fuel consumption.

---

## Features

- 1D vertical motion
- Thrust-based propulsion model
- Fuel-limited engine burn
- Euler integration
- CSV and PNG logging of flight data

---

## Physics Assumptions

- Earth gravity (9.81 m/s^2); does not account for distance from center of gravity
- No atmospheric drag
- 1D vertical motion only
- Constant mass flow rate
- Instant throttle response
- Simple Euler integration

---

## How to Run

```bash
python main.py