import numpy as np
from scipy import integrate
from scipy.misc import derivative


def define_mode_shape(mode_number, spatial_coordinate, length):
    return np.sin((mode_number + 1) * np.pi * spatial_coordinate / length)


def calculate_modal_mass(mass, length, mode_number):
    return integrate.quad(
        lambda spatial_coordinate: mass * define_mode_shape(mode_number, spatial_coordinate, length) ** 2,
        0,
        length,
    )[0]


def calculate_modal_masses(mass, length, mode_numbers):
    return [calculate_modal_mass(mass, length, mode_number) for mode_number in mode_numbers]


def calculate_modal_stiffness(youngs_modulus, moment_of_inertia, length, mode_number):
    return integrate.quad(
        lambda spatial_coordinate: youngs_modulus
        * moment_of_inertia
        * derivative(
            lambda spatial_coordinate: define_mode_shape(mode_number, spatial_coordinate, length),
            x0=spatial_coordinate,
            dx=1e-3,
            n=2,
        )
        ** 2,
        0,
        length,
    )[0]


def calculate_modal_stiffnesses(youngs_modulus, moment_of_inertia, length, mode_numbers):
    return [
        calculate_modal_stiffness(youngs_modulus, moment_of_inertia, length, mode_number)
        for mode_number in mode_numbers
    ]


def calculate_circular_frequencies(modal_stiffnesses, modal_masses):
    return np.sqrt(np.divide(modal_stiffnesses, modal_masses))


def calculate_modal_dampings(damping_ratio, mass, circular_frequencies, mode_numbers, length):
    return [
        integrate.quad(
            lambda spatial_coordinate: 2
            * damping_ratio
            * mass
            * circular_frequencies[mode_number]
            * define_mode_shape(mode_number, spatial_coordinate, length) ** 2,
            0,
            length,
        )[0]
        for mode_number in mode_numbers
    ]


def calculate_modal_properties(
    mass, youngs_modulus, moment_of_inertia, damping_ratio, length, element_size, mode_numbers
):
    mode_numbers = range(mode_numbers)
    modal_masses = calculate_modal_masses(mass, length, mode_numbers)
    modal_stiffnesses = calculate_modal_stiffnesses(
        
        youngs_modulus, moment_of_inertia, length, mode_numbers
    )
    circular_frequencies = calculate_circular_frequencies(modal_stiffnesses, modal_masses)
    modal_dampings = calculate_modal_dampings(
        damping_ratio, mass, circular_frequencies, mode_numbers, length
    )

    return modal_masses, modal_dampings, modal_stiffnesses, circular_frequencies
