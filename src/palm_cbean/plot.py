import matplotlib.pyplot as plt
import numpy as np
import utils

from config import Constants
from palmout import PalmOutXY, PalmOutXZ
from pathlib import Path
from topography import Topography


class PlotPalmOutXZ:
    def __init__(self, palmout: PalmOutXZ, storage_directory: str | Path, frame: int):
        """Initialize a PlotCrossSectionPalmOutXZ."""
        self.palmout_xz = palmout
        self.storage_directory = Path(storage_directory)
        self.frame = frame

        self.plot_data = self.palmout_xz.data.isel(time=self.frame)

        self.fig, self.ax = plt.subplots(figsize=(8, 10))

    def u_contour_plot(self):
        """Plots contour fill of the u component of the flow."""
        u = self.plot_data.u.values[::-1]
        u_contour_fill = self.ax.contourf(u, cmap="RdBu", levels=20)

        self.ax.set(
            title=f"Zonal Component of Flow at {self.plot_data['yv_xz'].values} m",
            xlabel="x",
            ylabel="z",
        )

        self.ax.grid()

        return u_contour_fill

    def wind_speed_contour_fill_plot(self, y_xz_index: int = 0):
        """Generate contour plot at a given time index."""

        wind_speed = self.plot_data.isel(y_xz=y_xz_index).wspeed_xz.values[::-1]

        elapsed_time_ns = self.plot_data["time"].values

        elapsed_time_s = elapsed_time_ns / np.timedelta64(1, "s")

        wind_speed_contour_fill = self.ax.contourf(
            self.palmout_xz.x,
            self.palmout_xz.y,
            wind_speed,
            cmap="turbo",
            levels=np.linspace(0, 10, 21),
        )

        wind_speed_colour_bar = self.fig.colorbar(wind_speed_contour_fill)
        wind_speed_colour_bar.set_ticks(ticks=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        wind_speed_colour_bar.set_label("Wind Speed (m/s)")

        self.ax.set(
            title=f"Wind Speed at {self.plot_data.isel(y_xz=y_xz_index).zu_xy.values} m\nFrame {self.frame}\nElapsed Time {elapsed_time_s:.0f} s",
            xlabel="x",
            ylabel="y",
        )

        return wind_speed_contour_fill, wind_speed_colour_bar

    def save_plot(self):
        """Save the plot to the specified storage directory."""
        frame_name = f"frame_{self.frame:05d}"
        frame_path = self.storage_directory / frame_name
        plt.savefig(frame_path)
        plt.close()


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

        fig, ax = plt.subplots(figsize=(20, 10), constrained_layout=True, dpi=300)

        plot_data = self.palmout_xy.data.isel(time=time_index)

        wind_speed = plot_data.isel(zu_xy=zu_xy_index).wspeed_xy.values[::-1]

        level = plot_data.isel(zu_xy=zu_xy_index).zu_xy.values

        elapsed_time_ns = plot_data["time"].values

        elapsed_time_s = elapsed_time_ns / np.timedelta64(1, "s")

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

    @staticmethod
    def _show_plot():
        """Show the plot."""
        plt.show()


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
