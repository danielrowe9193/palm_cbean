import animate
import cli
import palmout
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

po = None

if args.po == "xy":
    po = palmout.Loaders.load_xy(args.dp)
if args.po == "xz":
    po = palmout.Loaders.load_xz(args.dp)

anim = animate.Animator(palm_out=po)
anim.generate_frames_xy(variable=args.var, zu_xy_index=args.zu_xy_index)
# anim.generate_frames_xz(variable="w_xz", y_xz_index=3)
anim.animate_mp4(mp4_name=args.anim_name, new_frame_directory_name=args.frame_dir_name)
