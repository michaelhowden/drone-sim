"""
tests/test_physics.py — Tests for the drone physics

These tests check that the physics math is correct WITHOUT needing
a window or graphics — super fast to run!

Run them with:  pytest
"""

import pytest
from physics import DronePhysics, GRAVITY, MAX_SPEED, HOVER_THRUST


# ── Helpers ───────────────────────────────────────────────────────────────────

def simulate(drone, thrust, move_x, move_z, seconds, dt=0.016):
    """Helper: run the physics for a number of seconds at a fixed frame rate."""
    steps = int(seconds / dt)
    for _ in range(steps):
        drone.update(thrust, move_x, move_z, dt)


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestDronePhysics:

    def test_initial_position(self):
        """Drone starts at the position we give it."""
        drone = DronePhysics(x=1, y=10, z=3)
        assert drone.x == 1.0
        assert drone.y == 10.0
        assert drone.z == 3.0

    def test_initial_velocity_is_zero(self):
        """Drone starts with no movement."""
        drone = DronePhysics()
        vx, vy, vz = drone.get_velocity()
        assert vx == 0.0
        assert vy == 0.0
        assert vz == 0.0

    def test_gravity_pulls_drone_down(self):
        """With no thrust, the drone falls down."""
        drone = DronePhysics(y=20)
        initial_y = drone.y

        # No thrust at all — gravity wins
        simulate(drone, thrust=0.0, move_x=0, move_z=0, seconds=1.0)

        assert drone.y < initial_y, "Drone should fall when there's no thrust"

    def test_full_thrust_lifts_drone(self):
        """With full thrust, the drone should rise."""
        drone = DronePhysics(y=5)
        initial_y = drone.y

        simulate(drone, thrust=1.0, move_x=0, move_z=0, seconds=1.0)

        assert drone.y > initial_y, "Full thrust should lift the drone"

    def test_drone_doesnt_fall_through_floor(self):
        """The drone must not go below y=0.5 (the ground level)."""
        drone = DronePhysics(y=1)

        # No thrust — free fall for a long time
        simulate(drone, thrust=0.0, move_x=0, move_z=0, seconds=5.0)

        assert drone.y >= 0.5, "Drone should never go below the ground"

    def test_forward_movement(self):
        """Pressing W (move_z=1) should move the drone forward."""
        drone = DronePhysics(y=10)
        initial_z = drone.z

        # Full thrust to stay up, and move forward
        simulate(drone, thrust=1.0, move_x=0, move_z=1.0, seconds=1.0)

        assert drone.z > initial_z, "Drone should move forward with move_z=1"

    def test_backward_movement(self):
        """Pressing S (move_z=-1) should move the drone backward."""
        drone = DronePhysics(y=10)
        initial_z = drone.z

        simulate(drone, thrust=1.0, move_x=0, move_z=-1.0, seconds=1.0)

        assert drone.z < initial_z, "Drone should move backward with move_z=-1"

    def test_left_right_movement(self):
        """A and D keys should move the drone left and right."""
        drone_right = DronePhysics(y=10)
        drone_left  = DronePhysics(y=10)

        simulate(drone_right, thrust=1.0, move_x= 1.0, move_z=0, seconds=1.0)
        simulate(drone_left,  thrust=1.0, move_x=-1.0, move_z=0, seconds=1.0)

        assert drone_right.x > 0, "Drone should move right with move_x=1"
        assert drone_left.x  < 0, "Drone should move left with move_x=-1"

    def test_speed_is_capped(self):
        """The drone's speed should never exceed MAX_SPEED."""
        drone = DronePhysics(y=10)

        # Apply movement for a long time to try to exceed max speed
        simulate(drone, thrust=1.0, move_x=1.0, move_z=1.0, seconds=10.0)

        vx, vy, vz = drone.get_velocity()
        assert abs(vx) <= MAX_SPEED, f"vx={vx:.2f} exceeded MAX_SPEED={MAX_SPEED}"
        assert abs(vy) <= MAX_SPEED, f"vy={vy:.2f} exceeded MAX_SPEED={MAX_SPEED}"
        assert abs(vz) <= MAX_SPEED, f"vz={vz:.2f} exceeded MAX_SPEED={MAX_SPEED}"

    def test_drag_slows_drone(self):
        """After releasing the controls, the drone should slow down."""
        drone = DronePhysics(y=10)

        # Get the drone moving fast
        simulate(drone, thrust=1.0, move_x=1.0, move_z=0, seconds=2.0)
        speed_after_input = abs(drone.vx)

        # Release the controls — only hover thrust
        simulate(drone, thrust=0.65, move_x=0, move_z=0, seconds=2.0)
        speed_after_release = abs(drone.vx)

        assert speed_after_release < speed_after_input, \
            "Drone should slow down when controls are released (drag)"

    def test_get_position_returns_tuple(self):
        """get_position() should return a tuple of three numbers."""
        drone = DronePhysics(x=1, y=2, z=3)
        pos = drone.get_position()
        assert isinstance(pos, tuple)
        assert len(pos) == 3
        assert pos == (1.0, 2.0, 3.0)

    def test_get_velocity_returns_tuple(self):
        """get_velocity() should return a tuple of three numbers."""
        drone = DronePhysics()
        vel = drone.get_velocity()
        assert isinstance(vel, tuple)
        assert len(vel) == 3
