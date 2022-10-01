"""args
"""
import os
import sys
import argparse
import textwrap
from dataclasses import dataclass
from shutil import which


@dataclass
class GotchaArgs:
    """
        GotchaArgs
    """
    verbose: bool = False
    quiet: bool = False
    list: bool = False
    tty: str = ''
    auto: bool = False
    replay: str = ''
    speed: int = 1


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=textwrap.dedent('''\
·:.                                                            .:·

    ██████╗  ██████╗ ████████╗ ██████╗██╗  ██╗ █████╗ ██╗██╗██╗
   ██╔════╝ ██╔═══██╗╚══██╔══╝██╔════╝██║  ██║██╔══██╗██║██║██║
   ██║  ███╗██║   ██║   ██║   ██║     ███████║███████║██║██║██║
   ██║   ██║██║   ██║   ██║   ██║     ██╔══██║██╔══██║╚═╝╚═╝╚═╝
   ╚██████╔╝╚██████╔╝   ██║   ╚██████╗██║  ██║██║  ██║██╗██╗██╗
    ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝╚═╝

.:·                                                             ·:.
'''))

# Displays group options
display_group = parser.add_mutually_exclusive_group()

# Turn on verbose output
display_group.add_argument(
    "-v", "--verbose",
    action="store_true",
    help="Turn on verbose output")

# Enable quiet mode
display_group.add_argument(
    "-q", "--quiet",
    action="store_true",
    help="Enable quiet mode")

# Command group options
command_group = parser.add_mutually_exclusive_group()

# List available SSH Sessions
command_group.add_argument(
    "-l", "--list",
    action="store_true",
    help="List available SSH Sessions")

# Point GOTCHA to specific TTY
command_group.add_argument(
    "-t", "--tty",
    type=str,
    help="Point GOTCHA to specific TTY")

# Lazy mode, auto-attach to first found session
command_group.add_argument(
    "-a", "--auto",
    action="store_true",
    help="Lazy mode, auto-attach to first found session")

# Play previously recorded session
command_group.add_argument(
    "--replay",
    metavar="FILE",
    nargs="?",
    type=str,
    help="Play previously recorded session")

# GotchaArgs
gotcha_args = GotchaArgs(**vars(parser.parse_args()))
# print(gotcha_args)


# root privileges
if os.geteuid() != 0:
    parser.print_help()
    print("\n\n\t*** root privileges required for this software. ***\n")
    sys.exit(1)

# strace is required
if not which("strace"):
    parser.print_help()
    print("\n\n\t*** linux syscall tracer is required. ***\n\n\t\tSee: https://strace.io\n")
    sys.exit(1)
