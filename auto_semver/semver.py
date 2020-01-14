# pylint: disable=anomalous-backslash-in-string
import re


class Semver(object):
    def __init__(self, semver_string):
        self.original_semver_string = semver_string
        semver_dict = self._parse_semver_string(semver_string)

        if semver_dict is None:
            # We were not able to parse the semver string, return an error
            raise ValueError(
                "Invalid semver string, {}, being parsed.".format(
                    self.original_semver_string
                )
            )

        self.semver = semver_dict["semver"]
        self.major = semver_dict["major"]
        self.minor = semver_dict["minor"]
        self.patch = semver_dict["patch"]
        self.prerelease = semver_dict["prerelease"]
        self.version_prefix = semver_dict["version_prefix"]
        self.buildmetadata = semver_dict["buildmetadata"]

    def _parse_semver_string(self, semver_string):
        semver_dict = {"version_prefix": False}

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

        if semver_string.startswith("v"):
            semver_string = semver_string.replace("v", "")

            # Keeping track of if we need to support the "v" sometimes used before
            # a semver string. Example: v2.0.1
            semver_dict["version_prefix"] = True

        match = regex.match(semver_string)

        if match is None:
            return None

        # Splitting up the matched results into their coresponding
        # regex match groups which will make our lives much easier.
        major, minor, patch, prerelease, buildmetadata = match.groups()
        semver_dict["semver"] = match.group()
        semver_dict["major"] = major
        semver_dict["minor"] = minor
        semver_dict["patch"] = patch
        semver_dict["prerelease"] = prerelease
        semver_dict["buildmetadata"] = buildmetadata

        return semver_dict
