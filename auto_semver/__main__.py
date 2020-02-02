import sys

from auto_semver.cli import parse_cli_arguments
from auto_semver.git import GitTagSource, GitTagger
from auto_semver.auto_semver import AutoSemver


def main():
    args = parse_cli_arguments()

    # TODO: Do some checking to determine which source to use.
    # For now, the only one we support is the GitTagSource
    git_semver_list = GitTagSource(args.use_local).get_semver_list()
    a = AutoSemver(git_semver_list, args.value, args.print_highest)
    next_tag = a.auto_increment_semver()

    if args.should_tag:
        git_tagger = GitTagger(next_tag)
        git_tagger.tag_local()
    else:
        print(next_tag)


if __name__ == "__main__":
    main()
