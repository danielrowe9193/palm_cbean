import subprocess

from pathlib import Path


class Animator:
    """
    Utilities for animating outputs from PALM.
    """

    def __init__(self, frame_storage_directory: str):
        """
        Initialise the animator with a directory containing frames.

        Expects that the frames have already been generated and stored at the given frame directory. The Animator
        will return an error through ffmpeg if there are no frames (or frames of the incorrect format).
        :param frame_storage_directory: Directory containing the frames to be animated.
        """

        self.frame_storage_directory = Path(frame_storage_directory)

    def create_mp4(self, mp4_storage_directory: str, mp4_name: str):
        """
        Create mp4 animation from frames.

        WARNING: This method should be called only after frames have been generated to the temporary frame storage directory.

        :param mp4_storage_directory: The directory in which to store the mp4 animation.
        :param mp4_name: The name of the mp4 animation.
        :return: None
        """

        print("Creating MP4 video ... \n")

        mp4_file_path = Path(mp4_storage_directory) / mp4_name

        subprocess.run(
            [
                "ffmpeg",
                "-framerate", "30",
                "-i", "frame_%05d.png",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                str(mp4_file_path)
            ],
            cwd=self.frame_storage_directory,
            check=True,
        )

        print(f"Animated .mp4 stored at {mp4_file_path}")

        return None
