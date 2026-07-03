from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.colorbar import Colorbar
from matplotlib.contour import QuadContourSet

from config import Constants, PlotElements
from pathlib import Path
from typing import Literal


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

    @staticmethod
    def build_contour_levels(data: np.ndarray, step: int, round_to_nearest: int) -> np.ndarray:
        """
        Using the minimum and maximum values in the data to build contour levels that are of factor 10.


        :param step:
        :param data:
        :return:
        """

        max_val = data.max()

        min_val = data.min()

        max_up = np.ceil(max_val / round_to_nearest) * round_to_nearest

        min_down = np.ceil(min_val / round_to_nearest) * round_to_nearest

        lvls = np.arange(start=min_down, stop=max_up, step=step)

        return lvls


class PlotUtils:
    """
    Object containing utilities for the construction of most plots.

    The backbone of plotting functions exist here.
    """

    @staticmethod
    def save_plot(storage_directory: str | Path, plot_name: str) -> None:
        """
        Saves plot to the plot storage directory of the project.

        :param storage_directory: The directory in which the plots should be stored.
        :param plot_name: The name of the plot. Should include the extension (.png, .jpeg, etc.)
        :return: None.
        """
        plot_path = storage_directory / plot_name
        plt.savefig(plot_path)
        plt.close()

    @staticmethod
    def plot_contour_fill(
            fig: plt.Figure,
            ax: plt.Axes,
            x_data: np.ndarray | xr.DataArray,
            y_data: np.ndarray | xr.DataArray,
            plot_data: np.ndarray | xr.DataArray,
            var: str,
            title: str,
            x_label: str,
            y_label: str
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
        :return: The contour fill and associated colorbar.
        """

        var = PlotElements.plot_elements[var]

        contour_fill = ax.contourf(
            x_data,
            y_data,
            plot_data,
            cmap=var["cmap"],
            levels=var["levels"]
        )

        color_bar = fig.colorbar(
            contour_fill,
            label=var["long_name"] + var["units"]
        )
        color_bar.set_ticks(
            var["cb_ticks"]
        )

        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        return contour_fill, color_bar

    @staticmethod
    def plot_terrain(
            fig: plt.Figure,
            ax: plt.Axes,
            x_data: np.ndarray | xr.DataArray,
            y_data: np.ndarray | xr.DataArray,
            terrain_data: np.ndarray | xr.DataArray,
            var: str | Literal["elevation"],
            title: str,
            x_label: str,
            y_label: str,
    ):
        """
        General utility for plotting terrain.

        Includes a colour fill of the elevation and contours at levels specified in the config module.

        Future functionality should expand to plot multiple islands.

        Plots the title and the x and y labels of the plot, along with the colour bar.

        :param fig: The figure on which the plot should be made.
        :param ax: The current axis on which to create the plot
        :param x_data: Data representing the x coordinate.
        :param y_data: Data representing the y coordinate.
        :param terrain_data: The elevation data.
        :param var: The name of the variable to be plotted. Reveals access to PlotElements.
        :param title: The title of the plot.
        :param y_label: The label of the x-axis.
        :param x_label: The label of the y-axis.
        :return: None
        """

        var = PlotElements.plot_elements[var]

        contour_lines = ax.contour(
            y_data,
            x_data,
            terrain_data,
            colors=var["colors"],
            linewidths=var["linewidths"]
        )

        contour_fill = ax.contourf(
            y_data,
            x_data,
            terrain_data,
            cmap=var["cmap"],
            levels=var["contour_fill_levels"]
        )

        color_bar = fig.colorbar(
            contour_fill,
            label=f"{var['long_name']} [{var['units']}]"
        )

        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        return contour_lines, contour_fill, color_bar


class DirectoryManagement:
    """
    Utilities for handling directories associated with the palm_cbean package.
    """

    @staticmethod
    def make_data_directory():
        """
        Checks if a data/ directory exists in the package.

        If not, it creates the directory.

        :return: None
        """

        if Path("../../data/").exists() is True:
            print("data/ directory already present. No action taken.\n")
        else:
            print("data/ directory not present. Creating data/ directory.\n")
            Path("../../data/").mkdir(exist_ok=True)

        return None

    @staticmethod
    def make_plots_directory():
        """
        Checks if a plots/ directory exists in the package.

        If not, it creates the directory.

        :return: None
        """

        if Path("../../plots/").exists() is True:
            print("plots/ directory already present. No action taken.\n")
        else:
            print("plots/ directory not present. Creating data/ directory.\n")
            Path("../../plots/").mkdir(exist_ok=True)

        return None

    @staticmethod
    def clear_temp_frame_dir():
        """
        Clears frames in the temporary frame store from the previous animation run.

        This method necessary because overwriting existing frames in the directory won't work if the
        new amount of frames is less than the current amount of frames in the temporary directory store.

        :return:
        """

        print("Deleting frames from previous animation...\n")

        for frame in Path("../../plots/temp_frame_store").iterdir():
            Path(f"../../plots/temp_frame_store/{frame}").unlink()

        return None

