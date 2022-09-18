#!/usr/local/bin/python3
"""
_summary_
"""

from .__main__ import Gotcha, eeprint, KEYBOARD_INTERRUPT_MSG


def main() -> None:
    """_summary_
    """
    gotcha = Gotcha()
    try:
        gotcha.main()
    except IndexError:
        gotcha.usage(err='Argument value missing.')
    except KeyboardInterrupt:
        gotcha.working = False
        eeprint(KEYBOARD_INTERRUPT_MSG)


if __name__ == "__main__":
    main()
