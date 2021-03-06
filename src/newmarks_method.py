import numpy as np
from modal_properties import calculate_time_vector
BETA = 0.25
GAMMA = 0.5


def calculate_fixed_denominator(modal_mass, modal_damping, modal_stiffness, time_step):
    return modal_mass + np.multiply(GAMMA * time_step, modal_damping) + np.multiply(BETA * time_step ** 2, modal_stiffness)


def newmark_time_integration(modal_mass, modal_damping, modal_stiffness, modal_forces, mode_numbers):
    #time_vector = calculate_time_vector(bridge_length, train_speed, hslm_number)
    time_vector = calculate_time_vector()
    modal_displacement = [np.array([0]*len(mode_numbers))]
    modal_velocity = [np.array([0]*len(mode_numbers))] 
    modal_acceleration = [np.divide(
            modal_forces[0]
            - np.multiply(modal_damping,modal_velocity)
            - np.multiply(modal_stiffness,modal_displacement),
            modal_mass,
        )[0]]
    
    time_step = time_vector[1] - time_vector[0]

    fixed_denominator = calculate_fixed_denominator(
        modal_mass, modal_damping, modal_stiffness, time_step
    )
    
    for index in range(len(time_vector) - 1):
        temporary_modal_displacement = (
            modal_displacement[index]
            + time_step * modal_velocity[index]
            + 0.5 * time_step ** 2 * (1 - 2 * BETA) * modal_acceleration[index]
        )

        temporary_modal_velocity = (
            modal_velocity[index] + time_step * (1 - GAMMA) * modal_acceleration[index]
        )

        modal_acceleration.append(
            np.divide(
                modal_forces[index + 1]
                - modal_damping * temporary_modal_velocity
                - modal_stiffness * temporary_modal_displacement,
                fixed_denominator,
            )
        )
        print(modal_acceleration)
        modal_velocity.append(
            temporary_modal_velocity + GAMMA * time_step * modal_acceleration[index + 1]
        )
        modal_displacement.append(
            temporary_modal_displacement + BETA * time_step ** 2 * modal_acceleration[index + 1]
        )

    modal_acceleration = np.asmatrix(modal_acceleration)
    modal_velocity = np.asmatrix(modal_velocity)
    modal_displacement = np.asmatrix(modal_displacement)


    return modal_acceleration, modal_velocity, modal_displacement