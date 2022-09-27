"""args
"""
import argparse
import textwrap

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=textwrap.dedent('''\
    ██████╗  ██████╗ ████████╗ ██████╗██╗  ██╗ █████╗ ██╗██╗██╗
   ██╔════╝ ██╔═══██╗╚══██╔══╝██╔════╝██║  ██║██╔══██╗██║██║██║
   ██║  ███╗██║   ██║   ██║   ██║     ███████║███████║██║██║██║
   ██║   ██║██║   ██║   ██║   ██║     ██╔══██║██╔══██║╚═╝╚═╝╚═╝
   ╚██████╔╝╚██████╔╝   ██║   ╚██████╗██║  ██║██║  ██║██╗██╗██╗
    ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝╚═╝
   
.:·                      SSH-TTY control                       ·:.
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
parser.add_argument(
    "--replay",
    metavar="FILE",
    nargs="?",
    type=str,
    help="Play previously recorded session")

args = parser.parse_args()
