pl-pfdorun_mriconvert 0.2
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
        [--fileFilter <filter1,filter2,...>]        \\
        [--dirFilter <filter1,filter2,...>]         \\
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

    [--fileFilter <someFilter1,someFilter2,...>]
    An optional comma-delimated string to filter out files of interest
    from the <inputDir> tree. Each token in the expression is applied in
    turn over the space of files in a directory location, and only files
    that contain this token string in their filename are preserved.

    [--dirFilter <someFilter1,someFilter2,...>]
    Similar to the `fileFilter` but applied over the space of leaf node
    in directory paths. A directory must contain at least one file
    to be considered.

    If a directory leaf node contains a string that corresponds to any of
    the filter tokens, a special "hit" is recorded in the file hit list,
    "%d-<leafnode>". For example, a directory of

                /some/dir/in/the/inputspace/here1234

    with a `dirFilter` of `1234` will create a "special" hit entry of
    "%d-here1234" to tag this directory for processing.
    
    In addition, if a directory is filtered through, all the files in
    that directory will be added to the filtered file list. If no files
    are to be added, passing an explicit file filter with an "empty"
    single string argument, i.e. `--fileFilter " "`, is advised.
    
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

First, let's create a directory, say ``devel`` wherever you feel like it. We will place some test data in this directory to process with this plugin.

.. code:: bash

    cd ~/
    mkdir devel
    cd devel
    export DEVEL=$(pwd)

Now, we need to fetch sample DICOM data.


Pull DICOM
^^^^^^^^^^

The input should be a DICOM file usually with extension .dcm

We provide a sample directory of .dcm images here. (https://github.com/FNNDSC/SAG-anon.git)

-   Clone this repository (SAG-anon) to your local computer within the ${DEVEL} directory.

.. code:: bash

    git clone https://github.com/FNNDSC/SAG-anon.git

Make sure the ``SAG-anon`` directory is placed in the devel directory.


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

- Make sure your current working directory is ``devel``. At this juncture it should contain `SAG-anon`.

- Create an output directory named ``results`` in ``devel``.

.. code:: bash

    mkdir results && chmod 777 results

- Pull the ``fnndsc/pl-pfdorun_mriconvert`` image using the following command.

.. code:: bash

    docker pull fnndsc/pl-pfdorun_mriconvert

Examples
--------

.. code:: bash

    docker run --rm -v ${DEVEL}/SAG-anon/:/incoming 
            -v ${DEVEL}/results:/outgoing                                   \
            fnndsc/pl-pfdorun_mriconvert pfdorun_mriconvert.py               \
            --exec "mri_convert %inputWorkingFile 
                %outputWorkingDir/%_rmext_inputWorkingFile.nii"              \
            --fileFilter dcm                                           \
            --analyzeFileIndex f                                             \
            --printElapsedTime                                               \
            /incoming /outgoing







