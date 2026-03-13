import animate
import palmout as po

filepath = "C:\\Users\\drowe\\flow_around_cube_cyclic_xy.000.nc"
palmout_xy = po.PalmOutXY(palm_out_filepath=filepath)
palmout_xy.normalise().add_normalised_coords_to_data()

storage_dir = "C:\\Users\\drowe\\palm_cbean_plot_test_1"
animate.generate_frames_xy(palm_out=palmout_xy, storage_directory=storage_dir)

frame_storage_directory = "C:\\Users\\drowe\\palm_cbean_plot_test_1"
gif_storage_directory = "C:\\Users\\drowe"
animate.animate(frame_storage_directory=gif_storage_directory, gif_storage_directory=gif_storage_directory, gif_name="flow_past_cubes.gif")
