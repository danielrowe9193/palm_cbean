from pathlib import Path


class Constants:
    plot_storage_directory = Path("../../plots/")

    _xy_data = Path("../../data/flow_around_cube_cyclic_xy.000.nc")
    _xz_data = Path("../../data/bds_test9_xz.000.nc")

    SIGMA = 1.5


class PlotElements:
    """
    Container for all plot decorators.
    """

    plot_elements = {
        "w_speed": dict(
            long_name="Wind Speed",
            units=r"$ms^{-1}$"
        ),
        "u": dict(
            long_name="Zonal Component of Wind",
            units=r"$ms^{-1}$"
        ),
        "v": dict(
            long_name="Meridional Component of Wind",
            units=r"$ms^{-1}$"
        ),
    }
