import numpy as np
import rasterio
import xarray as xr
import utils

from pathlib import Path
from scipy.ndimage import (zoom, gaussian_filter)


class Topography:
    """
    Object representing and containing utilities for preparing topography to be used with PALM.
    """

    def __init__(self, filepath: str):
        """Initialise a Topography object."""

        self.filepath = Path(filepath)
        self.source = rasterio.open(self.filepath)

        self.elevation = self.source.read(1)
        self.resolution = self.source.transform[0]

        self.x, self.y = np.meshgrid(
            np.arange(self.source.height), np.arange(self.source.width), indexing="ij"
        )

    @property
    def shape(self) -> tuple[int]:
        """The shape of the topography file."""

        return self.elevation.shape

    @property
    def dataset(self) -> xr.Dataset:
        """
        Stores the elevation data in a xarray Dataset.

        Creates normalised coordinates between 0 and 1 for easy selection of data.
        :return:
        """

        x = self.x[:, 0]
        y = self.y[0, :]

        norm_x = (x - x.min()) / (x.max() - x.min())
        norm_y = (y - y.min()) / (y.max() - y.min())

        dataset = xr.Dataset(
            data_vars={"elevation": (("x", "y"), self.elevation)},
            coords={
                "x": ("x", x),
                "y": ("y", y),
                "norm_x": ("x", norm_x),
                "norm_y": ("y", norm_y)
            }
        )

        dataset = dataset.interpolate_na(dim="x", method="nearest").interpolate_na(
            dim="y", method="nearest"
        )

        return dataset

    def mask(self) -> None:
        """Mask missing values in the topography file"""

        self.elevation[self.elevation < 0] = 0

        return None

    def flip(self) -> None:
        """Flips the elevation array to match cardinal north."""

        self.elevation = self.elevation[::-1]

        return None

    def make_shape_even(self) -> None:
        """Pads the elevation if the shape of any dimension is odd. This should be called after downscaling or padding."""

        self.elevation = utils.Calculations.make_even(self.elevation)

        return None

    def pad(self, padding_amount: int) -> None:
        """Adds padding around the original topography file."""
        pass

    def downscale(self, final_resolution: int) -> None:
        """Downscale the topography file from the initial 10m resolution to a final resolution."""

        if final_resolution <= self.resolution:
            raise ValueError(
                f"Final resolution cannot be equal to or less than the original resolution."
            )

        scale = self.resolution / final_resolution
        self.elevation = zoom(self.elevation, (scale, scale))
        self.x = zoom(self.x, (scale, scale))
        self.y = zoom(self.y, (scale, scale))
        self.resolution = self.resolution / scale

        return None

    def smooth(self):
        """Smooth the topography by some amount."""

        self.elevation = gaussian_filter(self.elevation, sigma=1.5)

        return None

    def to_ascii(self, output_directory: str, output_filename: str) -> None:
        """Convert the elevation to ascii and store it in the given directory."""

        topography_file_name = f"{output_filename}_{1 / self.resolution}m_topo"

        topography_file_directory = Path(output_directory)

        topography_file_path = topography_file_directory / topography_file_name

        np.savetxt(
            fname=topography_file_path,
            X=self.elevation,
            fmt="%.1d",
        )

        print(f"\nFile saved to {topography_file_path}\n")

        return None
