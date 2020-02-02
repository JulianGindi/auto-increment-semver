# Auto Semver

![img](https://upload.wikimedia.org/wikipedia/commons/8/82/Semver.jpg)

A small python tool that aims to let you focus on writing software, while it versions it for you. Strictly follows [Semver](https://semver.org/) using [Git tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging) (more flexible support coming soon).

## Install

`pip install auto-semver`

## Usage

Run from within a git directory, will print the next Semver value to use by incrementing the patch number.

`auto-semver`

Run using local git tags (not from a remote).

`auto-semver --use-local`

Specifying a specific git remote.

`auto-semver --remote git@github.com:JulianGindi/auto-increment-semver.git`

Auto-incrementing a minor version.

`auto-semver --value minor`

Just print out the current highest git semver tag.

`auto-semver --print-highest`

You can also have auto-semver create a git tag for you locally by running a `git tag` command.

`auto-semver -t`
