"""setup GOTCHA_TTY
"""
__updated__ = "2022-09-25 22:31:15"

import os
from configparser import ConfigParser
from typing import Any, List
from subprocess import check_call
from pkg_resources import parse_requirements
from setuptools import setup, Command

NAME = 'gotcha'
VERSION = None

here = os.path.abspath(os.path.dirname(__file__))

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    SLUG = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, SLUG, '__version__.py'), encoding='utf-8') as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class ListDependenciesCommand(Command):
    """A custom command to list dependencies"""

    description = "list package dependencies"
    user_options: List[Any] = []

    def initialize_options(self):
        """initialize_options
        """

    def finalize_options(self):
        """finalize_options
        """

    def run(self):
        """run
        """
        cfg = ConfigParser()
        cfg.read("setup.cfg")
        requirements = cfg["options"]["install_requires"]
        print(requirements)


class PyInstallerCommand(Command):
    """A custom command to run PyInstaller to build standalone executable."""

    description = "run PyInstaller on gotcha entrypoint"
    user_options: List[Any] = []

    def initialize_options(self):
        """initialize_options
        """

    def finalize_options(self):
        """finalize_options
        """

    def run(self):
        """run
        """
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


setup(
    # use_scm_version={"fallback_version": "noversion"},
    version=about["__version__"],
    cmdclass={
        "dependencies": ListDependenciesCommand,
        "pyinstaller": PyInstallerCommand,
    },
)
