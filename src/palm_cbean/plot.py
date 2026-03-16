from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import numpy as np

from palmout import VolumePalmOut, PalmOutXY
from pathlib import Path
from topography import Topography


class PlotPalmOutXZ:

    def __init__(self, palmout: VolumePalmOut):
        """Initialise a plot with a PalmOut object"""
        self.palmout = palmout

        self.fig, self.ax = plt.subplots(figsize=(8, 10))

    def u_contour_plot(self):
        """Plots contour fill of the u component of the flow."""
        u = self.palmout.data.u.values[::-1]
        u_contour_fill = self.ax.contourf(u, cmap="RdBu", levels=200)

        self.ax.set(
            title=f"Zonal Component of Flow at {self.palmout.z} m",
            xlabel="x Direction", ylabel="y Direction"
        )

        self.ax.grid()

        return u_contour_fill


class PlotPalmOutXY:
    """Plot a cross-section Palm Out xy object."""

    def __init__(self, palmout: PalmOutXY, storage_directory: str | Path, frame: int, figure_size: tuple = (8, 10)):
        """Initialize a PlotCrossSectionPalmOutXY."""
        self.palmout_xy = palmout
        self.storage_directory = Path(storage_directory)
        self.frame = frame

        self.plot_data = self.palmout_xy.data.isel(time=self.frame)

        self.fig, self.ax = plt.subplots(figsize=figure_size)

    def wind_speed_contour_fill_plot(self, zu_xy_index: int = 0):
        """Generate contour plot at a given time index."""

        wind_speed = self.plot_data.isel(zu_xy=zu_xy_index).wspeed_xy.values[::-1]

        wind_speed_contour_fill = self.ax.contourf(
            wind_speed, cmap="turbo", levels=np.linspace(0, 10, 11)
        )

        wind_speed_colour_bar = self.fig.colorbar(
            wind_speed_contour_fill
        )

        self.ax.set(
            title="Wind Speed"
        )

        return wind_speed_contour_fill, wind_speed_colour_bar

    def show_plot(self):
        """Show the plot."""
        plt.show()

    def save_plot(self, ):
        """Save the plot to the specified storage directory."""
        frame_name = f"frame_{self.frame:05d}"
        frame_path = self.storage_directory / frame_name
        plt.savefig(frame_path)
        plt.close()


class PlotTopography:

    def __init__(self, topography: Topography):
        self.topography = topography

        self.fig, self.ax = plt.subplots(figsize=(8, 10))

    def plot_elevation(
            self, contour_levels=None
    ):
        """Create a contour plot of topography."""

        if contour_levels is None:
            contour_levels = [0, 1, 5, 10, 25, 50, 100, 200, 300, 400]

        contour_fill_levels = np.arange(start=self.topography.elevation.min(), stop=self.topography.elevation.max(), step=1)

        elevation_contour = self.ax.contour(self.topography.norm_y, self.topography.norm_x, self.topography.elevation, levels=contour_levels, colors='black', linewidths=0.5)
        elevation_contour_fill = self.ax.contourf(self.topography.norm_y, self.topography.norm_x, self.topography.elevation, cmap="terrain", levels=contour_fill_levels)

        self.ax.set_title("Plot Showing Relief of Barbados (m)")
        self.ax.set_xlabel("Normalised x")
        self.ax.set_ylabel("Normalised y")

        return elevation_contour, elevation_contour_fill

