from abc import ABC, abstractmethod
import xarray

from pathlib import Path


class PalmOut(ABC):
    """Absract PalmOut class."""

    def __init__(self, palm_out_filepath: str | Path):
        """
        Initialize a PalmOut object with a specified filepath.
        :param palm_out_filepath: The filepath
        """

        try:
            self.palm_out_filepath = Path(palm_out_filepath)
            self.data = xarray.open_dataset(self.palm_out_filepath, engine='netcdf4', decode_timedelta=False)
        except:
            pass

        self.x: int | None = None
        self.y: int | None = None
        self.z: int | None = None
        self.t: int | None = None

    @abstractmethod
    def show_info(self):
        """Print information about the PalmOut dataset."""
        print(self.data)

    @abstractmethod
    def normalise(self):
        """Normalise spatial coordinates between 0 and 1."""
        return self

    @abstractmethod
    def update_data_with_normalised_coords(self):
        """Update the data of the PalmOut with the normalised coordinates."""
        return self


class PalmOutXZ(PalmOut):
    """Initialise a PalmOut that represents an XZ cross-section."""

    def show_info(self):
        """Print information about the PalmOut dataset."""
        print(self.data)

    def normalise(self) -> PalmOut:
        """Normalise x and z coordinates between 0 and 1."""
        self.x = (self.data.xu.values - self.data.xu.values.min()) / (self.data.xu.values.max() - self.data.xu.values.min())
        self.z = (self.data.zu.values - self.data.zu.values.min()) / (self.data.zu.values.max() - self.data.zu.values.min())
        return self

    def update_data_with_normalised_coords(self) -> PalmOut:
        """Update the data of the PalmOut with the normalised coordinates."""
        self.data = self.data.assign_coords(norm_x=self.x)
        self.data = self.data.assign_coords(norm_z=self.z)
        return self


class PalmOutXY(PalmOut):
    """Initialise a PalmOut that represents an XY cross-section."""

    def show_info(self):
        """Print information about the PalmOut dataset."""
        print(self.data)

    def normalise(self) -> PalmOut:
        """Normalise x and y coordinates between 0 and 1."""
        self.x = (self.data.x.values - self.data.x.values.min()) / (self.data.x.values.max() - self.data.x.values.min())
        self.y = (self.data.y.values - self.data.y.values.min()) / (self.data.y.values.max() - self.data.y.values.min())
        return self

    def update_data_with_normalised_coords(self):
        """Update the data of the PalmOut with the normalised coordinates."""
        self.data = self.data.assign_coords(norm_x=self.x)
        self.data = self.data.assign_coords(norm_y=self.y)
        return self
