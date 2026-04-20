# Drone Simulator — Project Guide

A 3D drone simulator built with Python and Ursina, created as a parent + kid learning project!

---

## Project structure

```
drone-sim/
├── main.py          ← the game (run this!)
├── physics.py       ← all the movement math (gravity, thrust, drag)
├── requirements.txt ← Python packages needed
├── tests/
│   └── test_physics.py  ← automated tests for the physics
└── CLAUDE.md        ← this file
```

---

## How to install and run

### 1. Make sure Python 3.9+ is installed

```bash
python --version   # should print Python 3.9 or newer
```

### 2. Install the dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **ursina** — the 3D game engine that draws everything
- **pytest** — the testing tool

### 3. Run the simulator

```bash
python main.py
```

A window will open and you're flying!

---

## Controls

| Key       | Action              |
|-----------|---------------------|
| W         | Fly forward         |
| S         | Fly backward        |
| A         | Strafe left         |
| D         | Strafe right        |
| Space     | Thrust up           |
| Shift     | Reduce thrust (sink)|
| Escape    | Quit                |

**Tip:** You need to hold Space to stay in the air — gravity is always pulling the drone down!

---

## Running the tests

The tests check the physics logic without opening a game window — super fast!

```bash
pytest
```

Or for more detail:

```bash
pytest -v
```

You should see all tests pass with green checkmarks. ✓

---

## How the code works (learning notes)

### physics.py
Contains the `DronePhysics` class. Every frame it:
1. Calculates the net vertical force (thrust − gravity)
2. Updates velocity based on forces
3. Applies drag (air resistance slows the drone)
4. Clamps speed so the drone can't go infinitely fast
5. Moves position based on velocity
6. Stops the drone if it hits the ground

### main.py
Contains the Ursina game setup:
- `build_world()` — creates the ground and colourful obstacle boxes
- `build_drone()` — builds the drone from simple 3D shapes
- `update()` — called every frame: reads keys, calls physics, moves the 3D model

### tests/test_physics.py
Each `test_` function checks one behaviour, like:
- Does gravity pull the drone down?
- Does full thrust make it go up?
- Can it pass through the floor? (it shouldn't!)

---

## Ideas for what to add next

- Score points for flying through rings
- Wind that pushes the drone sideways
- A mini-map in the corner
- Sound effects for the motors
- Day/night cycle
- A second drone that follows you
