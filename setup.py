#!/usr/bin/env python3
"""_summary_
    """
from io import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))


# get the long description from the README.rst
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ttyGotcha",
    version="0.0.5",
    description="SSH-TTY control Interface",
    long_description=long_description,
    author="Marcos Caputo",
    author_email="caputo.marcos@gmail.com",
    url="https://github.com/caputomarcos/gotcha",
    packages=[
        "gotcha",
    ],
    license="MIT",
    install_requires=[
        "psutil==5.9.2",
    ],
    entry_points={
        "console_scripts": [
            "gotcha = gotcha:main",
        ]
    },
    python_requires=">=3.10",
    include_package_data=True,
)
