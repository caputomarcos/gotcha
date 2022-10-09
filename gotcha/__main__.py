"""args
"""
import os
import sys
import argparse
import textwrap

from shutil import which
from gotcha.gotcha_tty import GotchaTTY, GotchaArgs

parser = argparse.ArgumentParser(
    prog='gotcha',
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

# List available SSH Sessions
command_group.add_argument(
    "-s", "--session-files",
    const=1,
    nargs="?",
    type=int,
    choices=range(1, 4),
    help="List Session Files")

# Point GOTCHA to specific TTY
command_group.add_argument(
    "-t", "--tty",
    metavar="tty",
    nargs="?",
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
    metavar="session",
    nargs="?",
    type=str,
    help="Play previously recorded session")

# root privileges
if os.geteuid() != 0:
    parser.print_help()
    print("\n\n\t*** root privileges required for this software. ***\n")
    sys.exit(1)

# Check if we are running in a TTY
if not sys.stdout.isatty():
    parser.print_help()
    print("\n\n\t*** Sorry, your shell is not a TTY shell. ***\n\n\t\tTry to spawn PTY with python\n")
    sys.exit(1)

# strace is required
if not which("strace"):
    parser.print_help()
    print("\n\n\t*** linux syscall tracer is required. ***\n\n\t\tSee: https://strace.io\n")
    sys.exit(1)

if __name__ == "__main__":
    try:
        # GotchaArgs & GotchaTTYgotcha_args
        gotcha_args = GotchaArgs(**vars(parser.parse_args()))
        gotcha = GotchaTTY()

        # print(gotcha, gotcha_args)
        # import time
        # time.sleep(5)

        if gotcha_args.list:
            gotcha.list()
        elif gotcha_args.tty:
            gotcha.attach(gotcha_args.tty)
        elif gotcha_args.auto:
            gotcha.attach("auto")
        elif gotcha_args.session_files:
            gotcha.session_list(gotcha_args.session_files)
        elif gotcha_args.replay:
            gotcha.replay(gotcha_args.replay)
        else:
            parser.print_usage()
    except Exception:  # pylint: disable=broad-except
        sys.exit(1)
