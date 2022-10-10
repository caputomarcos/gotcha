"""setup GOTCHA_TTY
"""
__updated__ = "2022-10-09 22:12:32"

import os
import sys
from configparser import ConfigParser
from typing import Any, List
from subprocess import check_call
from pkg_resources import parse_requirements
from setuptools import setup, Command
from setuptools.command.install import install
import subprocess

NAME = "gotcha"
VERSION = None

# # root privileges
# if os.geteuid() != 0:
#     print("\n\n\t*** root privileges required for this software. ***\n")
#     sys.exit(1)

here = os.path.abspath(os.path.dirname(__file__))

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    SLUG = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, SLUG, "__version__.py"), encoding="utf-8") as f:
        exec(f.read(), about)  # pylint: disable=exec-used
else:
    about["__version__"] = VERSION

# get the long description from the README.rst
with open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()


class ListDependenciesCommand(Command):
    """A custom command to list dependencies"""

    description = "list package dependencies"
    user_options: List[Any] = []

    def initialize_options(self):
        """initialize_options"""

    def finalize_options(self):
        """finalize_options"""

    def run(self):
        """run"""
        cfg = ConfigParser()
        cfg.read("setup.cfg")
        requirements = cfg["options"]["install_requires"]
        print(requirements)


class PyInstallerCommand(Command):
    """A custom command to run PyInstaller to build standalone executable."""

    description = "run PyInstaller on gotcha entrypoint"
    user_options: List[Any] = []

    def initialize_options(self):
        """initialize_options"""

    def finalize_options(self):
        """finalize_options"""

    def run(self):
        """run"""
        cfg = ConfigParser()
        cfg.read("setup.cfg")
        command = [
            "pyinstaller",
            "--additional-hooks-dir",
            "pyinstaller_hooks",
            "--clean",
            "--onefile",
            "--name",
            "gotcha",
        ]
        setup_cfg = cfg["options"]["install_requires"]
        requirements = parse_requirements(setup_cfg)
        for _r in requirements:
            command.extend(["--hidden-import", _r.key])
        command.append("gotcha/__main__.py")
        print(" ".join(command))
        check_call(command)


def compile_and_install_software():
    """Used the subprocess module to compile/install the C software."""
    # compile & install the process hider
    subprocess.check_call('sudo make install', cwd='./hider/', shell=True)


class CustomInstall(install):
    """Custom handler for the 'install' command."""

    def run(self):
        compile_and_install_software()
        super().run()


setup(
    name="ttyGotcha",
    # use_scm_version={"fallback_version": "noversion"},
    version=about["__version__"],
    cmdclass={
        'install': CustomInstall,
        "dependencies": ListDependenciesCommand,
        "pyinstaller": PyInstallerCommand,
    },
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
            "gotcha = gotcha:__main__.main",
        ]
    },
    python_requires=">=3.10.7",
    include_package_data=True,
)
