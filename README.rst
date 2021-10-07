pl-pull_scp
================================

.. image:: https://img.shields.io/docker/v/fnndsc/pl-pull_scp?sort=semver
    :target: https://hub.docker.com/r/fnndsc/pl-pull_scp

.. image:: https://img.shields.io/github/license/fnndsc/pl-pull_scp
    :target: https://github.com/FNNDSC/pl-pull_scp/blob/master/LICENSE

.. image:: https://github.com/FNNDSC/pl-pull_scp/workflows/ci/badge.svg
    :target: https://github.com/FNNDSC/pl-pull_scp/actions


.. contents:: Table of Contents


Abstract
--------

This plugin application is used to recursively copy data from a remote host into an analysis root node.


Description
-----------


``pull_scp`` is a *ChRIS fs-type* application that produces data for a tree by copying data off a remote host using ``scp``. Of course this assumes that the user executing this plugin has the correct login credentials to access the resource.

Other than login credentials, this plugin also needs a ``filepath`` in the remote user space. All files and directories rooted in this file ``filepath`` are copied into this plugin's ``outputdir``.


Usage
-----

.. code::

    docker run --rm fnndsc/pl-pull_scp pull_scp             \
        [-h|--help]                                         \
        [--json] [--man] [--meta]                           \
        [--savejson <DIR>]                                  \
        [-v|--verbosity <level>]                            \
        [--version]                                         \
        --username <username>                               \
        --password <password>                               \
        --host <hostname>                                   \
        --filepath <filepath>                               \
        <outputDir>


Arguments
~~~~~~~~~

.. code::

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


Getting inline help is:

.. code:: bash

    docker run --rm fnndsc/pl-pull_scp pull_scp --man

Run
~~~

You need to specify input and output directories using the `-v` flag to `docker run`.


.. code:: bash

    docker run --rm -u $(id -u)                             \
        -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
        fnndsc/pl-pull_scp pull_scp                         \
        --username johnnyapple                              \
        --password 'mysecret'                               \
        --host computer.org                                 \
        --filepath /home/johnnyapple/data                   \
        /outgoing


Development
-----------

Build the Docker container:

.. code:: bash

    docker build -t local/pl-pull_scp .

Run unit tests:

.. code:: bash

    docker run --rm local/pl-pull_scp nosetests

Examples
--------

Put some examples here!


.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co
