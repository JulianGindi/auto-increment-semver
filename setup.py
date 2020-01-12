from setuptools import setup

setup(
    name="auto-semver",
    version="0.5.0",
    description="Semver swiss-army knife",
    url="http://github.com/juliangindi/auto-semver",
    author="Julian Gindi",
    author_email="julian@gindi.io",
    license="MIT",
    packages=["auto_semver"],
    zip_safe=False,
    entry_points={
        "console_scripts": ["auto-semver=auto_semver.__main__:main",]
    },
)

