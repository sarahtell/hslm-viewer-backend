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
    mode_numbers = range(mode_numbers)
    (
        modal_masses,
        modal_dampings,
        modal_stiffnesses,
        circular_frequencies,
        modal_forces,
        time_vector
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
        modal_masses, modal_dampings, modal_stiffnesses, modal_forces, mode_numbers
    )

    mode_shape = create_mode_matrix(mode_numbers, bridge_length, element_size)
    bridge_displacement = np.dot(modal_displacement, mode_shape)
    midpoint_DOF = int(np.around(np.divide(bridge_length,2*element_size))) 
    midpoint_displacement = np.squeeze(np.asarray(bridge_displacement[:,midpoint_DOF]))
    max_bridge_displacement = bridge_displacement.max()
    
    return midpoint_displacement, time_vector 