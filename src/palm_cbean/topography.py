import matplotlib.pyplot as plt
import numpy as np
import rasterio
import xarray
from pyproj import Transformer
from scipy.ndimage import zoom


def make_even(data: np.ndarray):
    """Checks if any dimension of the array is odd and pads it so that it becomes even. PALM demands that the topography files have even dimensions."""
    if data.shape[0] % 2 != 0:
        data = np.pad(data, ((0, 1), (0, 0)), mode='constant')

    if data.shape[1] % 2 != 0:
        data = np.pad(data, ((0, 0), (0, 1)), mode='constant')

    return data


class Topography:
    """A topography object."""

    def __init__(self, filepath: str):
        """Initialise a Topography object."""
        self.filepath = filepath
        self.source = rasterio.open(self.filepath)

        self.elevation = self.source.read(1)
        self.resolution = self.source.transform[0]

        self.x, self.y = np.meshgrid(np.arange(self.source.height), np.arange(self.source.width), indexing="ij")

        self.norm_x: np.ndarray | None = None
        self.norm_y: np.ndarray | None = None

        # self.x, self.y = rasterio.transform.xy(self.source.transform, self.rows, self.columns)
        #
        # self.transformer = Transformer.from_crs(self.source.crs, "EPSG:4326", always_xy=True)
        # self._lon, self._lat = self.transformer.transform(self.x, self.y)
        #
        # self.latitude = np.array(self._lat).reshape(self.source.height, self.source.width)
        # self.longitude = np.array(self._lon).reshape(self.source.height, self.source.width)

        self.dataset: xarray.Dataset | None = None

    @property
    def shape(self):
        """The shape of the topography file."""
        return self.elevation.shape

    @property
    def mask(self):
        """Mask missing values in the topography file"""

        # Apply linear interpolation using the nearest members around the missing value grid point.

        self.elevation[self.elevation == -3.402823466385288598e+38] = 0
        self.elevation[self.elevation == -3.402820018375655977e+38] = 0

        return self

    @property
    def flip(self):
        """Flips the elevation array to match cardinal north."""

        self.elevation = self.elevation[::-1]

        return self

    @property
    def make_shape_even(self):
        """Pads the elevation if the shape of any dimension is odd. This should be called after downscaling or padding."""
        self.elevation = make_even(self.elevation)

        return self

    @property
    def normalise_axes(self):
        """Normalise the x and y axes to fall between 0 and 1."""
        x = self.x[:, 0]
        y = self.y[0, :]

        self.norm_x = (x - x.min()) / (x.max() - x.min())
        self.norm_y = (y - y.min()) / (y.max() - y.min())

        return self

    def pad(self, padding_amount: int):
        """Adds padding around the original topography file."""
        pass

    def downscale(self, final_resolution: int):
        """Downscale the topography file from the initial 10m resolution to a final resolution."""

        if final_resolution <= self.resolution:
            raise ValueError(f"Final resolution cannot be equal to or less than the original resolution.")

        scale = self.resolution / final_resolution
        self.elevation = zoom(self.elevation, (scale, scale))
        self.x = zoom(self.x, (scale, scale))
        self.y = zoom(self.y, (scale, scale))
        self.resolution = self.resolution / scale
        return self

    def to_ascii(self, output_directory: str, output_filename: str):
        """Convert the elevation to ascii and store it at the given directory."""
        np.savetxt(f"{output_directory}\\{output_filename}_{1 / self.resolution}m_topo", self.elevation, fmt="%.1d")
        return self

    def to_xarray(self):
        """Construct a xarray dataset for the elevation data."""

        self.dataset = xarray.Dataset(
            data_vars={
                "elevation": (("x", "y"), self.elevation)
            },
            coords={
                "norm_x": ("x", self.norm_x),
                "norm_y": ("y", self.norm_y)
            }
        )

        return self
