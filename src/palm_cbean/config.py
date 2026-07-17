import numpy as np

from pathlib import Path


class Constants:
    plot_storage_directory = Path("../../plots/")
    data_storage_directory = Path("../../data/")

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
        "wspeed_xy": dict(
            long_name="Wind Speed in the XY Plane",
            units=r"$ms^{-1}$",
            cmap="turbo",
            levels=np.linspace(0, 100, 101),
            cb_ticks=np.linspace(0, 100, 11),
        ),
        "wspeed_xz": dict(
            long_name="Wind Speed in the XZ Plane",
            units=r"$ms^{-1}$",
            cmap="turbo",
            levels=np.linspace(0, 100, 101),
            cb_ticks=np.linspace(0, 100, 11),
        ),
        "wspeed_yz": dict(
            long_name="Wind Speed in the YZ Plane",
            units=r"$ms^{-1}$",
            cmap="turbo",
            levels=np.linspace(0, 100, 101),
            cb_ticks=np.linspace(0, 100, 11),
        ),
        "u_xy": dict(
            long_name="Zonal Component of Wind in XY Plane",
            units=r"$ms^{-1}$"
        ),
        "u_xz": dict(
            long_name="Zonal Component of Wind in XZ Plane",
            units=r"$ms^{-1}$"
        ),
        "u_yz": dict(
            long_name="Zonal Component of Wind in YZ Plane",
            units=r"$ms^{-1}$"
        ),
        "v_xy": dict(
            long_name="Meridional Component of Wind in XY Plane",
            units=r"$ms^{-1}$"
        ),
        "v_xz": dict(
            long_name="Meridional Component of Wind in XZ Plane",
            units=r"$ms^{-1}$"
        ),
        "v_yz": dict(
            long_name="Meridional Component of Wind in YZ Plane",
            units=r"$ms^{-1}$"
        ),
        "w_xy": dict(
            long_name="Vertical Component of Wind in XY Plane",
            units=r"$ms^{-1}$",
            cmap="RdBu",
            levels=np.linspace(-5, 5, 21),
            cb_ticks=np.linspace(-5, 5, 21),
        ),
        "w_xz": dict(
            long_name="Vertical Component of Wind in XZ Plane",
            units=r"$ms^{-1}$",
            cmap="RdBu",
            levels=np.linspace(-5, 5, 21),
            cb_ticks=np.linspace(-5, 5, 21),
        ),
        "w_yz": dict(
            long_name="Vertical Component of Wind in YZ Plane",
            units=r"$ms^{-1}$",
            cmap="RdBu",
            levels=np.linspace(-5, 5, 21),
            cb_ticks=np.linspace(-5, 5, 21),
        ),
    }
