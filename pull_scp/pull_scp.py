#
# pull_scp FS ChRIS plugin app
#
# (c) 2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

from paramiko.client    import SSHClient
from chrisapp.base      import ChrisApp

from .                  import commandList_execOnRemote
from .config            import LOCAL_FILE_DIRECTORY, SSH_CONFIG_VALUES
from .log               import LOGGER

import  pudb

Gstr_title = r"""
             _ _
            | | |
 _ __  _   _| | |  ___  ___ _ __
| '_ \| | | | | | / __|/ __| '_ \
| |_) | |_| | | | \__ \ (__| |_) |
| .__/ \__,_|_|_| |___/\___| .__/
| |           ______       | |
|_|          |______|      |_|
"""

Gstr_synopsis = """

    NAME

        pull_scp

    SYNOPSIS

        docker run --rm fnndsc/pl-pull-scp pull_scp                     \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            --username <username>                                       \\
            --password <password>                                       \\
            --host <hostname>                                           \\
            --filepath <filepath>                                       \\
            <outputDir>

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                             \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
                fnndsc/pl-pull-scp pull_scp                         \
                --username johnnyapple                              \
                --password 'mysecret'                               \
                --host computer.org                                 \
                --filepath /home/johnnyapple/data                   \
                /outgoing

    DESCRIPTION

        ``pull_scp`` is a *ChRIS fs-type* application that produces data for
        an analysis tree by copying data off a remote host using ``scp``. Of
        course this assumes that the user executing this plugin has the correct
        login credentials to access the resource.

        Other than login credentials, this plugin also needs a ``filepath`` in
        the remote user space. All files and directories rooted in this file
        ``filepath`` are copied into this plugin's ``outputdir``.

    ARGS

        --filepath <filepath>
        The path in the <hostname>'s filesystem to pull.

        [--username <username>]
        The username in the remote host.

        [--password <password>]
        The <username>'s password to connect to the remote host.

        [--host <hostname>]
        The hostname to access.

        [-h] [--help]
        If specified, show help message and exit.

        [--json]
        If specified, show json representation of app and exit.

        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.

        [--savejson <DIR>]
        If specified, save json representation file to DIR and exit.

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number and exit.
"""


class Pull_scp(ChrisApp):
    """
    This plugin application is used to recursively copy data from a remote host into an analysis root node.
    """
    PACKAGE                 = __package__
    TITLE                   = "A ChRIS plugin FS app that scp's data from a remote host"
    CATEGORY                = 'utility'
    TYPE                    = 'fs'
    ICON                    = ''   # url of an icon image
    MIN_NUMBER_OF_WORKERS   = 1    # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS   = 1    # Override with the maximum number of workers as int
    MIN_CPU_LIMIT           = 1000 # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT        = 200  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT           = 0    # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT           = 0    # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def __init__(self, remoteclient):
        """constructor

        This is a custom constructor that is initiated with a RemoteClient
        object.

        Args:
            remoteclient ([type]): a remote client
        """
        super().__init__()
        self.client     = remoteclient

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument('--username',
            dest        = 'str_username',
            type        = str,
            optional    = True,
            default     = "",
            help        = 'The username in the remote computer.'
        )
        self.add_argument('--password',
            dest        = 'str_password',
            type        = str,
            optional    = True,
            default     = "",
            help        = "The <username>'s password in the remote computer."
        )
        self.add_argument('--host',
            dest        = 'str_hostname',
            type        = str,
            optional    = True,
            default     = "",
            help        = 'The name of the remote computer.'
        )
        self.add_argument('--filepath',
            dest        = 'str_filepath',
            type        = str,
            optional    = False,
            default     = "",
            help        = 'The location in the remote computer to pull.'
        )

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        str_remotedirs  : str   = 'find %s -type d' % options.str_filepath
        str_remotefiles : str   = 'find %s maxdepth 1 -type f' % options.str_filepath
        l_remotefiles   : list  = []
        l_remotedirs    : list  = []
        options.verbosity       = int(options.verbosity)
        self.client.localpath   = options.outputdir
        self.client.verbosity   = options.verbosity

        # Intro
        if options.verbosity:
            print(Gstr_title)
            print('Version: %s' % self.get_version())
        if options.verbosity >= 2:
            LOGGER.info('%s' % SSH_CONFIG_VALUES)
            LOGGER.info('exec: "%s"' % str_remotefiles)

        # First, get a list of remote directories...
        l_remotedirs = commandList_execOnRemote(
            self.client,
            [str_remotedirs]
        )

        # And for each remote dir, execute a 1-level file pull...
        l_remotefiles = commandList_execOnRemote(
            self.client,
            [str_remotefiles]
        )
        if len(l_remotefiles[0]['stdout']):
            self.client.bulk_pullObj(l_remotefiles[0]['stdout'])

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
