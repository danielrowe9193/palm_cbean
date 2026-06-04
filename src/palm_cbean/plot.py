import matplotlib.pyplot as plt
import numpy as np

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
        frame: int,
        figure_size: tuple = (8, 10),
    ):
        """Initialize a PlotCrossSectionPalmOutXY."""
        self.palmout_xy = palmout
        self.storage_directory = Path(storage_directory)
        self.frame = frame

        self.plot_data = self.palmout_xy.data.isel(time=self.frame)

        self.fig, self.ax = plt.subplots(figsize=figure_size)

    def wind_speed_contour_fill_plot(self, zu_xy_index: int = 0):
        """Generate contour plot at a given time index."""

        wind_speed = self.plot_data.isel(zu_xy=zu_xy_index).wspeed_xy.values[::-1]

        elapsed_time_ns = self.plot_data["time"].values

        elapsed_time_s = elapsed_time_ns / np.timedelta64(1, "s")

        wind_speed_contour_fill = self.ax.contourf(
            self.palmout_xy.x,
            self.palmout_xy.y,
            wind_speed,
            cmap="turbo",
            levels=np.linspace(0, 10, 21),
        )

        wind_speed_colour_bar = self.fig.colorbar(wind_speed_contour_fill)
        wind_speed_colour_bar.set_ticks(ticks=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        wind_speed_colour_bar.set_label("Wind Speed (m/s)")

        self.ax.set(
            title=f"Wind Speed at {self.plot_data.isel(zu_xy=zu_xy_index).zu_xy.values} m\nFrame {self.frame}\nElapsed Time {elapsed_time_s:.0f} s",
            xlabel="x",
            ylabel="y",
        )

        return wind_speed_contour_fill, wind_speed_colour_bar

    @staticmethod
    def _show_plot():
        """Show the plot."""
        plt.show()

    def save_plot(self):
        """Save the plot to the specified storage directory."""
        frame_name = f"frame_{self.frame:05d}"
        frame_path = self.storage_directory / frame_name
        plt.savefig(frame_path)
        plt.close()


class PlotTopography:
    """
    Utilities for plotting topography files.
    """
    def __init__(self, topography: Topography):
        self.topography = topography

        self.fig, self.ax = plt.subplots(figsize=(8, 10))

    def plot_elevation(self, contour_levels: list | np.ndarray | None = None):
        """Create a contour plot of topography."""

        if contour_levels is None:
            contour_levels = [0, 1, 5, 10, 25, 50, 100, 200, 300, 400]

        elevation_contour = self.ax.contour(
            self.topography.dataset.norm_y,
            self.topography.dataset.norm_x,
            self.topography.elevation,
            levels=contour_levels,
            colors="black",
            linewidths=0.5,
        )
        elevation_contour_fill = self.ax.contourf(
            self.topography.dataset.norm_y,
            self.topography.dataset.norm_x,
            self.topography.dataset.elevation,
            cmap="terrain"
        )

        self.ax.set_title("Plot Showing Relief of Barbados (m)")
        self.ax.set_xlabel("Normalised x")
        self.ax.set_ylabel("Normalised y")

        return elevation_contour, elevation_contour_fill

    def plot_xz_cross_section(self, y: int | float) -> None:
        """
        Plots a cross-section of the topography along a given y slice.
        :param y: The normalised y coordinate on which to take the slice
        :return: None
        """

        cross_section = self.topography.dataset.sel(norm_y=y, method="nearest")

        plt.plot(cross_section.elevation.values)

        plt.show()
