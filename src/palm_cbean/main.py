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
bds_topo.make_shape_even()
bds_topo.flip()
bds_topo.mask()
# bds_topo.downscale(final_resolution=100)
# bds_topo.smooth()
# bds_topo.mask()

print(
    f"{bds_topo.dataset}"
)

palmout_xy = palmout.PalmOutXY(
    palm_out_filepath=Path("../../data/toy_model_xy.002.nc")
)
palmout_xy.normalise()
palmout_xy.update_data_with_normalised_coords()


# plot.PlotTopography(bds_topo).plot_elevation()
# plot.PlotTopography(bds_topo).plot_xz_cross_section(norm_y=0.5)
# plot = plot.PlotPalmOutXY(
#     palmout=palmout_xy,
#     storage_directory=config.Constants.plot_storage_directory,
# )
# plot.wind_speed_contour_fill_plot(time_index=20, zu_xy_index=2)

gif_anim = animate.Animator(palm_out=palmout_xy)
# gif_anim.generate_frames_xy(variable="wspeed", zu_xy_index=2)
# gif_anim.animate_gif(gif_name="test.gif", new_frame_directory_name="toy_model_xy.002", keep_frames=False)

