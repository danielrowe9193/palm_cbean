import imageio.v2 as imageio
import palmout
import plot
import tqdm

from pathlib import Path


def generate_frames_xy(palm_out: palmout.PalmOutXY, storage_directory: str, zu_xy_index: int = 0) -> None:
    """Get the frames from the time values within the PalmOut file."""
    print("Generating frames...")

    storage_dir = Path(storage_directory)

    frames = tqdm.tqdm(palm_out.data.time.values)
    for frame, _ in enumerate(frames):
        po = plot.PlotPalmOutXY(palmout=palm_out, storage_directory=storage_dir, frame=frame)
        po.wind_speed_contour_fill_plot(zu_xy_index=zu_xy_index)
        po.save_plot()

    print(f"All frames generated and stored in {storage_directory}")


def generate_frames_xz(palm_out: palmout.PalmOutXZ, storage_directory: str, y_xz_index: int = 0) -> None:
    """Get the frames from the time values within the PalmOut file."""
    print("Generating frames...")

    storage_dir = Path(storage_directory)

    frames = tqdm.tqdm(palm_out.data.time.values)
    for frame, _ in enumerate(frames):
        po = plot.PlotPalmOutXZ(palmout=palm_out, storage_directory=storage_dir, frame=frame)
        po.wind_speed_contour_fill_plot(y_xz_index=y_xz_index)
        po.save_plot()

    print(f"All frames generated and stored in {storage_directory}")


def animate(frame_storage_directory: str, gif_storage_directory: str, gif_name: str):
    """Generate animated gif of the frames"""
    print("Creating animated gif...\n")

    frame_dir = Path(frame_storage_directory)
    gif_path = Path(gif_storage_directory) / gif_name

    files = frame_dir.glob("*.png")

    with imageio.get_writer(gif_path, mode="I", duration=0.2) as writer:
        for file in files:
            image = imageio.imread(file)
            writer.append_data(image)

    print(f"Animated GIF stored at {gif_path}")
