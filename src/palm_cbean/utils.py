import numpy as np


def make_even(data: np.ndarray) -> np.ndarray:
    """Checks if any dimension of the array is odd and pads it so that it becomes even. PALM demands that the topography files have even dimensions."""
    if data.shape[0] % 2 != 0:
        data = np.pad(data, ((0, 1), (0, 0)), mode="constant")

    if data.shape[1] % 2 != 0:
        data = np.pad(data, ((0, 0), (0, 1)), mode="constant")

    return data


def normalise(data: np.ndarray) -> np.ndarray:
    """Normalise data between zero and one."""
    pass
