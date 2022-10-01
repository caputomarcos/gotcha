GOTCHA - The SSH-TTY control Interface
======================================
::

         ██████╗  ██████╗ ████████╗ ██████╗██╗  ██╗ █████╗ ██╗██╗██╗
        ██╔════╝ ██╔═══██╗╚══██╔══╝██╔════╝██║  ██║██╔══██╗██║██║██║
        ██║  ███╗██║   ██║   ██║   ██║     ███████║███████║██║██║██║
        ██║   ██║██║   ██║   ██║   ██║     ██╔══██║██╔══██║╚═╝╚═╝╚═╝
        ╚██████╔╝╚██████╔╝   ██║   ╚██████╗██║  ██║██║  ██║██╗██╗██╗
        ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝╚═╝

        SSH-TTY control
        


        Usage: GOTCHA [OPTIONS]

        Args: --auto                # Lazy mode, auto-attach to first found session.
              --list                # List available SSH Sessions.
              --tty /dev/pts/XX     # Point GOTCHA to specific TTY.
              --replay <file>       # Play previously recorded session.
              --speed 4             # Replay speed multiplier (Default: 4).

                     ----- root privileges required! -----

Installation
------------
   
   Linux syscall tracer `(strace) <https://strace.io/>`_ and root privileges required!

From pypi::

   pip3 install ttyGotcha

From source::

   git clone https://github.com/caputomarcos/gotcha.git
   cd gotcha
   python setup.py install


Community Distributions
-----------------------

Feel free! All contributions are welcome.


TO DO
-----
 
   * CHANGE `__main__.main` AND `gotcha.main` TO `gotcha/args.py` *argparse* ::

         usage: args.py [-h] [-v | -q] [-l | -t TTY | -a | --replay [FILE]]

         ·:.                                                            .:·

            ██████╗  ██████╗ ████████╗ ██████╗██╗  ██╗ █████╗ ██╗██╗██╗
            ██╔════╝ ██╔═══██╗╚══██╔══╝██╔════╝██║  ██║██╔══██╗██║██║██║
            ██║  ███╗██║   ██║   ██║   ██║     ███████║███████║██║██║██║
            ██║   ██║██║   ██║   ██║   ██║     ██╔══██║██╔══██║╚═╝╚═╝╚═╝
            ╚██████╔╝╚██████╔╝   ██║   ╚██████╗██║  ██║██║  ██║██╗██╗██╗
            ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝╚═╝

         .:·                       SSH-TTY control                       ·:.
                                 -+---------------+-

         optional arguments:
         -h, --help         show this help message and exit
         -v, --verbose      Turn on verbose output
         -q, --quiet        Enable quiet mode
         -l, --list         List available SSH Sessions
         -t TTY, --tty TTY  Point GOTCHA to specific TTY
         -a, --auto         Lazy mode, auto-attach to first found session
         --replay [FILE]    Play previously recorded session

