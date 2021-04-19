from train_properties import get_train_vector
from modal_properties import (
    calculate_modal_properties,
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
        hslm_number,
    )

    modal_acceleration, modal_velocity, modal_displacement = newmark_time_integration(
        modal_masses, modal_dampings, modal_stiffnesses, modal_forces
    )

    mode_shape = create_mode_matrix(mode_numbers, bridge_length)
    bridge_acceleration = np.dot(mode_shape, modal_acceleration).sum(
        axis=1, dtype="float"
    )
