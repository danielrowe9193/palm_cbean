import matplotlib.pyplot as plt
import numpy as np
import utils

from config import Constants
from palmout import PalmOutXY, PalmOutXZ
from pathlib import Path
from topography import Topography


class PlotPalmOutXY:
    """Plot a cross-section Palm Out xy object."""

    def __init__(
        self,
        palmout: PalmOutXY,
        storage_directory: str | Path,
    ):
        """Initialize a PlotCrossSectionPalmOutXY."""
        self.palmout_xy = palmout
        self.storage_directory = Path(storage_directory)

    def wind_speed_contour_fill_plot(self, time_index: int, zu_xy_index: int = 0):
        """
        Plots the wind speed in the xy plane.

        Saves the figure to the plot directory.

        :param time_index:
        :param zu_xy_index:
        :return:
        """

        fig, ax = plt.subplots(figsize=(10, 10), constrained_layout=True)

        plot_data = self.palmout_xy.data.isel(time=time_index)

        wind_speed = plot_data.isel(zu_xy=zu_xy_index).wspeed_xy.values[::-1]

        level = plot_data.isel(zu_xy=zu_xy_index).zu_xy.values

        elapsed_time_s = utils.Calculations.calculate_elapsed_time(plot_data.values)

        utils.PlotUtils.plot_contour_fill(
            fig=fig,
            ax=ax,
            x_data=self.palmout_xy.x,
            y_data=self.palmout_xy.y,
            plot_data=wind_speed,
            var="w_speed",
            title=f"Wind Speed at {level} m\nFrame {time_index}\nElapsed Time {elapsed_time_s:.0f} s",
            x_label="x",
            y_label="y",
        )

        frame_name = f"frame_{time_index:05d}.png"

        utils.PlotUtils.save_plot(storage_directory=self.storage_directory, plot_name=frame_name)

        return None


class PlotPalmOutXZ:
    """Plot a cross-section Palm Out xy object."""

    def __init__(
        self,
        palmout: PalmOutXZ,
        storage_directory: str | Path,
    ):
        """Initialize a PlotCrossSectionPalmOutXY."""
        self.palmout_xz = palmout
        self.storage_directory = Path(storage_directory)

    def w_contour_fill_plot(self, time_index: int, y_xz_index: int = 0) -> None:
        """
        Plots a contour fill of vertical wind.

        Saves the plot to a given directory.

        :param time_index: The time iteration step.
        :param y_xz_index: The y-index at which to take the xz slice.
        :return: None
        """

        fig, ax = plt.subplots(figsize=(8, 4), constrained_layout=True, dpi=300)

        plot_data = self.palmout_xz.data.isel(time=time_index)

        w = plot_data.isel(y_xz=y_xz_index)["w_xz"]

        y_slice = plot_data.isel(y_xz=y_xz_index).y_xz.values

        elapsed_time = utils.Calculations.calculate_elapsed_time(data=plot_data)

        utils.PlotUtils.plot_contour_fill(
            fig=fig,
            ax=ax,
            x_data=self.palmout_xz.x,
            y_data=self.palmout_xz.z,
            plot_data=w,
            var="w_xz",
            title=f"Vertical Component of Wind at {y_slice} m\nFrame {time_index}\nElapsed Time {elapsed_time:.0f} s",
            x_label="x",
            y_label="z",
        )

        frame_name = f"frame_{time_index:05d}.png"

        utils.PlotUtils.save_plot(storage_directory=self.storage_directory, plot_name=frame_name)

        return None

    def wind_speed_contour_fill_plot(self, time_index: int, y_xz_index: int = 0):
        """
        Plots the wind speed in the xy plane.

        Saves the figure to the plot directory.

        :param time_index:
        :param y_xz_index:
        :return:
        """

        fig, ax = plt.subplots(figsize=(10, 10), constrained_layout=True)

        plot_data = self.palmout_xz.data.isel(time=time_index)

        wind_speed = plot_data.isel(y_xz=y_xz_index)["w_xz"].values[::-1]

        y_slice = plot_data.isel(y_xz=y_xz_index)["y_xz"].values

        elapsed_time_s = utils.Calculations.calculate_elapsed_time(plot_data["time"].values)

        utils.PlotUtils.plot_contour_fill(
            fig=fig,
            ax=ax,
            x_data=self.palmout_xz.x,
            y_data=self.palmout_xz.z,
            plot_data=wind_speed,
            var="w_speed",
            title=f"Wind Speed at {y_slice} m\nFrame {time_index}\nElapsed Time {elapsed_time_s:.0f} s",
            x_label="x",
            y_label="z",
        )

        frame_name = f"frame_{time_index:05d}.png"

        utils.PlotUtils.save_plot(storage_directory=self.storage_directory, plot_name=frame_name)

        return None


class PlotTopography:
    """
    Utilities for plotting topography files.
    """
    def __init__(self, topography: Topography):
        self.topography = topography

        self.fig, self.ax = plt.subplots(figsize=(8, 10), dpi=300)

    def plot_elevation(self) -> None:
        """
        Creates a plot of elevation of the topography.

        Displays a contour fill plot and contour lines and selected levels to indicate elevation.

        Saves the figure to the plots directory of the palm_cbean project.

        :return: None.
        """

        utils.PlotUtils.plot_terrain(
            fig=self.fig,
            ax=self.ax,
            x_data=self.topography.dataset["norm_x"],
            y_data=self.topography.dataset["norm_y"],
            terrain_data=self.topography.dataset["elevation"],
            var="elevation",
            title="Elevation Map of Barbados",
            x_label="Normalised x coordinate",
            y_label="Normalised y coordinate"
        )

        plt.savefig(Constants.plot_storage_directory / "bds.elevation.png")

        plt.close()

        return None

    def plot_xz_cross_section(self, norm_y: int | float) -> None:
        """
        Plots a cross-section of the topography along a given y slice.
        :param norm_y: The normalised y coordinate on which to take the slice
        :return: None
        """

        cross_section = self.topography.dataset.sel(norm_y=norm_y, method="nearest")

        plt.plot(cross_section.elevation.values)

        plt.savefig(Constants.plot_storage_directory / f"{norm_y}.xz_cross_section.png")
