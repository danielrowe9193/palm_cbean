# Module for command line interface.

import argparse


def parse_arguments():
    """
    Function for handling arguments in the CLI.
    :return:
    """

    parser = argparse.ArgumentParser(
        description="palm_cbean: Utilities for handling palm in Caribbean context."
    )

    parser.add_argument(
        "--input_xy",
        help="Path to the PALM xy output file."
    )

    parser.add_argument(
        "--input_xz",
        help="Path to the PALM xz output file."
    )

    parser.add_argument(
        "--variable",
        help="Variable name to be visualized."
    )

    parser.add_argument(
        "--zu_xy_index",
        help="The vertical index to choose in the xy plane."
    )

    parser.add_argument(
        "--y_xz_index",
        help="The meridional index to choose in the xz plane."
    )

    parser.add_argument(
        "--anim_name",
        help="Name of the animation."
    )

    parser.add_argument(
        "--frame_dir_name",
        help="Name of frame storage directory."
    )

    return parser.parse_args()

