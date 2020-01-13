class AutoSemver(object):
    def __init__(self, semver_list, value_to_increment, print_only):
        self.value_to_increment = value_to_increment
        self.print_only = print_only
        self.semver_list = semver_list

        # Creating some variables to hold the current parsed semver, and the
        # semver string that we will be updating to
        self.current_semver = None
        self.next_semver = None

    def _increment_specified_semver_number(self):
        # Starting by creating a "copy" of the current_semver value
        self.next_semver = self.current_semver

        if self.value_to_increment == "minor":
            semver_part_as_int = int(self.current_semver.minor)
            self.next_semver.minor = str(semver_part_as_int + 1)
            # If the value_to_increment is minor, we want to 'clear' the patch version.
            self.next_semver.patch = "0"
        else:
            semver_part_as_int = int(self.current_semver.patch)
            self.next_semver.patch = str(semver_part_as_int + 1)

        self.next_semver.semver = "{}.{}.{}".format(
            self.next_semver.major,
            self.next_semver.minor,
            self.next_semver.patch,
        )

        return self.next_semver

    def auto_increment_semver(self):
        # If we don't get any parsed tags back, we will print out an initial version.
        if len(self.semver_list) == 0:
            return "0.1.0"

        # Get reference to actual highest tag here
        self.current_semver = self.get_highest_semver_from_list()

        if self.print_only is True:
            print(self.current_semver.semver)
            return

        self._increment_specified_semver_number()

        semver_string = self.next_semver.semver

        if self.next_semver.version_prefix == True:
            semver_string = "v{}".format(self.next_semver.semver)

        print(semver_string)

    def get_highest_semver_from_list(self):
        # We will start our comparisons with the first tag in the list.
        current_highest_semver = self.semver_list[0]

        for tag in self.semver_list[1:]:
            if int(tag.major) > int(current_highest_semver.major):
                current_highest_semver = tag
            elif int(tag.major) < int(current_highest_semver.major):
                continue
            elif int(tag.major) == int(current_highest_semver.major):
                # Now we search through the minor versions
                if int(tag.minor) > int(current_highest_semver.minor):
                    current_highest_semver = tag
                elif int(tag.minor) < int(current_highest_semver.minor):
                    continue
                elif int(tag.minor) == int(current_highest_semver.minor):
                    if int(tag.patch) > int(current_highest_semver.patch):
                        current_highest_semver = tag
                    elif int(tag.patch) < int(current_highest_semver.patch):
                        continue
                    elif int(tag.patch) == int(current_highest_semver.patch):
                        # Values are identitcal, not sure how this happened.
                        continue

        self.current_semver = current_highest_semver
        return current_highest_semver
