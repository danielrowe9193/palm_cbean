import palmout


def require_palmout_xy(obj) -> None:
    if not isinstance(obj, palmout.PalmOutXY):
        raise TypeError(
            f"Expected PalmOutXY, got {type(obj).__name__}"
        )

    return None


def require_palmout_xz(obj) -> None:
    if not isinstance(obj, palmout.PalmOutXZ):
        raise TypeError(
            f"Expected PalmOutXZ, got {type(obj).__name__}"
        )

    return None
