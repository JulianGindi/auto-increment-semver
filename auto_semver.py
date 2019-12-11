# pylint: disable=anomalous-backslash-in-string
import argparse
import re
import subprocess
import sys


def parse_semver_tags(raw_semver_text):
    semver_result_output = []
    regex_string = (
        "^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|"
        "[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-]"
        "[0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*"
        "))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*)"
        ")?$"
    )

    # Compiling regex to speed up matching during loop below.
    regex = re.compile(regex_string)

    for line in raw_semver_text.splitlines():
        # Removing the fixed part of the git tag output we won't need.
        line_cleaned = line.replace("refs/tags/", "")
        match = regex.match(line_cleaned)

        # Splitting up the matched results into their coresponding
        # regex match groups which will make our lives much easier.
        major, minor, patch, prerelease, buildmetadata = match.groups()

        # Creating a new entry containing all the resulting match data.
        semver_entry = {
            "semver": match.group(),
            "major": major,
            "minor": minor,
            "patch": patch,
            "prerelease": prerelease,
            "buildmetadata": buildmetadata,
        }
        semver_result_output.append(semver_entry)

    return semver_result_output


def get_remote_git_tags(remote):
    # Git command to list remote tags, only grabbing tags and not the
    # commit hashes.
    tag_command = "git ls-remote --tags -q {} | awk '{{print $2}}'".format(
        remote
    )

    command_output = subprocess.run(
        tag_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    # Checking to make sure our command succeeded. The stdout() function
    # returns None if the command fails and there is no output.
    if command_output.stderr != "":
        sys.exit("Error getting tags from remote")
    elif command_output.stdout == "":
        # There are no returned tags, writing a message to stdout and exiting.
        print("No tags found. Nothing to do.")
        sys.exit(0)

    return command_output.stdout


def get_highest_tag_from_list(tag_list):
    # We will start our comparisons with the first tag in the list.
    current_highest_tag = tag_list[0]

    for tag in tag_list[1:]:
        if int(tag["major"]) > int(current_highest_tag["major"]):
            current_highest_tag = tag
        elif int(tag["major"]) < int(current_highest_tag["major"]):
            continue
        elif int(tag["major"]) == int(current_highest_tag["major"]):
            # Now we search through the minor versions
            if int(tag["minor"]) > int(current_highest_tag["minor"]):
                current_highest_tag = tag
            elif int(tag["minor"]) < int(current_highest_tag["minor"]):
                continue
            elif int(tag["minor"]) == int(current_highest_tag["minor"]):
                if int(tag["patch"]) > int(current_highest_tag["patch"]):
                    current_highest_tag = tag
                elif int(tag["patch"]) < int(current_highest_tag["patch"]):
                    continue
                elif int(tag["patch"]) == int(current_highest_tag["patch"]):
                    # Values are identitcal, not sure how this happened.
                    continue

    return current_highest_tag


def increment_specified_semver_number(semver, value_to_increment):
    semver_part_as_int = int(semver[value_to_increment])
    semver[value_to_increment] = str(semver_part_as_int + 1)

    # If the value_to_increment is minor, we want to 'clear' the patch version.
    if value_to_increment == "minor":
        semver["patch"] = "0"

    semver["semver"] = "{}.{}.{}".format(
        semver["major"], semver["minor"], semver["patch"]
    )

    return semver


def auto_increment_semver_tags(args):
    remote_tag_text = get_remote_git_tags(args.remote)
    tag_list = parse_semver_tags(remote_tag_text)
    highest_tag = get_highest_tag_from_list(tag_list)
    auto_incremented_tag = increment_specified_semver_number(
        highest_tag, args.highest_value
    )
    print(auto_incremented_tag["semver"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto increment semver tags")

    # Adding one argument that represents the 'highest' value you would
    # want to increment.
    parser.add_argument(
        "--highest-value",
        type=str,
        default="patch",
        required=False,
        help="The highest value (minor or patch) to auto-increment",
    )

    parser.add_argument(
        "--remote",
        type=str,
        default="",
        required=False,
        help="A specific git origin to pull tags from",
    )

    args = parser.parse_args()
    auto_increment_semver_tags(args)
