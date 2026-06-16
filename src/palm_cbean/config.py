import numpy as np

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
        "elevation": dict(
            long_name="Elevation",
            units=r"$m$",
            xlabel=dict(x="x", norm_x="normalised x"),
            ylabel=dict(y="y", norm_y="normalised y"),
            cmap="terrain",
            contour_line_levels=[0, 1, 5, 10, 25, 50, 100, 200, 300, 400],
            contour_fill_levels=np.linspace(0, 400, 21)
        ),
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
