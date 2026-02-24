import math
import matplotlib.pyplot as plt
import numpy as np

from src.palm_cbean.palmout import PalmOut
from src.palm_cbean.topography import Topography


class PlotPalmOut:

    def __init__(self, palmout: PalmOut):
        """Initialise a plot with a PalmOut object"""
        self.palmout = palmout

        self.fig, self.ax = plt.subplots(figsize=(8, 10))

    def contour_plot(self):
        """Create a contour plot"""
        ...

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


class PlotTopography:

    def __init__(self, topo: Topography):
        self.topo = topo

        self.fig, self.ax = plt.subplots(figsize=(8, 10))

    def plot_elevation(
            self, contour_levels=None
    ):
        """Create a contour plot of topography."""

        if contour_levels is None:
            contour_levels = [0, 1, 5, 10, 25, 50, 100, 200, 300, 400]

        contour_fill_levels = np.arange(start=self.topo.elevation.min(), stop=self.topo.elevation.max(), step=1)

        elevation_contour = self.ax.contour(self.topo.norm_y, self.topo.norm_x, self.topo.elevation, levels=contour_levels, colors='black', linewidths=0.5)
        elevation_contour_fill = self.ax.contourf(self.topo.norm_y, self.topo.norm_x, self.topo.elevation, cmap="terrain", levels=contour_fill_levels)

        self.ax.set_title("Plot Showing Relief of Barbados (m)")
        self.ax.set_xlabel("Normalised x")
        self.ax.set_ylabel("Normalised y")

        return elevation_contour, elevation_contour_fill


file_location = "C:\\Users\\drowe\\Downloads\\Raster\\Raster\\BRB_DEM_10M_UTM21N.tif"
storage_directory = "C:\\Users\\drowe"
# bds_topo = Topography(file_location).make_shape_even.mask.flip.normalise_axes
#
# bds_topo_plot = PlotTopography(bds_topo)
# bds_topo_plot.plot_elevation()
# plt.show()

bds_palm_output = PalmOut("C:\\Users\\drowe\\bds_test9_t58_slice.nc")
bds_palm_output_xy = bds_palm_output.xy_cross_section(z=4500)

bds_palm_output_xy_plot = PlotPalmOut(bds_palm_output_xy)
bds_palm_output_xy_plot.u_contour_plot()
plt.show()
