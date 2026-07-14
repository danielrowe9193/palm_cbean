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

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    topo = subparsers.add_parser(
        "topography",
        help="Generate topography."
    )

    topo.add_argument(
        '--input',
        type=Path,
        required=True
    )

    topo.add_argument(
        '--pad',
        default=1000
    )

    topo.add_argument(
        '--resolution',
        default=100
    )

    animate = subparsers.add_parser(
        "animate",
        help="Animate PALM output."
    )

    animate.add_argument(
        "--variable",
        required=True,
    )

    animate.add_argument(
        "--dir",
        help='The directory to store the animation.',
        required=True
    )

    animate.add_argument(
        "--output",
        help='The name of the animation.',
        type=Path,
        default="animation.mp4",
        required=True
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

