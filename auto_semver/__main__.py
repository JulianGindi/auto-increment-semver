import sys

from auto_semver.cli import parse_cli_arguments
from auto_semver.git import GitTagSource
from auto_semver.auto_semver import AutoSemver


def main():
    args = parse_cli_arguments()

    # TODO: Do some checking to determine which source to use.
    # For now, the only one we support is the GitTagSource
    git_semver_list = GitTagSource().get_semver_list()
    a = AutoSemver(git_semver_list, args.value, args.print_highest)
    a.auto_increment_semver()


if __name__ == "__main__":
    main()
