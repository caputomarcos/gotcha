"""setup GOTCHA_TTY
"""
from configparser import ConfigParser
from typing import Any, List
from subprocess import check_call
from pkg_resources import parse_requirements
from setuptools import setup, Command


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
    use_scm_version={"fallback_version": "noversion"},
    cmdclass={
        "dependencies": ListDependenciesCommand,
        "pyinstaller": PyInstallerCommand,
    },
)
