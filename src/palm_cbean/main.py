import animate
import config
import matplotlib.pyplot as plt
import numpy as np
import palmout
import plot
import utils

from pathlib import Path
from topography import Topography

utils.DirectoryManagement.make_data_directory()
utils.DirectoryManagement.make_plots_directory()

bds_topo = Topography(
    filepath=config.Constants.bds_topography_path
)

palmout_xy = palmout.PalmOutXY(
    palm_out_filepath=Path("../../data/toy_model_xy.002.nc")
)
palmout_xy.normalise()
palmout_xy.update_data_with_normalised_coords()

palmout_xz = palmout.PalmOutXZ(
    palm_out_filepath=Path("../../data/bds_test9_xz.000.nc")
)
palmout_xz.normalise()
palmout_xz.update_data_with_normalised_coords()

print(palmout_xz.data)

anim = animate.Animator(palm_out=palmout_xz)
# anim.generate_frames_xy(variable="wspeed", zu_xy_index=2)
anim.generate_frames_xz(variable="w_xz", y_xz_index=2)
# anim.animate_mp4(mp4_name="test.mp4", new_frame_directory_name="toy_model_xy.002")

