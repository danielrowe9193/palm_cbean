import config
import imageio.v2 as imageio
import plot
import subprocess
import utils

from palmout import (
    PalmOutXZ, PalmOutXY
)
from pathlib import Path


class Animator:
    """
    Utilities for animating outputs from PALM.

    Creates animated GIFs of the simulation results.
    """

    def __init__(self, palm_out: PalmOutXY | PalmOutXZ):
        """
        Initialise the animator with PalmOut data.

        Expects the data to be of type palmout.PalmOut and currently
        animates _xy and _xz files.
        :param palm_out: The PalmOut file to be animated.
        """
        self.palm_out = palm_out
        self.temp_frame_storage = "../../plots/temp_frame_store/"

    def generate_frames_xy(self, variable: str, zu_xy_index: int = 0):
        """
        Generates and stores frames to a temporary file store.

        :param zu_xy_index: The vertical index of the _xy data to be animated.
        :param variable: The variable to be plotted.
        :return:
        """

        if type(self.palm_out) is not PalmOutXY:
            return TypeError("Expected type of PalmOut is PalmOutXY.")

        Path(self.temp_frame_storage).mkdir(exist_ok=True)
        print("Generated temporary frame storage directory.")

        print("Generating frames ... ")

        palm_out_plot = plot.PlotPalmOutXY(
            palmout=self.palm_out,
            storage_directory=self.temp_frame_storage,
        )

        frames = self.palm_out.data.time.values
        for frame, _ in enumerate(frames):

            if variable == "wspeed":
                palm_out_plot.wind_speed_contour_fill_plot(time_index=frame, zu_xy_index=zu_xy_index)
                print(f"Frame {frame:4d} stored in {self.temp_frame_storage}")

        print(f"\nAll frames generated and stored in {self.temp_frame_storage}")

        return None

    def generate_frames_zy(self, storage_directory: str, y_xz_index: int = 0):
        ...

    def animate_gif(self, gif_name: str, new_frame_directory_name: str | Path, keep_frames: bool = False):
        """
        Creates an animated gif using the frames stored in the temporary frame store.
        By default, this method will delete the temporary frame store.
        Stores the animated gif in the plots directory of the project.

        WARNING: This method should be called only after frames have been generated to the temporary frame storage directory.

        :param gif_name: The name of the animated GIF.
        :param new_frame_directory_name: The name of directory frames should be stored in, if keep_frames=True.
        :param keep_frames: Determines if to keep the temporary frame store or not.
        :return:
        """

        print("Creating animated gif...\n")

        new_frame_directory = Path(f"../../plots/{new_frame_directory_name}")

        if keep_frames is not False:
            frame_dir = Path(self.temp_frame_storage).rename(new_frame_directory)
            print(f"keep_frames=True. Frames are being stored at {frame_dir}.\n")
        else:
            frame_dir = Path(self.temp_frame_storage)
            print(f"keep_frames=False. The frames will remain in the temporary frame store.")

        gif_path = config.Constants.plot_storage_directory / gif_name

        with imageio.get_writer(gif_path, mode="I", duration=0.2) as writer:
            for file in frame_dir.iterdir():
                image = imageio.imread(file)
                writer.append_data(image)

        print(f"Animated GIF stored at {gif_path}")

        utils.DirectoryManagement.clear_temp_frame_dir()

        return None

    def animate_mp4(self, mp4_name: str, new_frame_directory_name: str | Path, keep_frames: bool = False):
        """
        Creates MP4 video using the frames stored in the temporary frame store.
        By default, this method will delete the temporary frame store.
        Stores the animated gif in the plots directory of the project.

        WARNING: This method should be called only after frames have been generated to the temporary frame storage directory.

        :param mp4_name: The name of the animated GIF.
        :param new_frame_directory_name: The name of directory frames should be stored in, if keep_frames=True.
        :param keep_frames: Determines if to keep the temporary frame store or not.
        :return:
        """
        
        print("Creating MP4 video ... \n")
        
        new_frame_directory = Path(f"../../plots/{new_frame_directory_name}")

        mp4_file_path = config.Constants.plot_storage_directory / mp4_name
        
        if keep_frames is not False:
            frame_dir = Path(self.temp_frame_storage).rename(new_frame_directory)
            print(f"keep_frames=True. Frames are being stored at {frame_dir}.\n")
        else:
            frame_dir = Path(self.temp_frame_storage)
            print(f"keep_frames=False. The frames will remain in the temporary frame store.")

        subprocess.run(
            [
                "ffmpeg",
                "-framerate", "5",
                "-i", "frame_%05d.png",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                str(mp4_file_path)
            ],
            cwd=self.temp_frame_storage,
            check=True,
        )
        
        print(f"Animated GIF stored at {mp4_file_path}")

        utils.DirectoryManagement.clear_temp_frame_dir()

        return None

        
        
