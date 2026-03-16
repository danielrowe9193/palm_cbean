from abc import ABC, abstractmethod
import xarray

from pathlib import Path


class PalmOut(ABC):
    """Absract PalmOut class."""

    def __init__(self, palm_out_filepath: str):
        """Initialize a PalmOut object with a specified filepath."""
        self.palm_out_filepath = Path(palm_out_filepath)
        self.data = xarray.open_dataset(self.palm_out_filepath, engine='netcdf4')

        self.x: int | None = None
        self.y: int | None = None
        self.z: int | None = None
        self.t: int | None = None

    @abstractmethod
    def show_info(self):
        """Print information about the PalmOut dataset."""
        print(self.data)
        return self

    @abstractmethod
    def normalise(self):
        """Normalise spatial coordinates between 0 and 1."""
        return self

    @abstractmethod
    def add_normalised_coords_to_data(self):
        """Update the data of the PalmOut with the normalised coordinates."""
        return self


class CrossSectionPalmOutXZ(PalmOut):
    """Initialise a PalmOut that represents an XZ cross-section."""

    def normalise(self) -> PalmOut:
        """Normalise x and z coordinates between 0 and 1."""
        self.x = (self.data.xu.values - self.data.xu.values.min()) / (self.data.xu.values.max() - self.data.xu.values.min())
        self.z = (self.data.zu.values - self.data.zu.values.min()) / (self.data.zu.values.max() - self.data.zu.values.min())
        return self

    def add_normalised_coords_to_data(self) -> PalmOut:
        """Update the data of the PalmOut with the normalised coordinates."""
        self.data = self.data.assign_coords(norm_x=self.x)
        self.data = self.data.assign_coords(norm_z=self.z)
        return self


class PalmOutXY(PalmOut):
    """Initialise a PalmOut that represents an XY cross-section."""

    def show_info(self):
        """Print information about the PalmOut dataset."""
        print(self.data)
        return self

    def normalise(self) -> PalmOut:
        """Normalise x and y coordinates between 0 and 1."""
        self.x = (self.data.x.values - self.data.x.values.min()) / (self.data.x.values.max() - self.data.x.values.min())
        self.y = (self.data.y.values - self.data.y.values.min()) / (self.data.y.values.max() - self.data.y.values.min())
        return self

    def add_normalised_coords_to_data(self):
        """Update the data of the PalmOut with the normalised coordinates."""
        self.data = self.data.assign_coords(norm_x=self.x)
        self.data = self.data.assign_coords(norm_y=self.y)
        return self


class VolumePalmOut:
    """A PalmOut object initialized using the Palm model output."""

    def __init__(self, palm_out_filepath: str):
        """
        Initialise a PalmOut object with the specified filepath that contains the palm out file.
        :param palm_out_filepath: The filepath in which the palm out file is stored.
        """

        self.palm_out_filepath = palm_out_filepath
        self.data = xarray.open_dataset(self.palm_out_filepath)

        self.z: int | None = None
        self.t: int | None = None

    def normalise(self):
        """Normalise spatial coordinates between 0 and 1."""
        pass

    def xy_cross_section(self, z: int = 0, i_time: int = 0):
        """Select a xy cross-section at a given level and time index."""
        self.z = z
        self.data = self.data.sel(zu_3d=z, zw_3d=z, method="nearest")
        return self


# bds_palm_output = CrossSectionPalmOutXZ("C:\\Users\\drowe\\bds_test9_xz.000.nc")
# print(bds_palm_output.normalise().add_normalised_coords_to_data().data)
