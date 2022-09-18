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
   
   root privileges required!

From pypi::

   pip3 install gotcha

From source::

   git clone https://github.com/caputomarcos/gotcha.git
   cd gotcha
   python setup.py install


Community Distributions
-----------------------

Feel free! All contributions are welcome.

