from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.colorbar import Colorbar
from matplotlib.contour import QuadContourSet

from config import PlotElements

class Calculations:

    @staticmethod
    def make_even(data: np.ndarray) -> np.ndarray:
        """Checks if any dimension of the array is odd and pads it so that it becomes even. PALM demands that the topography files have even dimensions."""
        if data.shape[0] % 2 != 0:
            data = np.pad(data, ((0, 1), (0, 0)), mode="constant")

        if data.shape[1] % 2 != 0:
            data = np.pad(data, ((0, 0), (0, 1)), mode="constant")

        return data

    @staticmethod
    def normalise(data: np.ndarray) -> np.ndarray:
        """Normalise data between zero and one."""
        pass


class PlotUtils:
    """
    Object containing utilities for the construction of most plots.

    The backbone of plotting functions exist here.
    """

    @staticmethod
    def save_plot(destination_directory: str, plot_name: str) -> None:
        """
        Saves the figure to the desired destination directory. Uses the default
        plot storage directory in the config file.
        :param destination_directory: The directory in which to store the plot
        :param plot_name: The name of the plot. Should include the extension (.png, .jpeg, etc.)
        :return: None.
        """
        ...

    @staticmethod
    def plot_contour_fill(
            fig: plt.Figure,
            ax: plt.Axes,
            x_data: np.array | xr.DataArray,
            y_data: np.array | xr.DataArray,
            plot_data: np.array | xr.DataArray,
            var: str,
            title: str,
            x_label: str,
            y_label: str,
            cmap: str
    ) -> tuple[QuadContourSet, Colorbar]:
        """
        General utility for plotting contour fills of 2D data.

        Also prepares the title of the plot, the x and y labels and the colorbar.

        :param fig: The figure on which the plot should be made.
        :param ax: The axis on which the plot should be made.
        :param x_data: The x_data on which to populate the x_axis.
        :param y_data: The y_data on which to populate the y_axis.
        :param plot_data: The data used for plotting the contour fill.
        :param var: The variable name that is being plotted.
        :param title: The title of the plot.
        :param x_label: The label of the x-axis.
        :param y_label: The label of the y-axis.
        :param cmap: The colormap to be used in the contourfill plot.
        :return: The contour fill and associated colorbar.
        """

        var = PlotElements.plot_elements[var]

        contour_fill = ax.contourf(
            x_data,
            y_data,
            plot_data,
            cmap=var["cmap"]
        )

        color_bar = fig.colorbar(
            contour_fill,
            label=var["title"] + var["units"]
        )

        return contour_fill, color_bar

    @staticmethod
    def plot_terrain(
            fig: plt.Figure,
            ax:plt.Axes,
            x_data: np.array | xr.DataArray,
            y_data: np.array | xr.DataArray,
            terrain_data: np.array | xr.DataArray,
            var: str
    ):
        ...

