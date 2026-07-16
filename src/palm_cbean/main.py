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
if args.po == "xz":
    po = palmout.Loaders.load_xz(args.dp)

if args.command == "topography":
    bds_topo = topo.Topography(
        filepath=args.input
    )
    bds_topo.mask()
    bds_topo.flip()
    bds_topo.make_shape_even()
    bds_topo.pad(amount=args.pad)
    if args.resolution is None:
        pass
    else:
        bds_topo.downscale(final_resolution=args.resolution)
    bds_topo.mask()
    print(bds_topo.shape)

    plot.PlotTopography(bds_topo).plot_elevation()

if args.command == 'gen_frames':
    frames = frames.Frames(
        frame_storage_directory=args.fdn,
        po=po,
        var=args.var,
        index=args.i
    )
    frames.generate_frames()

if args.command == 'animate':
    anim2 = animate.Animator(
        frame_storage_directory=args.fdn
    )
    anim2.create_mp4(
        mp4_storage_directory=args.dir,
        mp4_name=args.an
    )
