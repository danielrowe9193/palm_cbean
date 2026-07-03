import palmout


def require_palmout_xy(obj) -> None:
    if not isinstance(obj, palmout.PalmOutXY):
        raise TypeError(
            "Expected type of PalmOut is PalmOutXY."
        )

    return None


def require_palmout_xz(obj) -> None:
    if not isinstance(obj, palmout.PalmOutXZ):
        raise TypeError(
            "Expected type of PalmOut is PalmOutXZ."
        )

    return None
