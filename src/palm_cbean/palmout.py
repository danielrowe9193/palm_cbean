import xarray


class PalmOut:
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


# bds_palm_output = PalmOut("C:\\Users\\drowe\\bds_test9_t58_slice.nc")
# bds_palm_output_xy = bds_palm_output.xy_cross_section(z=40)
# print(bds_palm_output_xy)
