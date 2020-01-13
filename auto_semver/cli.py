import argparse


def parse_cli_arguments():
    parser = argparse.ArgumentParser(description="Auto increment semver tags")

    # Adding one argument that represents the 'highest' value you would
    # want to increment.
    parser.add_argument(
        "--value",
        type=str,
        default="patch",
        choices=["major", "minor", "patch"],
        required=False,
        help="The highest semver element value to auto-increment",
    )

    parser.add_argument(
        "--remote",
        type=str,
        default="",
        required=False,
        help="A specific git origin to pull tags from",
    )

    parser.add_argument(
        "--print-highest",
        dest="print_highest",
        action="store_true",
        default=False,
        required=False,
        help="Should the script just print the highest semver value without auto-incrementing?",
    )

    return parser.parse_args()
