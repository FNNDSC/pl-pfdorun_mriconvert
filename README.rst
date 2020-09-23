pl-pfdorun_mriconvert
================================

.. image:: https://badge.fury.io/py/pfdorun_mriconvert.svg
    :target: https://badge.fury.io/py/pfdorun_mriconvert

.. image:: https://travis-ci.org/FNNDSC/pfdorun_mriconvert.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/pfdorun_mriconvert

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-pfdorun_mriconvert

.. contents:: Table of Contents


Abstract
--------

An app to use the mri_convert functionality of FreeSurfer with pfdo_run: a Python utility which traverses a given tree structure, runs a command from the user and replcates the strcture in a given outputDir.


Synopsis
--------

.. code::

    python pfdorun_mriconvert.py                                           \
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


Description
-----------

``pfdorun_mriconvert.py`` is a ChRIS-based application that 
recursively walks down a directory tree and runs a CLI program
from mri_convert (a FreeSurfer program to convert mri images from one format to another)
Results of each operation are saved in an output tree
that preserves the input directory structure.

``pl-pfdorun_mriconvert`` runs mri_convert's user specified CLI at each path/file location
in an input directory, storing results (and logs) at a corresponding 
dir location rooted in the output directory.

Arguments
---------

.. code::

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

Run
---

Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

Now, prefix all calls with 

.. code:: bash

    docker run --rm -v $(pwd)/out:/outgoing                             \
            fnndsc/pl-pfdorun_mriconvert pfdorun_mriconvert.py                        \

Thus, getting inline help is:

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-pfdorun_mriconvert pfdorun_mriconvert.py                        \
            --man                                                       \
            /incoming /outgoing

Examples
--------





