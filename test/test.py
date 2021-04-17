from modal_properties import calculate_modal_properties, calculate_modal_forces 
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


def sum_abc(a, b, c):
    return sum([int(a), int(b), int(c)])


def test_sum_abc():
    summa = sum_abc(1, 2, 3)
    summa_string_test = sum_abc("1", "2", "3")
    assert summa == 6
    assert summa_string_test == 6


def test_calculate_modal_forces():
    train_distances = [1, 2, 3]
    train_axle_forces = [1, 1, 1]
    train_speeds = [10]
    mode_numbers = [0, 1]
    spatial_coordinate = 0.5
    length = 1
    modal_forces = calculate_modal_forces(
        train_distances,
        train_axle_forces,
        train_speeds,
        mode_numbers,
        spatial_coordinate,
        length,
    )
    assert modal_forces.shape[0] == len(train_speeds)
    assert modal_forces.shape[1] == len(mode_numbers)