GOTCHA - The SSH-TTY control Interface
======================================
::

      $ ./gotcha 
      usage: gotcha [-h] [-v | -q] [-l | -s [{1,2,3}] | -t [tty] | -a | --replay [session]]

      ·:.                                                             .:·

          ██████╗  ██████╗ ████████╗ ██████╗██╗  ██╗ █████╗ ██╗██╗██╗
         ██╔════╝ ██╔═══██╗╚══██╔══╝██╔════╝██║  ██║██╔══██╗██║██║██║
         ██║  ███╗██║   ██║   ██║   ██║     ███████║███████║██║██║██║
         ██║   ██║██║   ██║   ██║   ██║     ██╔══██║██╔══██║╚═╝╚═╝╚═╝
         ╚██████╔╝╚██████╔╝   ██║   ╚██████╗██║  ██║██║  ██║██╗██╗██╗
         ╚═════╝  ╚═════╝    ╚═╝    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝╚═╝

      .:·                                                             ·:.

      options:
      -h, --help            Show this help message and exit
      -v, --verbose         Turn on verbose output
      -q, --quiet           Enable quiet mode
      -l, --list            List available SSH Sessions
      -s [{1,2,3}], --session-files [{1,2,3}]
                            List Session Files
      -t [tty], --tty [tty]
                            Point GOTCHA to specific TTY
      -a, --auto            Lazy mode, auto-attach to first found session
      --replay [session]    Play previously recorded session


         *** root privileges required for this software. ***

::

      $ sudo ./gotcha 
      usage: gotcha [-h] [-v | -q] [-l | -s [{1,2,3}] | -t [tty] | -a | --replay [session]]

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

      -v, --verbose         Turn on verbose output
      -q, --quiet           Enable quiet mode