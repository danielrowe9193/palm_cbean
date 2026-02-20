import numpy as np
import rasterio
from pyproj import Transformer
from scipy.ndimage import zoom
import xarray


class Topography:
    """A topography object."""

    def __init__(self, filepath: str):
        """Initialise a Topography object."""
        self.filepath = filepath
        self.source = rasterio.open(self.filepath)

        self.elevation = self.source.read(1)
        self.resolution = self.source.transform[0]

        self.rows, self.columns = np.meshgrid(np.arange(self.source.height), np.arange(self.source.width), indexing="ij")
        self.x, self.y = rasterio.transform.xy(self.source.transform, self.rows, self.columns)

        self.transformer = Transformer.from_crs(self.source.crs, "EPSG:4326", always_xy=True)
        self._lon, self._lat = self.transformer.transform(self.x, self.y)

        self.latitude = np.array(self._lat).reshape(self.source.height, self.source.width)
        self.longitude = np.array(self._lon).reshape(self.source.height, self.source.width)

        self.dataset: xarray.Dataset | None = None

    @property
    def mask(self):
        """Mask missing values in the topography file"""

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

        if self.elevation.shape[0] % 2 != 0:
            # Add one row of zeros at the bottom.
            self.elevation = np.pad(self.elevation, ((0, 1), (0, 0)), mode='constant')

            # Check if the number of columns is odd.
        if self.elevation.shape[1] % 2 != 0:
            # Add one column of zeros on the right.
            self.elevation = np.pad(self.elevation, ((0, 0), (0, 1)), mode='constant')

        return self

    def downscale(self, final_resolution: int):
        """Downscale the topography file from the initial 10m resolution to a final resolution."""

        if final_resolution <= self.resolution:
            raise ValueError(f"Final resolution cannot be equal to or less than the original resolution.")

        self.resolution = self.resolution / final_resolution
        self.elevation = zoom(self.elevation, (self.resolution, self.resolution))
        return self

    def to_ascii(self, output_directory: str, output_filename: str) -> None:
        """Convert the elevation to ascii and store it at the given directory."""
        np.savetxt(f"{output_directory}\\{output_filename}_{self.resolution:.0f}_topo", self.elevation, fmt="%.1d")

    def to_xarray(self) -> xarray.Dataset:
        """Construct a xarray dataset for the elevation data."""
        pass


file_location = "C:\\Users\\drowe\\Downloads\\Raster\\Raster\\BRB_DEM_10M_UTM21N.tif"
bds_topo = Topography(file_location).mask.flip.downscale(20).make_shape_even
