"""
main.py — Drone Simulator

A 3D drone simulator built with Ursina game engine.
Fly around with WASD + Space + Shift!

Controls:
  W / S       — fly forward / backward
  A / D       — fly left / right
  Space       — thrust up (hold to fly!)
  Shift       — let gravity pull you down faster
  Mouse       — look around
  Escape      — quit
"""

from ursina import (
    Ursina, Entity, Sky, color, Vec3, held_keys,
    camera, Text, window, scene, time, load_texture
)
from ursina.prefabs.first_person_controller import FirstPersonController

from physics import DronePhysics, GRAVITY

# ── App setup ────────────────────────────────────────────────────────────────

app = Ursina(title="Drone Simulator", borderless=False)
window.color = color.rgb(135, 206, 235)   # sky-blue background


# ── World / landscape ────────────────────────────────────────────────────────

def build_world():
    """Create the ground and obstacles the drone flies around."""

    # Ground plane — a big flat green surface
    ground = Entity(
        model="plane",
        scale=(100, 1, 100),
        color=color.rgb(60, 160, 60),
        texture="white_cube",
        texture_scale=(50, 50),
        collider="box",
    )

    # A sky dome so it looks like we're outside
    Sky(color=color.rgb(135, 206, 235))

    # ── Obstacles ──────────────────────────────────────────────────────────
    # Each obstacle is a coloured box placed somewhere on the map.
    # The drone has to fly around (or over) them!

    obstacles = [
        # (x, y, z, scale_x, scale_y, scale_z, color)
        (  5,  2,  5,  2, 4,  2, color.red),
        ( -8,  2, 10,  3, 4,  3, color.orange),
        ( 15,  3, -5,  2, 6,  2, color.yellow),
        ( -5,  2,-12,  4, 4,  2, color.cyan),
        ( 20,  2, 15,  2, 4,  4, color.violet),
        (-15,  2,-15,  3, 6,  3, color.brown),
        (  0,  2, 20,  5, 4,  2, color.lime),
        (-20,  3,  5,  2, 6,  2, color.azure),
    ]

    for (ox, oy, oz, sx, sy, sz, col) in obstacles:
        Entity(
            model="cube",
            position=Vec3(ox, oy, oz),
            scale=Vec3(sx, sy, sz),
            color=col,
            collider="box",
        )

    return ground


build_world()


# ── Drone visual ─────────────────────────────────────────────────────────────

def build_drone():
    """
    Build the drone model out of simple shapes.
    It's a small body with four arms sticking out.
    """
    # Central body
    body = Entity(
        model="cube",
        color=color.dark_gray,
        scale=Vec3(0.4, 0.15, 0.4),
        position=Vec3(0, 5, 0),
    )

    arm_color = color.gray
    arm_positions = [
        Vec3( 0.5, 0,  0.5),
        Vec3(-0.5, 0,  0.5),
        Vec3( 0.5, 0, -0.5),
        Vec3(-0.5, 0, -0.5),
    ]

    # Four arms
    for pos in arm_positions:
        Entity(
            model="cube",
            color=arm_color,
            scale=Vec3(0.6, 0.06, 0.06),
            position=body.position + pos,
            parent=body,
        )

    # Four propeller discs (flat circles approximated with thin cubes)
    prop_color = color.rgba(100, 200, 255, 180)
    for pos in arm_positions:
        Entity(
            model="cube",
            color=prop_color,
            scale=Vec3(0.3, 0.02, 0.3),
            position=pos * 1.5,
            parent=body,
        )

    return body


drone_entity = build_drone()


# ── Physics ───────────────────────────────────────────────────────────────────

# Create the physics object starting at the same position as our drone visual
drone_physics = DronePhysics(x=0, y=5, z=0)


# ── Camera ────────────────────────────────────────────────────────────────────

# We'll use a simple third-person follow camera.
# The camera will smoothly chase the drone from behind and above.
camera.parent = scene            # detach from any default parent
camera.position = Vec3(0, 7, -10)
camera.rotation = Vec3(15, 0, 0)

# How quickly the camera catches up to the drone (0=instant, 1=never)
CAMERA_LAG = 0.08


# ── HUD (heads-up display) ────────────────────────────────────────────────────

hud_altitude  = Text("Altitude: 0 m",  position=(-0.85,  0.45), scale=1.2, color=color.white)
hud_speed     = Text("Speed: 0 m/s",   position=(-0.85,  0.40), scale=1.2, color=color.white)
hud_controls  = Text(
    "W/S: Forward/Back   A/D: Left/Right\n"
    "SPACE: Thrust Up    SHIFT: Down\n"
    "ESC: Quit",
    position=(-0.85, -0.38), scale=0.9, color=color.rgba(255, 255, 255, 180),
)


# ── Propeller spin ────────────────────────────────────────────────────────────

propeller_spin = 0.0   # current rotation angle of the propellers


# ── Main update loop ──────────────────────────────────────────────────────────

def update():
    """
    This function is called every frame by Ursina (about 60 times per second).
    It reads keyboard input, updates physics, and moves the drone visual.
    """
    global propeller_spin

    dt = time.dt   # time since last frame in seconds (usually ~0.016)

    # ── Read keyboard input ──────────────────────────────────────────────

    # Thrust: space = full thrust, shift = no thrust (let gravity win)
    if held_keys["space"]:
        thrust = 1.0
    elif held_keys["shift"]:
        thrust = 0.3   # reduced thrust → gravity pulls drone down
    else:
        thrust = 0.65  # just enough to almost hover — need a little space to stay up

    # Horizontal movement relative to the drone's current facing direction.
    # We keep it simple: W/S = world Z, A/D = world X.
    move_x = 0.0
    move_z = 0.0

    if held_keys["d"]:
        move_x += 1.0
    if held_keys["a"]:
        move_x -= 1.0
    if held_keys["w"]:
        move_z += 1.0
    if held_keys["s"]:
        move_z -= 1.0

    # Normalize diagonal movement so it's not faster
    if move_x != 0 and move_z != 0:
        move_x *= 0.707
        move_z *= 0.707

    # ── Update physics ───────────────────────────────────────────────────

    drone_physics.update(thrust, move_x, move_z, dt)
    px, py, pz = drone_physics.get_position()

    # ── Move the 3D drone to match the physics position ──────────────────

    drone_entity.position = Vec3(px, py, pz)

    # Tilt the drone slightly in the direction of movement (looks cool!)
    vx, vy, vz = drone_physics.get_velocity()
    drone_entity.rotation_z = -vx * 3    # roll left/right
    drone_entity.rotation_x =  vz * 3    # pitch forward/back

    # ── Spin the propellers ──────────────────────────────────────────────

    propeller_spin += 720 * dt   # spin speed in degrees per second
    for child in drone_entity.children:
        # Propellers are the thin flat ones (scale_y very small)
        if child.scale_y < 0.05:
            child.rotation_y = propeller_spin

    # ── Follow camera ────────────────────────────────────────────────────

    # Target position: behind and above the drone
    target_cam_pos = Vec3(px, py + 4, pz - 8)

    # Lerp = smoothly move toward the target (feels less jarring)
    camera.position = camera.position + (target_cam_pos - camera.position) * CAMERA_LAG * 60 * dt
    camera.look_at(drone_entity.position + Vec3(0, 1, 0))

    # ── Update HUD ───────────────────────────────────────────────────────

    speed_horizontal = (vx**2 + vz**2) ** 0.5
    hud_altitude.text  = f"Altitude:  {py:.1f} m"
    hud_speed.text     = f"Speed:     {speed_horizontal:.1f} m/s"


# ── Run the app ───────────────────────────────────────────────────────────────

app.run()
