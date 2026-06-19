import animate
import palmout
import utils

from pathlib import Path

utils.DirectoryManagement.make_data_directory()
utils.DirectoryManagement.make_plots_directory()

palmout_xy = palmout.PalmOutXY(
    palm_out_filepath=Path("../../data/toy_model_xy.002.nc")
)
palmout_xy.normalise()
palmout_xy.update_data_with_normalised_coords()

print(
    palmout_xy.data
)

gif_anim = animate.Animator(palm_out=palmout_xy)
gif_anim.generate_frames_xy(variable="wspeed", zu_xy_index=2)
gif_anim.animate_gif(gif_name="test.gif", new_frame_directory_name="toy_model_xy.002", keep_frames=False)

