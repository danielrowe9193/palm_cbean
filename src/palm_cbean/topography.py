import numpy as np
import rasterio
import xarray as xr
import utils


from config import Constants
from pathlib import Path
from skimage.transform import rescale


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

        self.height, self.width = np.meshgrid(
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

        x = np.linspace(0, self.shape[0], self.shape[0])
        y = np.linspace(0, self.shape[1], self.shape[1])

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

        dataset = dataset.set_xindex("norm_x")
        dataset = dataset.set_xindex("norm_y")

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

    def pad(self, amount: int) -> None:
        """
        Pad the topography file with 0 elevation values.

        Pads the topography file in all directions with the designated padding amount.
        :param amount: The amount of padding to apply to the topography file, meters.
        :return: None.
        """

        grid_points = utils.Calculations.distance_to_grid_points(amount, self.resolution)

        self.elevation = np.pad(
            array=self.elevation,
            pad_width=grid_points
        )

        return None

    def downscale(self, final_resolution: int) -> None:
        """
        Downscale the topography file from the initial 10m resolution to a final resolution.

        Currently, resolutions that are multiples of 10m are known to work with PALM, and
        further testing is required for other resolutions and their compatibility with
        PALM

        Utilising the skimage.transform.rescale function, downscaling can be achieved without
        artifacting at the zero contours

        :param final_resolution: The final resolution of the topography file, in meters.
        :return: None
        """

        if final_resolution <= self.resolution:
            raise ValueError(
                f"Final resolution cannot be equal to or less than the original resolution."
            )

        scale = self.resolution / final_resolution
        self.elevation = rescale(self.elevation, scale, order=1, anti_aliasing=True)
        self.height = rescale(self.height, scale, order=1)
        self.width = rescale(self.width, scale, order=1)
        self.resolution = final_resolution

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


class ToyTopography:
    """
    Class containing utilities for creating toy buildings to be used with PALM.

    Useful for testing and learning the PALM model system. Possible future applications testing fluid flow through buildings.
    """

    def __init__(self, size_of_domain: tuple[int]) -> None:
        """
        Creates the domain on which the toy buildings should be placed.

        Uses size_of_domain to create an array of zeros, which represents the surface. This is the canvas on which
        further buildings can be placed.

        :param size_of_domain: The size of the domain to be simulated, expressed as a tuple of integers. Also represents the
        shape of the domain which is critical for the namelist file and running PALM.
        """

        self.size_of_domain = size_of_domain

        self.topography = np.zeros(self.size_of_domain)

    def add_building(self, x_span: tuple[int], y_span: tuple[int], height: int) -> None:
        """
        Adds a building to the topography.

        This function simply defines the grid points in x, y, and z that a building will occupy. The actually dimensions of the
        building are established in the PALM simulation when you set `dx` and `dy`.



        :param x_span: The span of the building in the x-direction. It is defined by giving the leftmost x position and rightmost x position of the building.
        An x_span=(2, 10), means that the building will occupy a region ranging from x=2 to x=10.
        :param y_span: The span of the building in the y-direction. It is defined by giving the bottommost y position and uppermost y position of the building.
        A y_span=(2, 10), means that the building will occupy a region ranging from y=2 to y=10.
        :param height: The height of the building.
        :return:
        """

        self.topography[x_span[0]:x_span[1], y_span[0]:y_span[1]] = height

        return None

    def save_topofile(self, destination_directory: str, filename: str) -> None:
        """
        Saves the toy topography file to the directory of the user's choice.

        The filename should not have any extensions, as it will be saved as an ASCII file. Deviating from this
        may cause errors.

        This should be called after all the desired buildings are added. If it is called before, then the topography
        file will not contain all the buildings the user created.

        :param destination_directory: The directory to store the topography file. For the usages of PALM, this should be the
        INPUT/ directory of the experiment.
        :param filename: The name of the topography file. It should have the same name as the experiment directory and have
        _topo at the end. For example, if the experiment is stored in toy_model/, then the topography file should be called
        toy_model_topo.
        :return: None
        """

        filepath = Path(destination_directory) / filename

        np.savetxt(filepath, self.topography, fmt="%.0f")

        print(f"The ToyTopography file was saved to {filepath}")

        return None


