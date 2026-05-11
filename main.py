# main.py — Drone Simulator
#
# Run this file to play!  python main.py
#
# Controls:
#   W / S     — forward / backward
#   A / D     — left / right
#   SPACE     — thrust up
#   SHIFT     — sink down
#   ESC       — quit

from ursina import Ursina, Entity, Sky, color, Vec3, held_keys, camera, Text, window, time

from physics import DronePhysics

# --- Create the app window ---
app = Ursina(title="Drone Simulator", borderless=False)

def add_outline(entity, thickness=3):
    """Add black edge lines visible from any angle using wireframe rendering."""
    outline = Entity(model="cube", parent=entity, scale=1.001, color=color.black)
    outline.setRenderModeWireframe(thickness)


# --- World ---
# A big green ground plane
Entity(model="plane", scale=100, color=color.green)

# Three colourful obstacles to fly around
red_box    = Entity(model="cube", position=Vec3( 5, 2,  5), scale=Vec3(2, 4, 2), color=color.red)
orange_box = Entity(model="cube", position=Vec3(-6, 2, 10), scale=Vec3(2, 4, 2), color=color.orange)
cyan_box   = Entity(model="cube", position=Vec3(10, 2, -4), scale=Vec3(2, 4, 2), color=color.cyan)

add_outline(red_box)
add_outline(orange_box)
add_outline(cyan_box)

Sky()  # blue sky background

# --- Drone ---
# Just a simple grey cube for now — we can make it fancier later!
drone = Entity(model="cube", color=color.dark_gray, scale=0.5, position=Vec3(0, 5, 0))
add_outline(drone, thickness=4)

# --- Physics ---
physics = DronePhysics()

# Tell the physics about each obstacle so it can block the drone.
# Each entry: (center_x, center_y, center_z, half_width, half_height, half_depth)
physics.obstacles = [
    ( 5,  2,  5,  1, 2, 1),   # red box
    (-6,  2, 10,  1, 2, 1),   # orange box
    (10,  2, -4,  1, 2, 1),   # cyan box
]

# --- Controls hint ---
Text(
    "SPACE: up   SHIFT: down   WASD: move   ESC: quit",
    position=(0, -0.45),
    origin=(0, 0),
    color=color.white,
)

# --- update() is called automatically every frame by Ursina ---
def update():
    dt = time.dt  # time since last frame in seconds

    # Read keyboard input
    thrust = 1.0 if held_keys["space"] else 0.3 if held_keys["shift"] else 0.65
    move_x = held_keys["d"] - held_keys["a"]   # right=+1, left=-1
    move_z = held_keys["w"] - held_keys["s"]   # forward=+1, back=-1

    # Update the physics
    physics.update(thrust, move_x, move_z, dt)

    # Move the drone cube to match the physics position
    drone.position = Vec3(physics.x, physics.y, physics.z)

    # Camera follows the drone from behind and above
    camera.position = Vec3(physics.x, physics.y + 5, physics.z - 10)
    camera.look_at(drone)

app.run()
