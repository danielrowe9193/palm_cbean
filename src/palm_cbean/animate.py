import glob
import imageio.v2 as imageio
import os
import tqdm

import palmout
import plot


def generate_frames_xy(palm_out: palmout.PalmOutXY, storage_directory: str) -> None:
    """Get the frames from the time values within the PalmOut file."""
    print("Generating frames...")
    frames = tqdm.tqdm(palm_out.data.time.values)
    for frame, _ in enumerate(frames):
        po = plot.PlotPalmOutXY(palmout=palm_out, storage_directory=storage_directory, frame=frame)
        po.wind_speed_contour_fill_plot(zu_xy_index=0)
        po.save_plot()


def animate(frame_storage_directory: str, gif_storage_directory: str, gif_name: str):
    """Generate animated gif of the frames"""
    print("Creating animated gif...\n")

    files = glob.glob(f"{frame_storage_directory}\\*.png")

    with imageio.get_writer(f"{gif_storage_directory}\\{gif_name}", mode="I", duration=0.2) as writer:
        for file in files:
            image = imageio.imread(file)
            writer.append_data(image)

    print(f"Animated GIF stored at {gif_storage_directory}\\{gif_name}")
