import numpy as np
from scipy import integrate
from scipy.misc import derivative
from src.train_properties import calculate_train_vector, calculate_train_distances, calculate_axle_forces


def define_mode_shape(mode_number, spatial_coordinate, bridge_length):
    return np.sin((mode_number + 1) * np.pi * spatial_coordinate / bridge_length)

def create_mode_matrix(mode_numbers, bridge_length, element_size):
    spatial_coordinate = calculate_spatial_coordinate(bridge_length, element_size)
    mode_matrix = np.zeros((len(mode_numbers), len(spatial_coordinate)))
    for index, mode_number in enumerate(mode_numbers):
        mode_matrix[index,:] = define_mode_shape(mode_number, spatial_coordinate, bridge_length)
    return mode_matrix

def calculate_modal_mass(bridge_mass, bridge_length, mode_number):
    return integrate.quad(
        lambda spatial_coordinate: bridge_mass
        * define_mode_shape(mode_number, spatial_coordinate, bridge_length) ** 2,
        0,
        bridge_length,
    )[0]


def calculate_modal_masses(bridge_mass, bridge_length, mode_numbers):
    return [calculate_modal_mass(bridge_mass, bridge_length, mode_number) for mode_number in mode_numbers]


def calculate_modal_stiffness(youngs_modulus, moment_of_inertia, bridge_length, mode_number):
    return integrate.quad(
        lambda spatial_coordinate: youngs_modulus
        * moment_of_inertia
        * derivative(
            lambda spatial_coordinate: define_mode_shape(mode_number, spatial_coordinate, bridge_length),
            x0=spatial_coordinate,
            dx=1e-3,
            n=2,
        )
        ** 2,
        0,
        bridge_length,
    )[0]


def calculate_modal_stiffnesses(youngs_modulus, moment_of_inertia, bridge_length, mode_numbers):
    return [
        calculate_modal_stiffness(youngs_modulus, moment_of_inertia, bridge_length, mode_number)
        for mode_number in mode_numbers
    ]


def calculate_circular_frequencies(modal_stiffnesses, modal_masses):
    return np.sqrt(np.divide(modal_stiffnesses, modal_masses))


def calculate_modal_dampings(damping_ratio, bridge_mass, circular_frequencies, mode_numbers, bridge_length):
    return [
        integrate.quad(
            lambda spatial_coordinate: 2
            * damping_ratio
            * bridge_mass
            * circular_frequencies[mode_number]
            * define_mode_shape(mode_number, spatial_coordinate, bridge_length) ** 2,
            0,
            bridge_length,
        )[0]
        for mode_number in mode_numbers
    ]


def calculate_modal_forces(
    train_speed,
    time_vector,
    mode_numbers,
    spatial_coordinate,
    bridge_length,
    hslm_number
):
    train_distances = calculate_train_distances(hslm_number)
    train_axle_forces = calculate_axle_forces(hslm_number,train_distances)
    modal_forces = np.zeros((len(time_vector),len(mode_numbers)))
    for time_index, time in enumerate(time_vector):
        train_vector = calculate_train_vector(
            train_speed, time, bridge_length, train_distances, train_axle_forces
            )
        for mode_index, mode_number in enumerate(mode_numbers):
            mode_shape = define_mode_shape(
                mode_number,
                np.subtract(train_speed * time, train_distances),#
                bridge_length,
            )
            modal_forces[:, mode_index] = np.dot(np.transpose(mode_shape),np.nan_to_num(train_vector))

    return modal_forces

"""     train_distances = calculate_train_distances(hslm_number)
    train_axle_forces = calculate_axle_forces(hslm_number,train_distances)
    modal_forces = np.zeros((time_vector.shape[0],len(mode_numbers)))
    for time_index in range(len(time_vector)-1):
        for mode_index in range(len(mode_numbers)-1):
            train_vector = calculate_train_vector(
                train_speed, time_vector[time_index], bridge_length, train_distances, train_axle_forces
            )
            mode_shape = define_mode_shape(
                mode_numbers[mode_index],
                np.subtract(train_speed * time_vector[time_index], train_distances),
                bridge_length,
            )
            print(modal_forces.shape)
            modal_forces[:, mode_index] = np.dot(np.transpose(mode_shape),np.nan_to_num(train_vector))

    return modal_forces """


def get_modal_properties(
    bridge_mass,
    youngs_modulus,
    moment_of_inertia,
    damping_ratio,
    bridge_length,
    element_size,
    mode_numbers,
    train_speed,
    hslm_number
):
    modal_masses = calculate_modal_masses(bridge_mass, bridge_length, mode_numbers)
    modal_stiffnesses = calculate_modal_stiffnesses(
        youngs_modulus, moment_of_inertia, bridge_length, mode_numbers
    )
    circular_frequencies = calculate_circular_frequencies(modal_stiffnesses, modal_masses)
    modal_dampings = calculate_modal_dampings(
        damping_ratio, bridge_mass, circular_frequencies, mode_numbers, bridge_length
    )

    spatial_coordinate = calculate_spatial_coordinate(bridge_length, element_size)
    time_vector = calculate_time_vector()
    modal_forces = calculate_modal_forces(train_speed, time_vector, mode_numbers, spatial_coordinate, bridge_length, hslm_number)

    return modal_masses, modal_dampings, modal_stiffnesses, circular_frequencies, modal_forces, time_vector

def calculate_time_vector():
    return np.arange(0, 10, 0.1) # Todo: Hardcoded for now...change later.

def calculate_spatial_coordinate(bridge_length, element_size):
    return np.arange(0, bridge_length+element_size, element_size)
    