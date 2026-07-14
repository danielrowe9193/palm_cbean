import animate
import cli
import frames
import palmout
import plot
import topography as topo

args = cli.parse_arguments()

po = None

if args.po == "xy":
    po = palmout.Loaders.load_xy(args.dp)
    print(type(po))
if args.po == "xz":
    po = palmout.Loaders.load_xz(args.dp)
    print(type(po))

if args.command == "topography":
    bds_topo = topo.Topography(
        filepath=args.input
    )
    bds_topo.mask()
    bds_topo.flip()
    bds_topo.make_shape_even()
    bds_topo.pad(amount=args.pad)
    bds_topo.downscale(final_resolution=args.resolution)
    bds_topo.mask()
    print(bds_topo.shape)

    plot.PlotTopography(bds_topo).plot_elevation()

# anim = animate.Animator(palm_out=po)
# anim.generate_frames(variable=args.var, index=args.i)
# anim.generate_frames_xy(variable=args.var, zu_xy_index=args.i)
# anim.generate_frames_xz(variable="w_xz", y_xz_index=3)
# anim.animate_mp4(mp4_name=args.an, new_frame_directory_name=args.fdn)

if args.command == 'animate':
    frames = frames.Frames(
        frame_storage_directory=args.fdn,
        po=po,
        var=args.var,
        index=args.i
    )
    frames.generate_frames()

    anim2 = animate.Animator2(
        frames=frames
    )
    anim2.create_mp4(
        mp4_storage_directory=args.dir,
        mp4_name=args.output
    )
