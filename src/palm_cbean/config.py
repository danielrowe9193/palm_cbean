import numpy as np

from pathlib import Path


class Constants:
    plot_storage_directory = Path("../../plots/")

    bds_topography_path = Path("../../data/BRB_DEM_10M_UTM21N.tif")

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
            colors="black",
            linewidths=0.5,
            contour_fill_levels=np.linspace(0, 400, 21)
        ),
        "w_speed": dict(
            long_name="Wind Speed",
            units=r"$ms^{-1}$",
            cmap="turbo",
            levels=np.linspace(0, 100, 101),
            cb_ticks=np.linspace(0, 100, 11),
        ),
        "u": dict(
            long_name="Zonal Component of Wind",
            units=r"$ms^{-1}$"
        ),
        "v": dict(
            long_name="Meridional Component of Wind",
            units=r"$ms^{-1}$"
        ),
        "w": dict(
            long_name="Vertical Component of Wind",
            units=r"$ms^{-1}$",
            cmap="RdBu",
            levels=np.linspace(-5, 5, 21),
            cb_ticks=np.linspace(-5, 5, 21),
        ),
    }
