import palmout
import plot
import validation

from pathlib import Path


class Frames:
    """
    Utilities for the creation of frames.
    """

    def __init__(self, frame_storage_directory: str, po: palmout.PalmOut, var: str, index: int):
        """
        Initialise a frames object.
        :param frame_storage_directory: The name of the directory in which to store the frames.
        :param po: The PalmOut to be plotted.
        :param var: The variable to be visualised in the frames.
        :param index: The index/level for the frame slices to be visualised.
        """

        self.frame_storage_directory = Path(frame_storage_directory)
        self.po = po
        self.var = var
        self.index = index

    def generate_frames(self):
        """
        Generates and stores frames to the file store.

        Automatically detects the type of PalmOut.
        :return: None
        """

        Path(self.frame_storage_directory).mkdir(exist_ok=True)
        print(f"GENERATING FRAME STORAGE DIRECTORY AT {self.frame_storage_directory}")

        if validation.is_palmout_xy(self.po):

            print('GENERATING FRAMES FOR PALMOUTXY ... ')

            palm_out_plot = plot.PlotPalmOutXY(
                palmout=self.po,
                storage_directory=self.frame_storage_directory,
            )

            frames = self.po.data.time.values
            for frame, _ in enumerate(frames):

                if self.var == 'wspeed':
                    palm_out_plot.wind_speed_contour_fill_plot(time_index=frame, zu_xy_index=self.index)
                    print(f'Frame {frame:4d} stored in {self.frame_storage_directory}')
                elif self.var == 'w_xz':
                    palm_out_plot.w_contour_fill_plot(time_index=frame, zu_xy_index=self.index)
                    print(f'Frame {frame:4d} stored in {self.frame_storage_directory}')

            print(f"\nAll frames generated and stored in {self.frame_storage_directory}")

        elif validation.is_palmout_xz(self.po):

            print('GENERATING FRAMES FOR PALMOUTXZ ... ')

            palm_out_plot = plot.PlotPalmOutXZ(
                palmout=self.po,
                storage_directory=self.frame_storage_directory,
            )

            frames = self.po.data.time.values
            for frame, _ in enumerate(frames):

                if self.var == "wspeed":
                    palm_out_plot.wind_speed_contour_fill_plot(time_index=frame, y_xz_index=self.index)
                    print(f"Frame {frame:4d} stored in {self.frame_storage_directory}")
                elif self.var == "w_xz":
                    palm_out_plot.w_contour_fill_plot(time_index=frame, y_xz_index=self.index)
                    print(f"Frame {frame:4d} stored in {self.frame_storage_directory}")

            print(f"\nAll frames generated and stored in {self.frame_storage_directory}")

        else:

            print("NO VALID PALMOUT RECEIVED. NO FRAMES WILL BE GENERATED.")

        return None





