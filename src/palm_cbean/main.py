import animate
import cli
import config
import palmout
import plot
import utils

from pathlib import Path
from topography import Topography

utils.DirectoryManagement.make_data_directory()
utils.DirectoryManagement.make_plots_directory()

args = cli.parse_arguments()

# bds_topo = Topography(
#     filepath=config.Constants.bds_topography_path
# )
# bds_topo.mask()
# bds_topo.flip()
# bds_topo.make_shape_even()
# bds_topo.pad(amount=5000)
# bds_topo.downscale(final_resolution=100)
# bds_topo.mask()
# print(bds_topo.shape)

# plot.PlotTopography(bds_topo).plot_elevation()

palmout_xy = palmout.PalmOutXY(
    palm_out_filepath=Path(args.input_xy)
)
palmout_xy.normalise()
palmout_xy.update_data_with_normalised_coords()

palmout_xz = palmout.PalmOutXZ(
    palm_out_filepath=Path(args.input_xz)
)
palmout_xz.normalise()
palmout_xz.update_data_with_normalised_coords()

anim = animate.Animator(palm_out=palmout_xz)
anim.generate_frames_xy(variable=args.variable, zu_xy_index=args.zu_xy_index)
# anim.generate_frames_xz(variable="w_xz", y_xz_index=3)
anim.animate_mp4(mp4_name=args.anim_name, new_frame_directory_name=args.frame_dir_name)

