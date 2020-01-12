# Auto Semver

![img](https://upload.wikimedia.org/wikipedia/commons/8/82/Semver.jpg)

A portable python script that aims let you focus on writing software, while it versions it for you. Strictly follows [Semver](https://semver.org/) using [Git tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging).

## Install

`pip install auto-semver`

## Usage

Running from within a git directory.

`auto-semver`

Specifying a specific remote.

`auto-semver --remote git@github.com:JulianGindi/auto-increment-semver.git`

Auto-incrementing a minor version

`auto-semver --value minor`

Just print out the current highest git semver tag

`auto-semver --print-highest`