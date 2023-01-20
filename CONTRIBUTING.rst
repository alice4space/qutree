Contribute
==========

After forking the projet, run the following command to start developing: 

.. code-block:: console

    git clone https://github.com/alice4space/qutree.git
    cd qutree
    pip install -e .[dev]

Nox 
---

:code:`nox` can be used to automatically create isolated local development environments with all of the correct packages installed to work on the lib. The rest of this guide focuses on using nox to start with a basic environment.

You can call :code:`nox` from the command line in order to perform common actions that are needed in building the lib. :code:`nox` operates with isolated environments, so each action has its own packages installed in a local directory (:code:`.nox`). For common development actions, you’ll simply need to use :code:`nox` and won’t need to set up any other packages.
    
Pre-commit hooks 
----------------

:code:`pre-commit` allows us to run several checks on the codebase every time a new Git commit is made. This ensures standards and basic quality control for our code.

Install the pre-commit in the repository:

.. code-block:: console

    pre-commit install -t pre-commit -t commit-msg

Linting operations will be run automatically for every downstream commit.

.. note:: 

    to run liniting operation without commiting your change execute the following: 

    .. code-block:: console

        nox -s lint

Mypy
----

Mypy is a static type checker for Python.

Type checkers help ensure that you're using variables and functions in your code correctly. With mypy, add type hints (PEP 484) to your Python programs, and mypy will warn you when you use those types incorrectly.

Python is a dynamic language, so usually you'll only see errors in your code when you attempt to run it. Mypy is a static checker, so it finds bugs in your programs without even running them!

to run the MyPy checks run: 

.. code-block:: console

    nox -s mypy

Documentation
-------------

We build our documentation within the :code:`Sphinx` framework. execute the associated nox to build the file and produce the associated HTML:

.. code-block:: console

    nox -s docs

The index file will be in :code:`./docs/build/html/index.html`.

Release
-------

You need to use the :code:`commitizen` lib to create your release: `<https://commitizen-tools.github.io/commitizen>`__.
    
In the files change the version number by runnning commitizen `bump`: 

.. code-block:: console

    cz bump

It should modify for you the version number in :code:`qutree/__init__.py` and :code:`pyproject.toml` according to sementic versionning thanks to the conventional commit that we use in the lib. 

It will also update the :code:`CHANGELOG.md` file with the latest commits, sorted by categories.

You can now create a new tag with your new version number. use the same convention as the one found in :code:`pyproject.toml`: :code:`v$minor.$major.$patch$prerelease`. 
    
The CI should take everything in control from here and execute the :code:`Upload Python Package` GitHub Action that is publishing the new version on `PyPi <https://pypi.org/project/qutree>`_.
