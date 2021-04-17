import numpy as np

# Train properties
NUMBER_OF_INTERMEDIATE_COACHES = [18, 17, 16, 15, 14, 13, 13, 12, 11, 11]
COACH_LENGTH = np.array(range(18, 28))
BOGIE_AXLE_SPACING = [2.0, 3.5, 2.0, 3.0, 2.0, 2.0, 2.0, 2.5, 2.0, 2.0]
POINT_LOAD = [170, 200, 180, 190, 170, 180, 190, 190, 210, 210] * 1000
POWER_CAR_DISTANCES = [0.0, 3.0, 11.0, 3.0, 3.525]

def _create_end_coach_distances(hslm_number)

    return [
        BOGIE_AXLE_SPACING[hslm_number - 1],
        COACH_LENGTH[hslm_number - 1] - 1.5 * BOGIE_AXLE_SPACING[hslm_number - 1],
    ]

def _create_intermediate_coach_distances(hslm_number)

    return [
        BOGIE_AXLE_SPACING[hslm_number - 1],
        COACH_LENGTH[hslm_number - 1] - BOGIE_AXLE_SPACING[hslm_number - 1],
    ]

def _create_train_distances(hslm_number,end_coach_distances,intermediate_coach_distances):
    
    return np.cumsum(
        POWER_CAR_DISTANCES
        + end_coach_distances
        + intermediate_coach_distances * NUMBER_OF_INTERMEDIATE_COACHES[hslm_number - 1]
        + list(np.flip(end_coach_distances + [BOGIE_AXLE_SPACING[hslm_number - 1]]))
        + list(np.flip(POWER_CAR_DISTANCES[1::]))
    )

def get_train_distances(hslm_number):

    end_coach_distances = _create_end_coach_distances(hslm_number)
    intermediate_coach_distances = _create_intermediate_coach_distance(hslm_number)
    train_distances = _create_train_distances(hslm_number,end_coach_distances,intermediate_coach_distances)
    
    return train_distances

def get_axle_forces(hslm_number)

    train_axle_forces = POINT_LOAD[hslm_number - 1] * np.ones(len(train_distances))

    return train_axle_forces