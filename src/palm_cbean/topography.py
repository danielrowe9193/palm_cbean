import numpy as np
import rasterio
import xarray as xr
from scipy.ndimage import zoom


def make_even(data: np.ndarray) -> np.ndarray:
    """Checks if any dimension of the array is odd and pads it so that it becomes even. PALM demands that the topography files have even dimensions."""
    if data.shape[0] % 2 != 0:
        data = np.pad(data, ((0, 1), (0, 0)), mode="constant")

    if data.shape[1] % 2 != 0:
        data = np.pad(data, ((0, 0), (0, 1)), mode="constant")

    return data


class Topography:
    """A topography object."""

    def __init__(self, filepath: str):
        """Initialise a Topography object."""

        self.filepath = filepath
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
        """Construct and prepare a xarray dataset for the elevation data."""

        x = self.x[:, 0]
        y = self.y[0, :]

        norm_x = (x - x.min()) / (x.max() - x.min())
        norm_y = (y - y.min()) / (y.max() - y.min())

        dataset = xr.Dataset(
            data_vars={"elevation": (("x", "y"), self.elevation)},
            coords={"norm_x": ("x", norm_x), "norm_y": ("y", norm_y)},
        )

        dataset = dataset.interpolate_na(dim="x", method="nearest").interpolate_na(dim="y", method="nearest")

        return dataset

    def mask(self) -> None:
        """Mask missing values in the topography file"""

        self.elevation[self.elevation == -3.402823466385288598e38] = np.nan
        self.elevation[self.elevation == -3.402820018375655977e38] = np.nan

        return None

    def flip(self) -> None:
        """Flips the elevation array to match cardinal north."""

        self.elevation = self.elevation[::-1]

        return None

    def make_shape_even(self) -> None:
        """Pads the elevation if the shape of any dimension is odd. This should be called after downscaling or padding."""

        self.elevation = make_even(self.elevation)

        return None

    def pad(self, padding_amount: int):
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

    def to_ascii(self, output_directory: str, output_filename: str) -> None:
        """Convert the elevation to ascii and store it at the given directory."""

        np.savetxt(
            f"{output_directory}\\{output_filename}_{1 / self.resolution}m_topo",
            self.elevation,
            fmt="%.1d",
        )

        return None
