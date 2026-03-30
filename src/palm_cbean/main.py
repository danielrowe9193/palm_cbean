import animate
import palmout as po
import sys

data_input_filepath = sys.argv[1]
frame_storage_directory = sys.argv[2]
gif_storage_directory = sys.argv[3]
zu_xy_index = int(sys.argv[4])
gif_name = str(sys.argv[5])

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
