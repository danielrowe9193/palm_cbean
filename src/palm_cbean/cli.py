# Module for command line interface.

import argparse

from pathlib import Path


def parse_arguments():
    """
    Function for handling arguments in the CLI.
    :return:
    """

    parser = argparse.ArgumentParser(
        description="palm_cbean: Utilities for handling palm in Caribbean context."
    )

    parser.add_argument(
        "--po",
        required=True,
        help="Define the palm output. Options are 'xy', 'xz'"
    )

    parser.add_argument(
        "--dp",
        required=True,
        type=Path,
        help="Path to the palm output file."
    )

    parser.add_argument(
        "--var",
        help="Variable to be visualized."
    )

    parser.add_argument(
        "--i",
        type=int,
        help="The index representing the slice of the given palm output."
    )

    parser.add_argument(
        "--an",
        help="Name of the animation."
    )

    parser.add_argument(
        "--fdn",
        help="Name of frame storage directory."
    )

    return parser.parse_args()

