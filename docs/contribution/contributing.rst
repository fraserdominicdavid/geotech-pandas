==================
Contribution Guide
==================
(The contents of this guide are largely inspired by `Pandas
<https://pandas.pydata.org/docs/development/contributing.html>`__ and `GeoPandas
<https://geopandas.org/en/latest/community/contributing.html>`__)

Overview
--------
Contributions to geotech-pandas are very welcome. They are likely to be accepted more quickly if
they follow these guidelines.

At this stage of geotech-pandas development, the priorities are to define a simple, usable, and
stable API and to have clean, maintainable, readable code. Performance matters, but not at the
expense of those goals.

In general, geotech-pandas follows the conventions of the pandas project where applicable.

In particular, when submitting a pull request (PR):

- All existing tests should pass. Please make sure that the test suite passes, both locally and on
  `GitHub Actions (GHA) <https://GitHub.com/fraserdominicdavid/geotech-pandas/actions>`__. Status on
  GHA will be visible on a PR. GHA are automatically enabled on your own fork as well. To trigger a
  check, make a PR to your own fork.

- New functionality should include tests. Please write reasonable tests for your code and make sure
  that they pass on your PR.

- Classes, methods, functions, etc. should have docstrings. The first line of a docstring should be
  a standalone summary. Parameters and return values should be documented explicitly.

- Follow `PEP8 <http://www.python.org/dev/peps/pep-0008/>`__ when possible. We use
  `Ruff <https://beta.ruff.rs/docs/>`__ to ensure a consistent code format throughout the project.

- Follow the `Conventional Commits <https://www.conventionalcommits.org/>`__ standard when writing
  commits. We use `Commitizen <https://GitHub.com/commitizen-tools/commitizen>`__ to ensure
  consistent commit messages, which are then used in automated semantic versioning and changelog
  generation.

- The geotech-pandas project supports Python 3.10+ only, usually in-sync with the supported versions
  of Pandas.

Bug reports and feature requests
--------------------------------
Bug reports and enhancement requests are an important part of making geotech-pandas more stable.
These are curated though GitHub issues. When reporting and issue or request, please select the
`appropriate category <https://GitHub.com/fraserdominicdavid/geotech-pandas/issues/new/choose>`__
and fill out the issue form fully to ensure others and the core development team can fully
understand the scope of the issue.

The issue will then show up in GitHub issues and be open to comments/ideas from others.

Finding an issue to contribute to
---------------------------------
If you are brand new to geotech-pandas or open-source development, we recommend searching the
`GitHub "issues" tab <https://GitHub.com/fraserdominicdavid/geotech-pandas/issues>`__ to find issues
that interest you. Unassigned issues labeled `documentation <https://GitHub.com/fraserdominicdavid/geotech-pandas/issues?q=is%3Aopen+sort%3Aupdated-desc+label%3Adocumentation+no%3Aassignee>`__
and `good first issue <https://GitHub.com/fraserdominicdavid/geotech-pandas/issues?q=is%3Aopen+sort%3Aupdated-desc+label%3A%22good+first+issue%22+no%3Aassignee>`__
are typically good for newer contributors.

Once you've found an interesting issue, it's a good idea to assign the issue to yourself, so nobody
else duplicates the work on it.

If for whatever reason you are not able to continue working with the issue, please unassign it, so
other people know it's available again. You can check the list of assigned issues, since people may
not be working in them anymore. If you want to work on one that is assigned, feel free to kindly ask
the current assignee if you can take it. Please allow at least a week of inactivity before
considering work in the issue discontinued.

General contribution workflow
-----------------------------
Once you have chosen an issue to work on, follow the basic steps below to contribute to
geotech-pandas:

#. :ref:`fork-the-git-repository`
#. :ref:`set-up-development-environment`
#. :ref:`create-a-feature-branch`
#. :ref:`make-changes-to-code`
#. :ref:`add-reasonable-tests`
#. :ref:`lint-and-format-code`
#. :ref:`update-the-documentation`
#. :ref:`commit-changes`
#. :ref:`push-your-changes`
#. :ref:`submit-a-pull-request`
#. :ref:`update-your-pull-request`
#. :ref:`update-your-development-environment`

Each of these steps is detailed in the following sections after reading through the
:ref:`recommended-prerequisites`.

.. _recommended-prerequisites:

Recommended prerequisites
^^^^^^^^^^^^^^^^^^^^^^^^^
  
#. `Generate an SSH key <https://docs.GitHub.com/en/authentication/connecting-to-GitHub-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key>`__
   and `add the SSH key to your GitHub account <https://docs.GitHub.com/en/authentication/connecting-to-GitHub-with-ssh/adding-a-new-ssh-key-to-your-GitHub-account>`__.
#. Configure SSH to automatically load your SSH keys::

      cat << EOF >> ~/.ssh/config

      Host *
         AddKeysToAgent yes
         IgnoreUnknown UseKeychain
         UseKeychain yes
         ForwardAgent yes
      EOF

#. `Install Docker Desktop <https://www.docker.com/get-started>`__.
#. `Install VS Code <https://code.visualstudio.com/>`__ and `VS Code's Dev Containers extension 
   <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers>`__.
   Alternatively, install `PyCharm <https://www.jetbrains.com/pycharm/download/>`__.
#. *Optional:* install a `Nerd Font <https://www.nerdfonts.com/font-downloads>`__ such as
   `FiraCode Nerd Font <https://GitHub.com/ryanoasis/nerd-fonts/tree/master/patched-fonts/FiraCode>`__
   and `configure VS Code <https://GitHub.com/tonsky/FiraCode/wiki/VS-Code-Instructions>`__ or
   `configure PyCharm <https://GitHub.com/tonsky/FiraCode/wiki/Intellij-products-instructions>`__ to
   use it.

.. _fork-the-git-repository:

Fork the git repository
^^^^^^^^^^^^^^^^^^^^^^^
You will need your own fork to work on the code. Go to the `geotech-pandas project page
<https://GitHub.com/fraserdominicdavid/geotech-pandas>`__ and hit the ``Fork`` button.

.. _clone-your-fork:

Clone your fork
~~~~~~~~~~~~~~~
To clone your fork to your local machine::

   git clone git@GitHub.com:your-user-name/geotech-pandas.git geotech-pandas-yourname
   cd geotechpandas-yourname
   git remote add upstream git://GitHub.com/fraserdominicdavid/geotech-pandas.git
   git fetch upstream

This creates the directory ``geotech-pandas-yourname`` and connects your repository to the upstream
(main project) geotech-pandas repository.

.. _set-up-development-environment:

Set up a development environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The following development environments are supported:

#. ⭐️ *GitHub Codespaces*: click on
   `Open in GitHub Codespaces <https://github.com/codespaces/new/fraserdominicdavid/geotech-pandas>`__
   to start developing in your browser.

#. ⭐️ *VS Code Dev Container (with container volume)*: click on
   `Open in Dev Containers <https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/fraserdominicdavid/geotech-pandas>`__
   to clone this repository in a container volume and create a Dev Container with VS Code.

#. ⭐️ *uv*: clone this repository and run the following from root of the repository::

      # Create and install a virtual environment
      uv sync --python 3.10 --all-extras

      # Activate the virtual environment
      source .venv/bin/activate

      # Install the pre-commit hooks
      pre-commit install --install-hooks

#. *VS Code Dev Container*: :ref:`clone-your-fork`, open it with VS Code, and run :kbd:`Ctrl/⌘` +
   :kbd:`⇧` + :kbd:`P` → *Dev Containers: Reopen in Container*.

#. *PyCharm Dev Container*: :ref:`clone-your-fork`, open it with PyCharm, `create a Dev
   Container with Mount Sources <https://www.jetbrains.com/help/pycharm/start-dev-container-inside-ide.html>`__,
   and `configure an existing interpreter <https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html#widget>`__
   at ``/opt/venv/bin/python``.

.. _create-a-feature-branch:

Create a feature branch
^^^^^^^^^^^^^^^^^^^^^^^
Your local main branch should always reflect the current state of the geotech-pandas repository.
First ensure that it's up-to-date with the main repository::

   git checkout main
   git pull upstream main --ff-only

Then, create a feature branch for making your changes. For example::

    git checkout -b shiny-new-feature

This changes your working branch from the ``main`` to the ``shiny-new-feature`` branch. Keep any
changes in this branch specific to one bug or feature so it is clear what the branch brings to
geotech-pandas. You can have many feature branches and switch in between them using the
``git checkout`` command.

To update this branch, you need to retrieve the changes from the main branch::

    git fetch upstream
    git rebase upstream/main

This will replay your commits on top of the latest geotech-pandas git main. If this leads to merge
conflicts, you must resolve these before submitting your PR. If you have uncommitted changes, you
will need to ``git stash`` them prior to updating. This will effectively store your changes and they
can be reapplied after updating.

.. _make-changes-to-code:

Make changes to code
^^^^^^^^^^^^^^^^^^^^
The geotech-pandas project is serious about testing and strongly encourages contributors to embrace
`test-driven development (TDD) <http://en.wikipedia.org/wiki/Test-driven_development>`__. This
development process "relies on the repetition of a very short development cycle: first the developer
writes an, initially failing, automated test case that defines a desired improvement or new
function, then produces the minimum amount of code to pass that test." So, before actually writing
any code, you should write your tests. Often the test can be taken from the original GitHub issue.
However, it is always worth considering additional use cases and writing corresponding tests.

To see all the changes you've currently made, run::

   git status

.. _add-reasonable-tests:

Add reasonable tests
^^^^^^^^^^^^^^^^^^^^
Adding tests is one of the most common requests after code is pushed to geotech-pandas. Therefore,
it is worth getting in the habit of writing tests ahead of time so this is never an issue.

The `pytest testing system <http://doc.pytest.org/en/latest/>`__ and convenient extensions in the
``pandas._testing`` module are used in geotech-pandas.

All tests should go into the ``tests`` directory. This folder contains many current examples of
tests, and we suggest looking to these for inspiration.

The ``pandas._testing`` module has some special ``assert`` functions that make it easier to make
statements about whether :external:class:`~pandas.Series` or :external:class:`~pandas.DataFrame`
objects are equivalent. The easiest way to verify that your code is correct is to explicitly
construct the result you expect, then compare the actual result to the expected correct result,
using the appropriate ``assert`` functions from ``pandas._testing``.

The tests can then be run directly inside your Git clone by typing::

    poe test

.. _lint-and-format-code:

Lint and format code
^^^^^^^^^^^^^^^^^^^^
The PEP8 standard is followed in geotech-pandas with the help of Ruff to ensure a consistent code
format throughout the project.

Continuous Integration (CI) with GHA will run lint checking tools and report any stylistic
errors in your code. Therefore, it is helpful, before submitting code, to run the check yourself::

   poe lint

to auto-format your code. Additionally, the Dev Container supplied in this project applies these
tools as you edit files.

.. _update-the-documentation:

Update the documentation
^^^^^^^^^^^^^^^^^^^^^^^^
The geotech-pandas documentation resides in the ``docs`` folder of the repository. Changes to the
documentation are made by modifying the appropriate file in that folder. The documentation uses the
reStructuredText syntax rendered using `Sphinx <https://www.sphinx-doc.org/>`__. For more
information, see `reStructuredText Primer
<http://www.sphinx-doc.org/en/stable/rest.html#rst-primer>`__.

On the other hand, the docstrings follow the `Numpy Docstring Standard
<https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard>`__.

We highly encourage you to follow the `Google developer documentation style guide
<https://developers.google.com/style/highlights>`__ when updating or creating new documentation.

Once you have made your changes, you may try if they render correctly by building the docs using
sphinx. To do so, run::

    poe docs

The resulting html pages will be located in ``docs/_build/html``.

If you wish to render a "clean" build, run::

   poe docs -O "-E -a"

This ensures that sphinx will rebuild and save the output files completely.

A "cleaner" build can also be done by removing the ``_build`` and ``api-reference/api`` folders
first before building::

   rm -r docs/api-reference/api docs/_build
   poe docs

.. _commit-changes:

Commit changes
^^^^^^^^^^^^^^
After making the changes, tests, linting and formatting, you can now stage your changes using::

   git add path/to/files-to-be-added-or-changed.py

Running ``git status``, the output should be::

    On branch shiny-new-feature

         modified:   /relative/path/to/file-to-be-added-or-changed.py

Note that this project follows the Conventional Commits standard with the help of Commitizen. So, to
commit using Commitizen, run::

   cz commit

This command will guide you through the process of writing an appropriate commit message.

There are also `pre-commit <https://pre-commit.com/>`__ hooks set up to ensure that lint checks and
code tests are run before committing, but, again, it is always helpful to run these yourself first
before committing with::

   poe test

and::

   poe lint

.. _push-your-changes:

Push your changes
^^^^^^^^^^^^^^^^^
When you want your changes to appear publicly on your GitHub page, push your forked feature branch's
commits::

    git push origin shiny-new-feature

Here ``origin`` is the default name given to your remote repository on GitHub. You can see the
remote repositories::

    git remote -v

If you added the upstream repository as described above you will see something like::

    origin  git@GitHub.com:your-user-name/geotech-pandas.git (fetch)
    origin  git@GitHub.com:your-user-name/geotech-pandas.git (push)
    upstream        git://GitHub.com/fraserdominicdavid/geotech-pandas.git (fetch)
    upstream        git://GitHub.com/fraserdominicdavid/geotech-pandas.git (push)

Now your code is on GitHub, but it is not yet a part of the geotech-pandas project. For that to
happen, a PR needs to be submitted on GitHub.

.. _submit-a-pull-request:

Submit a pull request
^^^^^^^^^^^^^^^^^^^^^
Once you've made changes and pushed them to your forked repository, you then submit a PR to have
them integrated into the geotech-pandas code base.

You can find a PR tutorial in the `GitHub's Help Docs
<https://help.GitHub.com/articles/using-pull-requests/>`__.

.. _update-your-pull-request:

Update your pull request
^^^^^^^^^^^^^^^^^^^^^^^^
Based on the review you get on your PR, you will probably need to make some changes to the code. You
can follow the above steps again to address any feedback and update your PR.

It is also important that updates in the geotech-pandas ``main`` branch are reflected in your pull
request. To update your feature branch with changes in the geotech-pandas ``main`` branch, run::

    git checkout shiny-new-feature
    git fetch upstream
    git merge upstream/main

If there are no conflicts, or if they could be fixed automatically, a file with a default commit
message will open, and you can simply save and quit this file.

If there are merge conflicts, you need to solve those conflicts. For more information, see
`Resolving a merge conflict using the command line
<https://help.GitHub.com/articles/resolving-a-merge-conflict-using-the-command-line/>`__.

Once the conflicts are resolved, run:

#. ``git add -u`` to stage any files you've updated;
#. ``git commit`` to finish the merge.

.. note::

    If you have uncommitted changes at the moment you want to update the branch with ``main``, you
    will need to ``stash`` them prior to updating. This will effectively store your changes and they
    can be reapplied after updating. For more information, see `Stashing and Cleaning
    <https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning>`__.

After the feature branch has been update locally, you can now update your PR by pushing to the
branch on GitHub::

    git push origin shiny-new-feature

Any ``git push`` will automatically update your PR with your branch's changes and restart the CI
checks.

.. _update-your-development-environment:

Update your development environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
It is important to periodically update your local ``main`` branch with updates from the
geotech-pandas ``main`` branch and update your development environment to reflect any changes to the
various packages that are used during development. To do that, run::

    git checkout main
    git fetch upstream
    git merge upstream/main

Run ``uv sync --upgrade`` from within the development environment to upgrade all dependencies to
the latest versions allowed by ``pyproject.toml``. Add ``--only-dev`` to upgrade the development
dependencies only.

If there are any updates to the dependencies, for instance, if the ``pyproject.toml`` file is
changed, then you must also rebuild your Dev Container:

#. *GitHub Codespaces*:
   
   Run :kbd:`Ctrl/⌘` + :kbd:`⇧` + :kbd:`P` → *Codespaces: Rebuild Container*

#. *VS Code*:
   
   Run :kbd:`Ctrl/⌘` + :kbd:`⇧` + :kbd:`P` → *Dev Containers: Rebuild Container*.

#. *PyCharm*:
   
   See PyCharm's documentation about `Docker Compose
   <https://www.jetbrains.com/help/pycharm/docker-compose.html>`__.

#. *Terminal*:

   Open your fork with your terminal, and run::
      
      docker compose up --build --detach dev
   
   to start and rebuild a Dev Container in the background, and then run::
   
      docker compose exec dev zsh
   
   to open a shell prompt in the Dev Container.

Tips for a successful pull request
----------------------------------
Once you have :ref:`submitted a PR<submit-a-pull-request>`, one of the core contributors may take a
look. Please note however that there are only a handful of people are responsible for reviewing all
of the contributions, which can often lead to bottlenecks.

To improve the chances of your PR being reviewed, you should:

- **Reference an** `open issue <https://GitHub.com/fraserdominicdavid/geotech-pandas/issues?q=is%3Aissue+is%3Aopen+no%3Aassignee+sort%3Aupdated-desc>`__
  for non-trivial changes to clarify the PR's purpose;
- **Ensure you have** :ref:`reasonable tests<add-reasonable-tests>` and present them in the PR;
- **Keep your PRs as simple as possible** to make it easier to review the PR;
- **Ensure that GHA status is green**, otherwise, reviewers may not even take a look; and
- **Keep** :ref:`updating your PR<update-your-pull-request>`, either by the request of a reviewer or
  every few days to keep up-to-date with the current geotech-pandas codebase.

Bumping the package version
---------------------------
Run ``cz bump`` to bump the package's version, update the ``CHANGELOG.rst``, and create a git tag.
Then push the changes and the git tag with ``git push origin main --tags``.
