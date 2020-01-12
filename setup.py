from setuptools import setup

setup(
    name="auto-semver",
    version="0.4.0",
    description="Semver swiss-army knife",
    url="http://github.com/juliangindi/auto-semver",
    author="Julian Gindi",
    author_email="julian@gindi.io",
    license="MIT",
    packages=["auto_semver"],
    scripts=["bin/auto-semver"],
    zip_safe=False,
)

