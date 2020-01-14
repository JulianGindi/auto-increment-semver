import re

from .semver import Semver
from .auto_semver import AutoSemver


class SemverFileReplacer(object):
    def __init__(self, filename, value_to_increment):
        self.filename = filename
        self.value_to_increment = value_to_increment

    def find_and_replace_semver_instances(self):
        with open(self.filename, "r") as f:
            file_data = f.read()

        semver_matches = self._find_semver_values(file_data)
        if len(semver_matches) is 0:
            # Return some error message that there were no matching semvers
            print("No matching semver values in specified file.")
            return

        for match in semver_matches:
            semver_match_obj = Semver(match)
            as_obj = AutoSemver(
                [semver_match_obj], self.value_to_increment, False
            )
            file_data = file_data.replace(match, as_obj.next_semver.semver)

        with open(self.filename, "w") as f:
            f.write(file_data)

    def _find_semver_values(self, text_string):
        # We will use a "lighter" regex for searching because the context
        # will be much "messier".
        pattern = "[0-9]+.[0-9]+.[0-9]+"
        return re.findall(pattern, text_string)
