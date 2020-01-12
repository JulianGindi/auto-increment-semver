import sys

import auto_semver
from auto_semver import parse_cli_arguments, auto_increment_semver_tags


def main():
    args = parse_cli_arguments()
    auto_increment_semver_tags(args)


if __name__ == "__main__":
    main()
