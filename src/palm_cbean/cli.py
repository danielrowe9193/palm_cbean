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

    sub_parsers = parser.add_subparsers(dest="command", help="Interface different modules of palm-cbean.")

    topography_sub_parser = sub_parsers.add_parser("topography")

    parser.add_argument(
        "--input-xy",
        help="Path to the PALM xy output file."
    )

    parser.add_argument(
        "--input-xz",
        help="Path to the PALM xz output file."
    )

    parser.add_argument(
        "--variable",
        help="Variable name to be visualized."
    )

    parser.add_argument(
        "--zu-xy-index",
        help="The vertical index to choose in the xy plane."
    )

    parser.add_argument(
        "--y-xz-index",
        help="The meridional index to choose in the xz plane."
    )

    parser.add_argument(
        "--anim-name",
        help="Name of the animation."
    )

    parser.add_argument(
        "--frame-dir-name",
        help="Name of frame storage directory."
    )

    return parser.parse_args()

