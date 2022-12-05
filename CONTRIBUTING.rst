Contribute
==========

After forking the projet, run the following command to start developing: 

.. code-block:: console

    $ git clone https://github.com/<github id>/<python_lib>.git
    $ cd <python_lib> 
    $ pip install -e .[dev, test, doc]
    
.. danger:: 

    :code:`pre-commits` are installed in edit mode. Every commit that does not respect the conventional commits framework will be refused. 
    you can read this `documentation <https://www.conventionalcommits.org/en/v1.0.0/>`__ to learn more about them and we highly recommend to use the :code:`commitizen` lib to create your commits: `<https://commitizen-tools.github.io/commitizen>`__.

Develop within the project
--------------------------

Since 2020-08-14, this repository follows these `development guidelines <https://nvie.com/posts/a-successful-git-branching-model/>`__.

.. tip::

    Please consider using the :code:`--no-ff` option when merging to keep the repository consistent with PR. 

In the project to adapt to :code:`JupyterLab` IntelSense, we decided to explicitly write the `return` statement for every function.

We need to provide the users with version informations. When a new function or class is created please use the `Deprecated <https://pypi.org/project/Deprecated/>`__ lib to specify that the feature is new in the documentation. 

.. code-block:: python

    from deprecated.sphinx import deprecated
    from deprecated.sphinx import versionadded
    from deprecated.sphinx import versionchanged


    @versionadded(version='1.0', reason="This function is new")
    def function_one():
        '''This is the function one'''


    @versionchanged(version='1.0', reason="This function is modified")
    def function_two():
        '''This is the function two'''


    @deprecated(version='1.0', reason="This function will be removed soon")
    def function_three():
        '''This is the function three'''
    
How to commit
-------------

In this repository we use the Conventional Commits specification.
The Conventional Commits specification is a lightweight convention on top of commit messages. It provides an easy set of rules for creating an explicit commit history; which makes it easier to write automated tools on top of. This convention dovetails with SemVer, by describing the features, fixes, and breaking changes made in commit messages.

You can learn more about Conventional Commits following this `link <https://www.conventionalcommits.org/en/v1.0.0/>`__

What can I push and where
-------------------------

Our branching system embed some rules to avoid crash of the production environment. If you want to contribute to this framework, here are some basic rules that we try our best to follow :

-   the modification you offer is solving a critical bug in prod : **PR in a patch branch**
-   the modification you propose solve the following issues : test, documentation, typo, quality, refactoring, translation **PR in main**
-   the modification you propose is a new feature : open an issue to discuss with the maintainers and then **PR from a named branch**

the maintainers will try their best to use PR for new features, to help the community follow the development, for other modification they will simply push to the appropriate branch

Create a new release
--------------------

.. danger:: 

    for maintainers only 
    
 .. warning::
 
     You need to use the :code:`commitizen` lib to create your release: `<https://commitizen-tools.github.io/commitizen>`__
    
In the files change the version number by runnning commitizen `bump`: 

.. code-block:: console

    cz bump

It should modify for you the version number in :code:`sepal_ui/__init__.py`, :code:`setup.py`, and :code:`.cz.yaml` according to sementic versionning thanks to the conventional commit that we use in the lib. 

It will also update the :code:`CHANGELOG.md` file with the latest commits, sorted by categories.

Then you can now create a new tag with your new version number. use the same convention as the one found in :code:`.cz.yaml`: :code:`v$minor.$major.$patch$prerelease`. 
    
The CI should take everything in control from here and execute the :code:`Upload Python Package` GitHub Action that is publishing the new version on `PyPi <#>`_.
