import sys

from auto_semver.cli import parse_cli_arguments
from auto_semver.git import GitTagSource, GitTagger
from auto_semver.auto_semver import AutoSemver
from auto_semver.file_replacer import SemverFileReplacer


def main():
    args = parse_cli_arguments()

    if args.file is not "":
        # We will use the specified file as our semver source.
        sfr = SemverFileReplacer(args.file, args.value)
        sfr.find_and_replace_semver_instances()
        sys.exit("Updated semver values in {}".format(args.file))

    git_semver_list = GitTagSource(args.use_local).get_semver_list()
    a = AutoSemver(git_semver_list, args.value, args.print_highest)
    next_tag = a.print()

    if args.should_tag:
        git_tagger = GitTagger(next_tag)
        git_tagger.tag_local()
    else:
        print(next_tag)


if __name__ == "__main__":
    main()
