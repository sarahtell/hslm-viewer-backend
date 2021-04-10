import numpy as np

# Train properties
hslm_number = 8


def define_train_composition(hslm_number):

    number_of_intermediate_coaches = [18, 17, 16, 15, 14, 13, 13, 12, 11, 11]
    coach_length = np.array(range(18, 28))
    bogie_axle_spacing = [2.0, 3.5, 2.0, 3.0, 2.0, 2.0, 2.0, 2.5, 2.0, 2.0]
    point_load = [170, 200, 180, 190, 170, 180, 190, 190, 210, 210] * 1000
    locomotive_distances = [0.0, 3.0, 11.0, 3.0, 3.525]

    coach_spacings = [
        bogie_axle_spacing[hslm_number],
        coach_length[hslm_number]
        - 1.5 * bogie_axle_spacing[hslm_number]
        - locomotive_distances[-1] / 2,
    ]

    train_distances = np.concatenate(
        (
            np.cumsum(locomotive_distances),
            np.amax(np.cumsum(locomotive_distances[1::]))
            + np.cumsum(
                np.concatenate(
                    (
                        coach_spacings,
                        np.array(
                            [
                                bogie_axle_spacing[hslm_number],
                                coach_length[hslm_number] - bogie_axle_spacing[hslm_number],
                            ]
                            * number_of_intermediate_coaches[hslm_number]
                        ),
                    )
                )
            ),
        )
    )
    train_axle_forces = point_load[hslm_number] * np.ones(len(train_distances))

    return train_distances, train_axle_forces
