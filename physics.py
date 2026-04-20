"""
physics.py — Drone physics simulation

This module handles all the math for how the drone moves.
Keeping it separate from the graphics code makes it easy to test!
"""

# How strong gravity pulls the drone down (meters per second squared)
GRAVITY = -9.8

# Maximum speed the drone can reach in any direction
MAX_SPEED = 10.0

# How much the drone slows down when you stop pressing keys (air resistance)
DRAG = 0.85

# How powerful the drone's motors are
THRUST_POWER = 15.0

# How much thrust is needed just to hover in place
HOVER_THRUST = 9.8


class DronePhysics:
    """
    Tracks the drone's position and velocity, and updates them each frame.

    Think of this like the drone's "brain" for movement — it knows where
    the drone is and how fast it's going in each direction (x, y, z).
    """

    def __init__(self, x=0, y=5, z=0):
        # Starting position of the drone
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

        # Velocity — how fast the drone is moving in each direction
        # Positive y = moving up, negative y = moving down
        self.vx = 0.0  # left/right speed
        self.vy = 0.0  # up/down speed
        self.vz = 0.0  # forward/backward speed

    def update(self, thrust, move_x, move_z, dt):
        """
        Update the drone's position based on controls and physics.

        Parameters:
            thrust  — how hard the motors are pushing up (0.0 to 1.0)
            move_x  — left/right input (-1 = left, +1 = right)
            move_z  — forward/backward input (-1 = back, +1 = forward)
            dt      — time since last frame (delta time), in seconds

        This runs every single frame, like a heartbeat for the drone.
        """
        # --- Apply thrust (fighting against gravity) ---
        # When thrust is 1.0, we apply THRUST_POWER upward
        # Gravity always pulls down (GRAVITY is negative)
        thrust_force = thrust * THRUST_POWER
        vertical_acceleration = thrust_force + GRAVITY
        self.vy += vertical_acceleration * dt

        # --- Apply horizontal movement ---
        # Player input directly changes horizontal velocity
        self.vx += move_x * THRUST_POWER * 0.5 * dt
        self.vz += move_z * THRUST_POWER * 0.5 * dt

        # --- Apply drag (air resistance slows the drone down) ---
        # Multiply by DRAG each frame so the drone naturally slows to a stop
        # We only apply horizontal drag so gravity still works properly
        drag_factor = DRAG ** dt  # works correctly at any frame rate
        self.vx *= drag_factor
        self.vz *= drag_factor

        # Slow vertical speed too, but less — feels more natural
        self.vy *= (drag_factor * 0.98 + 0.02)

        # --- Clamp speed so the drone doesn't go infinitely fast ---
        self.vx = max(-MAX_SPEED, min(MAX_SPEED, self.vx))
        self.vy = max(-MAX_SPEED, min(MAX_SPEED, self.vy))
        self.vz = max(-MAX_SPEED, min(MAX_SPEED, self.vz))

        # --- Move the drone based on its velocity ---
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt

        # --- Ground collision — don't go through the floor! ---
        if self.y < 0.5:
            self.y = 0.5
            # Stop downward movement when hitting the ground
            if self.vy < 0:
                self.vy = 0

    def get_position(self):
        """Return the drone's current position as a tuple (x, y, z)."""
        return (self.x, self.y, self.z)

    def get_velocity(self):
        """Return the drone's current velocity as a tuple (vx, vy, vz)."""
        return (self.vx, self.vy, self.vz)
