# Module for command line interface.

import argcomplete
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
    
    topo.add_argument(
        '--output',
        help='Path to store the topography file.'
    )

    gen_frames = subparsers.add_parser(
        "gen_frames",
        help="Generate and store frames in a directory."
    )

    gen_frames.add_argument(
        '--po',
        required=True,
        help="Specify the palm output. Options are 'xy', 'xz'"
    )

    gen_frames.add_argument(
        "--dp",
        required=True,
        type=Path,
        help="Path to the palm output file."
    )

    gen_frames.add_argument(
        "--fdn",
        help="Name of frame storage directory."
    )

    gen_frames.add_argument(
        "--var",
        required=True,
    )

    gen_frames.add_argument(
        "--i",
        type=int,
        help="The index representing the slice of the given palm output."
    )

    animate = subparsers.add_parser(
        "animate",
        help="Animate PALM output."
    )

    animate.add_argument(
        "--fd",
        help="The frame storage directory."
    )

    animate.add_argument(
        "--dir",
        help='The directory to store the animation.',
        required=True,
        default=Path("../../plots")
    )

    animate.add_argument(
        '--an',
        help='The name of the animation.',
        type=Path,
        default='animation.mp4',
    )

    argcomplete.autocomplete(parser)

    return parser.parse_args()

