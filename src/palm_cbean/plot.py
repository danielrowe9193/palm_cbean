from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import numpy as np
from palmout import VolumePalmOut, PalmOutXY
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

    def __init__(self, palmout: PalmOutXY, storage_directory: str, frame: int, figure_size: tuple = (8, 10)):
        """Initialize a PlotCrossSectionPalmOutXY."""
        self.palmout_xy = palmout
        self.storage_directory = storage_directory
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
        frame_path = f"{self.storage_directory}\\{frame_name}"
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


"""
Dimensions:  (time: 6, zu_3d: 302, y: 1000, xu: 1000, yv: 1000, x: 1000,
              zw_3d: 302)
Coordinates:
  * time     (time) timedelta64[ns] 48B 00:10:00.131999999 ... 01:00:01.002000
  * zu_3d    (zu_3d) float64 2kB 0.0 5.0 15.0 ... 2.985e+03 2.995e+03 3.005e+03
  * y        (y) float64 8kB 50.0 150.0 250.0 ... 9.975e+04 9.985e+04 9.995e+04
  * xu       (xu) float64 8kB 0.0 100.0 200.0 ... 9.97e+04 9.98e+04 9.99e+04
  * yv       (yv) float64 8kB 0.0 100.0 200.0 ... 9.97e+04 9.98e+04 9.99e+04
  * x        (x) float64 8kB 50.0 150.0 250.0 ... 9.975e+04 9.985e+04 9.995e+04
  * zw_3d    (zw_3d) float64 2kB 0.0 10.0 20.0 30.0 ... 2.99e+03 3e+03 3.01e+03
Data variables:
    u        (time, zu_3d, y, xu) float32 7GB ...
    v        (time, zu_3d, yv, x) float32 7GB ...
    w        (time, zw_3d, y, x) float32 7GB ...
    wspeed   (time, zu_3d, y, x) float32 7GB ...
    wdir     (time, zu_3d, y, x) float32 7GB ...
    p        (time, zu_3d, y, x) float32 7GB ...
Attributes: (12/27)
    title:           PALM 25.04  run: bds_test9.00  host: default  2026-02-25...
    Conventions:     CF-1.7
    creation_time:   2026-02-25 12:42:54 -04
    data_content:    3d
    version:         1
    origin_time:     2019-06-21 12:00:00 +00
    ...              ...
    source:          PALM 25.04
    references:
    keywords:
    licence:
    comment:
    VAR_LIST:        ;u;v;w;wspeed;wdir;p;

<xarray.Dataset> Size: 58MB
Dimensions:   (y_xz: 4, time: 6, zu: 302, xu: 1000, zw: 302, x: 1000, yv_xz: 4)
Coordinates:
  * y_xz      (y_xz) float64 32B 250.0 2.05e+03 1.005e+04 5.005e+04
  * time      (time) timedelta64[ns] 48B 00:10:00.131999999 ... 01:00:01.002000
  * zu        (zu) float64 2kB 0.0 5.0 15.0 ... 2.985e+03 2.995e+03 3.005e+03
  * xu        (xu) float64 8kB 0.0 100.0 200.0 ... 9.97e+04 9.98e+04 9.99e+04
  * zw        (zw) float64 2kB 0.0 10.0 20.0 30.0 ... 2.99e+03 3e+03 3.01e+03
  * x         (x) float64 8kB 50.0 150.0 250.0 ... 9.975e+04 9.985e+04 9.995e+04
  * yv_xz     (yv_xz) float64 32B 200.0 2e+03 1e+04 5e+04
Data variables:
    ind_y_xz  (y_xz) float64 32B ...
    u_xz      (time, zu, y_xz, xu) float32 29MB ...
    w_xz      (time, zw, y_xz, x) float32 29MB ...
Attributes: (12/27)
    title:           PALM 25.04  run: bds_test9.00  host: default  2026-02-25...
    Conventions:     CF-1.7
    creation_time:   2026-02-25 12:42:54 -04
    data_content:    xz
    version:         1
    origin_time:     2019-06-21 12:00:00 +00
    ...              ...
    source:          PALM 25.04
    references:
    keywords:
    licence:
    comment:
    VAR_LIST:        ;u_xz;w_xz;
"""

# file_location = "C:\\Users\\drowe\\Downloads\\Raster\\Raster\\BRB_DEM_10M_UTM21N.tif"
# storage_directory = "C:\\Users\\drowe"
# bds_topo = Topography(file_location).make_shape_even.mask.flip.normalise_axes
# print(bds_topo.shape)
#
# bds_palm_output = VolumePalmOut("C:\\Users\\drowe\\bds_test9_t58_slice.nc")
# bds_palm_output_xy = bds_palm_output.xy_cross_section(z=4500)
#
# bds_palm_output_xy_plot = PlotPalmOutXZ(bds_palm_output_xy)
# bds_palm_output_xy_plot.u_contour_plot()
# plt.show()
