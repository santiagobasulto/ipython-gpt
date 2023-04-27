Contribute
==========

Thank you for your help improving **ipython-gpt**!

**ipython-gpt** uses `nox <https://nox.thea.codes/en/stable/>`__ to automate several development-related tasks.
Currently, the project uses four automation processes (called sessions) in ``noxfile.py``:

-   ``mypy``: to perform a mypy check on the lib;
-   ``test``: to run the test with pytest;
-   ``docs``: to build the documentation in the ``build`` folder;
-   ``lint``: to run the pre-commits in an isolated environment

Every nox session is run in its own virtual environment, and the dependencies are installed automatically.

To run a specific nox automation process, use the following command:

.. code-block:: console

   nox -s <session name>

For example: ``nox -s test`` or ``nox -s docs``.

Workflow for contributing changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We follow a typical GitHub workflow of:

-   Create a personal fork of this repo
-   Create a branch
-   Open a pull request
-   Fix findings of various linters and checks
-   Work through code review

See the following sections for more details.

Clone the repository
^^^^^^^^^^^^^^^^^^^^

First off, you'll need your own copy of **ipython-gpt** codebase. You can clone it for local development like so:

Fork the repository so you have your own copy on GitHub. See the `GitHub forking guide for more information <https://docs.github.com/en/get-started/quickstart/fork-a-repo>`__.

Then, clone the repository locally so that you have a local copy to work on:

.. code-block:: console

   git clone https://github.com/<YOUR USERNAME>/ipython-gpt
   cd ipython-gpt

Then install the development version of the extension:

.. code-block:: console

   pip install -e

This will install the **ipython-gpt** library, together with two additional tools:
-   `pre-commit <https://pre-commit.com>`__ for automatically enforcing code standards and quality checks before commits.
-   `nox <https://nox.thea.codes/en/stable/>`__, for automating common development tasks.

Lastly, activate the pre-commit hooks by running:

.. code-block:: console

    pre-commit install

This will install the necessary dependencies to run pre-commit every time you make a commit with Git.

Contribute to the codebase
^^^^^^^^^^^^^^^^^^^^^^^^^^

Any larger updates to the codebase should include tests and documentation. The tests are located in the ``tests`` folder, and the documentation is located in the ``docs`` folder.

To run the tests locally, use the following command:

.. code-block:: console

    nox -s test

See :ref:`below <contributing-docs>` for more information on how to update the documentation.

.. _contributing-docs:

Contribute to the docs
^^^^^^^^^^^^^^^^^^^^^^

The documentation is built using `Sphinx <https://www.sphinx-doc.org/en/master/>`__ and deployed to `Read the Docs <https://readthedocs.org/>`__.

To build the documentation locally, use the following command:

.. code-block:: console

    nox -s docs

For each pull request, the documentation is built and deployed to make it easier to review the changes in the PR. To access the docs build from a PR, click on the "Read the Docs" preview in the CI/CD jobs.

Realease new version
^^^^^^^^^^^^^^^^^^^^

To release a new version, start by pushing a new bump from the local directory:

.. code-block::

    cz bump

The commitizen-tool will detect the sementic version name based on the existing commits messages.

Then push to Github. In Github design a new release using the same tag name nad the ``release.yaml`` job will send it to pipy.
