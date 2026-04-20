# Rocket Flight Simulator (v0.2)

2D rocket flight simulation using a drag model, variable rocket conditions, and Euler integration.

---

## Features

- 2D vector-based motion and physics
- Basic drag model (including transonic drag divergence)
- Variable environmental conditions based on location of rocket
- Thrust-based propulsion model
- Fuel-limited engine burn
- Euler integration
- npy, svg, csv, and png logging of flight data

---

## Physics Assumptions

- 2D motion only
- Drag based on realistic constant calculations, not simulated fluid flow
- Atmospheric pressure determined by altitude and atmospheric layer alone
- Constant mass flow rate
- Instant throttle response
- Simple Euler integration

---

## How to Run

```bash
python main.py
