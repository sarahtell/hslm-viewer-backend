import numpy as np

BETA = 0.25
GAMMA = 0.5

def calculate_fixed_denominator(modal_mass, modal_damping, modal_stiffness, time_step):
    return modal_mass + GAMMA*time_step*modal_damping + BETA*time_step**2*modal_stiffness 

def newmark_time_integration(modal_mass, modal_damping, modal_stiffness, modal_force, time_vector):

    modal_displacement = [0]
    modal_velocity = [0]
    modal_acceleration = [np.divide(modal_force[0] - modal_damping*modal_velocity[0] - modal_stiffness*modal_displacement[0],modal_mass)]
    time_step = time_vector[1] - time_vector[0]

    fixed_denominator = calculate_fixed_denominator(modal_mass, modal_damping, modal_stiffness, time_step)

    for index in range(len(time_vector)-1):
        temporary_modal_displacement = modal_displacement[index] + time_step*modal_velocity[index] + 0.5*time_step**2*(1-2*BETA)*modal_acceleration[index]
        temporary_modal_velocity = modal_velocity[index] + time_step*(1-GAMMA)*modal_acceleration[index]
        
        modal_acceleration.append(np.divide(modal_force[index+1] - modal_damping*temporary_modal_velocity - modal_stiffness*temporary_modal_displacement,fixed_denominator))
        modal_velocity.append(temporary_modal_velocity + GAMMA*time_step*modal_acceleration[index+1])
        modal_displacement.append(temporary_modal_displacement + BETA*time_step**2*modal_acceleration[index+1])

    return modal_acceleration, modal_velocity, modal_displacement