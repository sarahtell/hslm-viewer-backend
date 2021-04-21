import numpy as np
from train_properties import get_train_vector
from modal_properties import (
    get_modal_properties,
    calculate_modal_forces,
    create_mode_matrix,
)
from newmarks_method import newmark_time_integration


def calculate_bridge_response(
    bridge_mass,
    youngs_modulus,
    moment_of_inertia,
    damping_ratio,
    bridge_length,
    element_size,
    mode_numbers,
    train_speed,
    hslm_number,
):
    (
        modal_masses,
        modal_dampings,
        modal_stiffnesses,
        circular_frequencies,
        modal_forces,
    ) = get_modal_properties(
        bridge_mass,
        youngs_modulus,
        moment_of_inertia,
        damping_ratio,
        bridge_length,
        element_size,
        mode_numbers,
        train_speed,
        hslm_number,
    )

    modal_acceleration, modal_velocity, modal_displacement = newmark_time_integration(
        modal_masses, modal_dampings, modal_stiffnesses, modal_forces
    )

    mode_shape = create_mode_matrix(mode_numbers, bridge_length, element_size)
    bridge_acceleration = np.dot(modal_acceleration, mode_shape)
    midacc = bridge_acceleration[:,210]
    max_bridge_acceleration = bridge_acceleration.max()
    print(midacc,midacc.shape)

    raise Exception