from modal_properties import calculate_modal_properties, calculate_modal_forces
from train_properties import calculate_train_vector
from newmarks_method import newmark_time_integration
import numpy as np

MASS = 18000


def test_calculate_modal_properties():
    (
        modal_mass,
        modal_damping,
        modal_stiffness,
        circular_frequency,
    ) = calculate_modal_properties(
        mass=19000.0,
        youngs_modulus=200e9,
        moment_of_inertia=0.86,
        damping_ratio=0.005,
        length=48.0,
        element_size=0.1,
        mode_numbers=[0, 1, 2],
    )
    assert sum(np.subtract(modal_mass, [456000.0, 456000.0, 456000.0])) < 0.01


def test_calculate_train_vector():
    train_distances = [1, 2, 3, 15]
    train_axle_forces = [1, 1, 1, 1]
    train_speeds = [10]
    time = 1
    mode_numbers = [0, 1, 2]
    spatial_coordinate = 0.5
    length = 10
    train_vector = calculate_train_vector(
        train_distances,
        train_axle_forces,
        train_speeds,
        time,
        length,
    )
    assert len(train_vector) == len(train_distances)
    assert list(train_vector) == [1, 1, 1, 0]


def test_newmark_time_integration():
    modal_mass = 1
    modal_damping = 1
    modal_stiffness = 1
    modal_force = np.array([1, 1, 1])
    time_vector = np.array([1, 2, 3])
    modal_acceleration, modal_velocity, modal_displacement = newmark_time_integration(
        modal_mass, modal_damping, modal_stiffness, modal_force, time_vector
    )
    assert len(modal_acceleration) == len(time_vector)