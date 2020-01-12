# pylint: disable=anomalous-backslash-in-string
import argparse
import re
import subprocess
import sys


def parse_semver_tags(raw_semver_text):
    semver_result_output = []

    # Keeping track of if we need to support the "v" sometimes used before
    # a semver string. Example: v2.0.1
    version_character_used = False

    # This is a wild regex, but it comes directly from the semver docs.
    # More here: https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
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

        # We will be left with a raw semver or one beginning with a "v".
        if line_cleaned[0] == "v":
            line_cleaned = line_cleaned.replace("v", "")
            version_character_used = True

        match = regex.match(line_cleaned)

        # We don't do anything if we don't have a valid semver
        if match is None:
            continue

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
            "version_prefix": version_character_used,
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

    # If we don't get any parsed tags back, we will print out an initial version.
    if len(tag_list) == 0:
        print("0.1.0")
        return

    highest_tag = get_highest_tag_from_list(tag_list)

    if args.print_highest is True:
        print(highest_tag["semver"])
        return

    auto_incremented_tag = increment_specified_semver_number(
        highest_tag, args.value
    )

    semver_string = auto_incremented_tag["semver"]

    if highest_tag["version_prefix"] == True:
        semver_string = "v{}".format(auto_incremented_tag["semver"])

    print(semver_string)


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
