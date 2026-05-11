# physics.py — Drone physics
#
# This file handles how the drone moves.
# It is kept separate from the graphics so we can test it easily.

GRAVITY    = -9.8   # gravity pulls the drone down (negative = downward)
THRUST     = 15.0   # how powerful the motors are
DRAG       = 0.9    # fraction of speed kept each frame (air resistance)
DRONE_HALF = 0.25   # half the drone's size (scale is 0.5)


class DronePhysics:
    """
    Keeps track of where the drone is and how fast it's moving.

    Position:  x (left/right),  y (up/down),  z (forward/back)
    Velocity:  vx, vy, vz  — speed in each direction
    """

    def __init__(self):
        # Start the drone in the air so it doesn't immediately hit the ground
        self.x  = 0.0
        self.y  = 5.0
        self.z  = 0.0
        self.vx = 0.0   # not moving left or right
        self.vy = 0.0   # not moving up or down
        self.vz = 0.0   # not moving forward or back

        # Obstacles: each is (center_x, center_y, center_z, half_x, half_y, half_z)
        self.obstacles = []

    def update(self, thrust, move_x, move_z, dt):
        """
        Update the drone every frame.

        thrust  — 0.0 (off) to 1.0 (full power)
        move_x  — -1 (left), 0 (still), +1 (right)
        move_z  — -1 (back),  0 (still), +1 (forward)
        dt      — seconds since the last frame (usually about 0.016)
        """

        # Vertical: thrust pushes up, gravity pulls down
        self.vy += (thrust * THRUST + GRAVITY) * dt

        # Horizontal: player input pushes the drone sideways
        self.vx += move_x * THRUST * 0.5 * dt
        self.vz += move_z * THRUST * 0.5 * dt

        # Drag: multiply speed by DRAG each frame so the drone slows down
        # when the player lets go of the keys
        self.vx *= DRAG
        self.vz *= DRAG

        # Move the drone based on its speed
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt

        # Stop the drone going through the floor
        if self.y < 0.5:
            self.y  = 0.5
            self.vy = 0

        # Stop the drone going through obstacles (AABB collision)
        for (cx, cy, cz, hx, hy, hz) in self.obstacles:
            ox = (DRONE_HALF + hx) - abs(self.x - cx)
            oy = (DRONE_HALF + hy) - abs(self.y - cy)
            oz = (DRONE_HALF + hz) - abs(self.z - cz)
            if ox > 0 and oy > 0 and oz > 0:
                # Push out along the axis with the smallest overlap
                if ox <= oy and ox <= oz:
                    self.x += ox if self.x > cx else -ox
                    self.vx = 0
                elif oy <= ox and oy <= oz:
                    self.y += oy if self.y > cy else -oy
                    self.vy = 0
                else:
                    self.z += oz if self.z > cz else -oz
                    self.vz = 0
