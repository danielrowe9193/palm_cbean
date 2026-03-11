import glob
import imageio.v2 as imageio
import palmout as po
import plot
import tqdm

filepath = "C:\\Users\\drowe\\flow_around_cube_cyclic_xy.000.nc"
cube_xy = po.PalmOutXY(palm_out_filepath=filepath)
cube_xy.normalise().add_normalised_coords_to_data()
cube_xy.show_info()

storage_dir = "C:\\Users\\drowe\\palm_cbean_plot_test_1"
frames = tqdm.tqdm(cube_xy.data.time.values)
for frame, _ in enumerate(frames):
    cube_xy_plot = plot.PlotPalmOutXY(palmout=cube_xy, storage_directory=storage_dir, frame=frame)
    cube_xy_plot.wind_speed_contour_fill_plot(zu_xy_index=0)
    cube_xy_plot.save_plot()

files = glob.glob("C:\\Users\\drowe\\palm_cbean_plot_test_1\\*.png")

print(files)

with imageio.get_writer("C:\\Users\\drowe\\palm_cbean.gif", mode="I", duration=0.2) as writer:
    for file in files:
        image = imageio.imread(file)
        writer.append_data(image)
