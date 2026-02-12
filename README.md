# Planetary Projectile Motion Simulator

A Python-based interactive projectile motion simulator with planet-based gravity selection, aerodynamic drag, and animated visualization.

This project simulates projectile motion on different planets and visualizes the trajectory using real-time animation with Matplotlib.

---

## Features

- Planet selection (Earth, Moon, Mars, Jupiter, etc.)
- Adjustable parameters:
  - Initial velocity
  - Launch angle
  - Initial position
  - Object mass
  - Aerodynamic drag coefficient
- Optional air resistance (quadratic drag model)
- Real-time animation
- Maximum height and range visualization
- Background planet image support
- Object selection (ball, arrow, rocket, or default marker)

---

## Physics Model

The simulation is based on:

- Newton’s Second Law
- Euler numerical integration
- Quadratic air resistance

Drag force formula:

```
F_drag = k * v^2
```

Where:

- g = planetary gravity  
- k = drag coefficient  
- m = object mass  
- v = velocity magnitude  

---

## Simulation Outputs

The simulator calculates:

- Total flight time
- Maximum height
- Horizontal range
- Real-time trajectory
- Markers for:
  - Start point
  - Landing point
  - Maximum height

---

## Project Structure

```
project-folder/
|
|-- main.py
|-- requirements.txt
|-- images/
|   |-- earth.jpg
|   |-- mars.jpg
|   |-- moon.jpg
|   |-- ball.png
|   |-- arrow.png
|   |-- rocket.png
|-- README.md
```

If planet images are not found, the simulator automatically uses background colors instead.

---

## Installation

Clone the repository:

```
git clone https://github.com/yourusername/project-name.git
cd project-name
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the project:

```
python main.py
```

---

## Tech Stack

- Python
- NumPy
- Matplotlib

---

## Future Improvements

- Replace Euler method with Runge-Kutta (RK4)
- Add wind model
- Extend to 3D simulation
- Convert to GUI application
- Build a web-based version

---

## Educational Purpose

Suitable for:

- Physics students
- Engineering fundamentals
- Numerical methods practice
- Scientific computing visualization
