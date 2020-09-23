#!/usr/bin/env python                                            
#
# pfdorun_mriconvert ds ChRIS plugin app
#
# (c) 2016-2019 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#


import os
import sys
import pudb
sys.path.append(os.path.dirname(__file__))

# import the Chris app superclass
from chrisapp.base import ChrisApp
from pfdo_run      import pfdo_run

Gstr_title = """

        __    _                                         _                               _   
       / _|  | |                                       (_)                             | |  
 _ __ | |_ __| | ___  _ __ _   _ _ __    _ __ ___  _ __ _  ___ ___  _ ____   _____ _ __| |_ 
| '_ \|  _/ _` |/ _ \| '__| | | | '_ \  | '_ ` _ \| '__| |/ __/ _ \| '_ \ \ / / _ \ '__| __|
| |_) | || (_| | (_) | |  | |_| | | | | | | | | | | |  | | (_| (_) | | | \ V /  __/ |  | |_ 
| .__/|_| \__,_|\___/|_|   \__,_|_| |_| |_| |_| |_|_|  |_|\___\___/|_| |_|\_/ \___|_|   \__|
| |                                 ______                                                  
|_|                                |______|                                                 

"""

class Pfdorun_mriconvert(ChrisApp):
    """
    An app to ....
    """
    AUTHORS                 = 'FNNDSC (dev@babyMRI.org)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'A ChRIS plugin app'
    CATEGORY                = ''
    TYPE                    = 'ds'
    DESCRIPTION             = 'An app to run the mri_convert program of freesurfer on an entire directory structure.'
    DOCUMENTATION           = 'http://wiki'
    VERSION                 = '0.1'
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

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

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """

        self.add_argument("-i", "--inputFile", help="input file", type=str,
                          dest='inputFile', optional=False, default="")

        self.add_argument("--exec", help="CLI command to execute", type=str,
                          dest='exec', optional=False, default="")

        self.add_argument("--analyzeFileIndex", help="file index per directory to analyze", type=str,
                          dest='analyzeFileIndex', optional=False, default="-1")

        self.add_argument("--filterExpression", help="string file filter", type=str,
                          dest='filter', optional=True, default="")

        self.add_argument('--printElapsedTime', dest='printElapsedTime', type=bool, action='store_true',
                          default=False, optional=True, help='print program run time')

        self.add_argument('--threads', dest='threads', type=str,
                          default="0", optional=True, help='number of threads for innermost loop processing')

        self.add_argument('--outputLeafDir', dest='outputLeafDir', type=str,
                          default="", optional=True, help='formatting spec for output leaf directory')

        self.add_argument('--test', dest='test', type=bool, action='store_true',
                          default=False, optional=True, help='test')

        self.add_argument('--noJobLogging', dest='noJobLogging', type=bool, action='store_true',
                          default=False, optional=True, help='Turn off per-job logging to file system')

        self.add_argument('--overwrite', dest='overwrite', type=bool, action='store_true',
                          default=False, optional=True, help='overwrite files if already existing')

        self.add_argument('--followLinks', dest='followLinks', type=bool, action='store_true',
                          default=False, optional=True, help='follow symbolic links')

        self.add_argument('-y', '--synopsis', dest='synopsis', type=bool, action='store_true',
                          default=False, optional=True, help='short synopsis')


    def show_man_page(self, ab_shortOnly=False):
        """
        Print the app's man page.
        """
        scriptName = os.path.basename(sys.argv[0])
        shortSynopsis = '''

        NAME

        pfdorun_mriconvert.py 

        SYNOPSIS

            python pfdorun_mriconvert.py                   \\
                --exec <CLIcmdToExec>                       \\
                [-i|--inputFile <inputFile>]                \\
                [--analyzeFileIndex <someIndex>]            \\
                [--threads <numThreads>]                    \\
                [--noJobLogging]                            \\
                [--test]                                    \\
                [-x|--man]                                  \\
                [-y|--synopsis]                             \\
                [--followLinks]                             \\
                [--json]                                    \\
                [-v <level>] [--verbosity <level>]          \\
                [--version]                                 \\
                <inputDir>                                  \\
                <outputDir> 

        ''' % scriptName

        description = '''
        DESCRIPTION

            ``pfdorun_mriconvert.py`` is a ChRIS-based application that 
            recursively walks down a directory tree and runs a CLI program
            from mri_convert (a FreeSurfer program to convert mri images from one format to another)
            Results of each operation are saved in an output tree
            that preserves the input directory structure.

            ``pl-pfdorun_mriconvert`` runs mri_convert's user specified CLI at each path/file location
            in an input directory, storing results (and logs) at a corresponding 
            dir location rooted in the output directory.

        ARGS

            --exec <CLIcmdToExec>
            The command line expression to apply at each directory node of the
            input tree. See the CLI SPECIFICATION section for more information.

            [-i|--inputFile <inputFile>]
            An optional <inputFile> specified relative to the <inputDir>. If
            specified, then do not perform a directory walk, but convert only
            this file.

            [-f|--filterExpression <someFilter>]
            An optional string to filter the files of interest from the
            <inputDir> tree.

            [--analyzeFileIndex <someIndex>]
            An optional string to control which file(s) in a specific directory
            to which the analysis is applied. The default is "-1" which implies
            *ALL* files in a given directory. Other valid <someIndex> are:

                'm':   only the "middle" file in the returned file list
                "f":   only the first file in the returned file list
                "l":   only the last file in the returned file list
                "<N>": the file at index N in the file list. If this index
                    is out of bounds, no analysis is performed.

                "-1" means all files.

            [--outputLeafDir <outputLeafDirFormat>]
            If specified, will apply the <outputLeafDirFormat> to the output
            directories containing data. This is useful to blanket describe
            final output directories with some descriptive text, such as
            'anon' or 'preview'.

            This is a formatting spec, so

                --outputLeafDir 'preview-%%s'

            where %%s is the original leaf directory node, will prefix each
            final directory containing output with the text 'preview-' which
            can be useful in describing some features of the output set.

            [--threads <numThreads>]
            If specified, break the innermost analysis loop into <numThreads>
            threads.

            [--noJobLogging]
            If specified, then suppress the logging of per-job output. Usually
            each job that is run will have, in the output directory, three
            additional files:

                    %inputWorkingFile-returncode
                    %inputWorkingFile-stderr
                    %inputWorkingFile-stdout

            By specifying this option, the above files are not recorded.

            [-x|--man]
            Show full help.

            [-y|--synopsis]
            Show brief help.

            [--json]
            If specified, output a JSON dump of final return.

            [--followLinks]
            If specified, follow symbolic links.

            -v|--verbosity <level>
            Set the app verbosity level.

                0: No internal output;
                1: Run start / stop output notification;
                2: As with level '1' but with simpleProgress bar in 'pftree';
                3: As with level '2' but with list of input dirs/files in 'pftree';
                5: As with level '3' but with explicit file logging for
                        - read
                        - analyze
                        - write
            
            [--version]
            If specified, print version number and exit. 
            
            
            ''' % (scriptName)

        if ab_shortOnly:
            return shortSynopsis
        else:
            return shortSynopsis + description

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())

        # pudb.set_trace()

        options.inputDir = options.inputdir
        options.outputDir = options.outputdir

        pf_do_shell         = pfdo_run(vars(options))
        # pf_do_shell         = pfdo_run.object_factoryCreate(vars(options)).C_convert

        if options.man or options.synopsis:
            if options.man:
                str_help = self.show_man_page(False)
            else:
                str_help = self.show_man_page(True)
            print(str_help)
            sys.exit(1)
            
        # And now run it!
        # pudb.set_trace()
        d_pfdo_shell        = pf_do_shell.run(timerStart = True)
        
        # print(d_pfdo_shell)
        if options.printElapsedTime:
            pf_do_shell.dp.qprint(
                    "Elapsed time = %f seconds" %
                    d_pfdo_shell['runTime']
            )

        sys.exit(0)

# ENTRYPOINT
if __name__ == "__main__":
    chris_app = Pfdorun_mriconvert()
    chris_app.launch()
