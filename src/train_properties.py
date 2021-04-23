import numpy as np

# Train properties
NUMBER_OF_INTERMEDIATE_COACHES = [18, 17, 16, 15, 14, 13, 13, 12, 11, 11]
COACH_LENGTH = np.array(range(18, 28))
BOGIE_AXLE_SPACING = [2.0, 3.5, 2.0, 3.0, 2.0, 2.0, 2.0, 2.5, 2.0, 2.0]
POINT_LOAD = [170, 200, 180, 190, 170, 180, 190, 190, 210, 210] * 1000
POWER_CAR_DISTANCES = [0.0, 3.0, 11.0, 3.0, 3.525]


def _create_end_coach_distances(hslm_number):

    return [
        BOGIE_AXLE_SPACING[hslm_number - 1],
        COACH_LENGTH[hslm_number - 1] - 1.5 * BOGIE_AXLE_SPACING[hslm_number - 1],
    ]


def _create_intermediate_coach_distances(hslm_number):

    return [
        BOGIE_AXLE_SPACING[hslm_number - 1],
        COACH_LENGTH[hslm_number - 1] - BOGIE_AXLE_SPACING[hslm_number - 1],
    ]


def _create_train_distances(
    hslm_number, end_coach_distances, intermediate_coach_distances
):

    return np.cumsum(
        POWER_CAR_DISTANCES
        + end_coach_distances
        + intermediate_coach_distances * NUMBER_OF_INTERMEDIATE_COACHES[hslm_number - 1]
        + list(np.flip(end_coach_distances + [BOGIE_AXLE_SPACING[hslm_number - 1]]))
        + list(np.flip(POWER_CAR_DISTANCES[1::]))
    )


def calculate_train_distances(hslm_number):

    end_coach_distances = _create_end_coach_distances(hslm_number)
    intermediate_coach_distances = _create_intermediate_coach_distances(hslm_number)
    train_distances = _create_train_distances(
        hslm_number, end_coach_distances, intermediate_coach_distances
    )

    return train_distances


def calculate_axle_forces(hslm_number,train_distances):

    train_axle_forces = -POINT_LOAD[hslm_number - 1] * np.ones(len(train_distances))

    return train_axle_forces


def calculate_train_vector(
    train_speed, time, bridge_length, train_distances, train_axle_forces
):
    train_vector = []
    for index in range(len(train_distances)): 
    
        train_vector.append(np.multiply(
        train_axle_forces[index],
        np.heaviside(np.subtract(time, np.divide(train_distances[index], train_speed)), 0)
        - np.heaviside(
            np.subtract(
                time, np.divide(np.add(bridge_length, train_distances[index]), train_speed)
            ),
            0,
        ),
    )
        )
    return np.array(train_vector) 


def get_train_vector(train_speed, time, bridge_length):
    train_distances =calculate_train_distances(hslm_number)
    train_axle_forces = calculate_axle_forces(hslm_number,train_distances)
    return calculate_train_vector(
        train_speed, time, bridge_length, train_distances, train_axle_forces
    )
