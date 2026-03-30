import animate
import palmout as po

data_input_filepath = "path/to/palmoutdata/"
frame_storage_directory = "/directory/to/store/frames"
gif_storage_directory = "/directory/to/store/frames"
zu_xy_index = 0
gif_name = "nameofgif.gif"

palmout_xy = po.PalmOutXY(palm_out_filepath=data_input_filepath)
palmout_xy.normalise().add_normalised_coords_to_data()

animate.generate_frames_xy(
    palm_out=palmout_xy,
    storage_directory=frame_storage_directory,
    zu_xy_index=zu_xy_index
)

animate.animate(
    frame_storage_directory=frame_storage_directory,
    gif_storage_directory=gif_storage_directory,
    gif_name=gif_name
)
