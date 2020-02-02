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

    parser.add_argument(
        "--use-local",
        action="store_true",
        default=False,
        required=False,
        help="Should the script reference local git tags instead of remote?",
    )

    parser.add_argument(
        "-t",
        "--tag",
        dest="should_tag",
        action="store_true",
        default=False,
        required=False,
        help="Do you want auto-semver to automatically create a new git tag for you locally?",
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="",
        required=False,
        help="If specified, the single file to use for looking up semver values, which them increments them in-place based on --value.",
    )

    return parser.parse_args()
