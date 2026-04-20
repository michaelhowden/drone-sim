# tests/test_physics.py — Tests for the drone physics
#
# These tests check the physics math without needing a game window.
# Run them with:  pytest

from physics import DronePhysics


def simulate(physics, thrust, move_x, move_z, seconds):
    """Run the physics for a given number of seconds (at 60 fps)."""
    dt = 1 / 60
    for _ in range(int(seconds * 60)):
        physics.update(thrust, move_x, move_z, dt)


def test_drone_starts_in_the_air():
    """Drone should start above the ground."""
    p = DronePhysics()
    assert p.y > 0


def test_gravity_pulls_drone_down():
    """With no thrust, the drone should fall."""
    p = DronePhysics()
    start_y = p.y
    simulate(p, thrust=0.0, move_x=0, move_z=0, seconds=1)
    assert p.y < start_y


def test_thrust_lifts_drone():
    """Full thrust should make the drone rise."""
    p = DronePhysics()
    start_y = p.y
    simulate(p, thrust=1.0, move_x=0, move_z=0, seconds=1)
    assert p.y > start_y


def test_drone_does_not_fall_through_floor():
    """The drone should never go below y=0.5."""
    p = DronePhysics()
    simulate(p, thrust=0.0, move_x=0, move_z=0, seconds=5)
    assert p.y >= 0.5


def test_drone_moves_forward():
    """move_z=1 should move the drone forward (increasing z)."""
    p = DronePhysics()
    simulate(p, thrust=1.0, move_x=0, move_z=1, seconds=1)
    assert p.z > 0


def test_drone_moves_sideways():
    """move_x=1 should move the drone to the right (increasing x)."""
    p = DronePhysics()
    simulate(p, thrust=1.0, move_x=1, move_z=0, seconds=1)
    assert p.x > 0
