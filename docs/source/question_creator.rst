.. role:: shell(code)
    :language: shell

=================================
Terminal-Based Question Generator
=================================

Creates a barebones OPB markdown question via a series of tui prompts.

Getting started
---------------

Install the package via pip:

.. code-block:: console

    $ pip install "problem_bank_scripts[tui] @ git+https://github.com/open-resources/problem_bank_scripts"


Create a ``.env`` file in the directory you will be running the TUI.

In it, fill in the required variables below, and any optional variables you wish to use.

+---------------------------+--------------------------------------------------------------+--------------------------+
| Variable                  | Description                                                  | Required?                |
+===========================+==============================================================+==========================+
| :code:`GITHUB_USERNAME`   | Your Username On GitHub                                      | Yes                      |
+---------------------------+--------------------------------------------------------------+--------------------------+
|| :code:`WRITE_PATH`       || The absolute path to the question bank                      || Yes                     |
||                          || the question should be created in                           ||                         |
||                          || when using the :code:`--create-pr` option, e.g.,            ||                         |
||                          || ``/home/<your-name>/instructor_stats_bank/source/unsorted`` ||                         |
+---------------------------+--------------------------------------------------------------+--------------------------+
|| :code:`PL_QUESTION_PATH` || The absolute path to your local prairielearn course,        || Yes                     |
||                          || e.g., ``/home/<your-name>/pl-opb-ind100/questions``         ||                         |
+---------------------------+--------------------------------------------------------------+--------------------------+
| :code:`MY_NAME`           | Your Name                                                    | Yes                      |
+---------------------------+--------------------------------------------------------------+--------------------------+
| :code:`MY_INITIALS`       | Your Initials                                                | Yes                      |
+---------------------------+--------------------------------------------------------------+--------------------------+
| :code:`OPENAI_API_KEY`    | Allows using the OpenAI API                                  | If :code:`--gpt` is used |
+---------------------------+--------------------------------------------------------------+--------------------------+
|| :code:`TEXTBOOK`         || The textbook you're creating the question from,             || No                      |
||                          || e.g., ``openstax-stats-2e``                                 ||                         |
+---------------------------+--------------------------------------------------------------+--------------------------+

Usage
-----

Create a question via:

.. code-block:: shell

    pbs-cli create-question
    # OR
    python -m problem_bank_scripts.tui

For more information run :shell:`pbs-cli create-question --help`

To see all available commands, run :shell:`pbs-cli --help`.

Variables
---------

To designate certain values as variables, wrap it in curly braces,
and prefix it with the variable name you want as follows:

.. code-block:: text

    {<variablename>:<original value>}

Variable Example
~~~~~~~~~~~~~~~~

To make ``12.6`` a variable in the sentence 
:code:`12.6% are age 65 and over.`, you would write it as:

.. code-block:: text

    {percent_senior:12.6}% are age 65 and over.

So for the following input in the TUI:

.. image:: images/variable_example.png
    :alt: Variable Example
    :scale: 75%

would result in the following being generated in the ``generate`` function:

.. code-block:: yaml

    generate: |
        ...

        percent_senior = round(random.uniform(11.3, 13.9), 1)  # 12.6

        data2['params']['percent_senior'] = percent_senior

        ...

and the following in the markdown file generated:

.. code-block:: markdown

    # {{ params.title }}

    {{ params.percent_senior }}% are age 65 and over.
    
    ...


For string variables, make sure add quotes around the value:

.. code-block:: text

    {percent_senior:"12.6"}% are age 65 and over.


Terminal commands
-----------------


The following commands can be used in the terminal:

.. list-table::
    :widths: auto
    :header-rows: 1

    * - Command
      - Description
    * - :kbd:`Ctrl + C`
      - Exit the program
    * - :kbd:`Ctrl + D`
      - Exit the program (same as :kbd:`Ctrl + C`, but can be used if :kbd:`Ctrl + C` is not working)
    * - :kbd:`Ctrl + U`
      - Clears the line for the input you are in. 

Saving results
--------------

In case you run into an issue where either you cancel the program
before it terminates or it crashes due to an exception being thrown,
the data you have already inputted will be saved in a file called `saved.json`.

You will be given the option to use this file the next time you run 
:shell:`pbs-cli create-question`, so that you do not need to re-enter all the data again.

.. warning::

    ``saved.json`` is overwritten each time you run the program.
    If you want to keep the file for future use, you should create a copy of it.


You can use the ``--saved-json`` argument to specify a different file to read from and write to:

.. code-block:: shell

    pbs-cli create-question --saved-json <path_to_file>


Creating a PR
-------------

To automatically have your generated Markdown question committed to Github with
a draft PR created for it, add the ``--create-pr`` flag to the command.
Make sure ``WRITE_PATH`` in your ``.env`` file is set correctly.

``gh`` must be installed and authenticated for this to work.

* To install, follow the instructions at on `Github <https://github.com/cli/cli?tab=readme-ov-file#installation>`_.
* To authenticate, run :shell:`gh auth login`, as explained in the `Github CLI documentation <https://cli.github.com/manual/gh_auth_login>`_.

GPT
---

.. warning::

    OpenStax forbids using their material in LLMs without permission, so do not use the ``--gpt`` flag with OpenStax textbooks.

To allow use of GPT add the ``--gpt`` flag to the command:

.. code-block:: shell

    pbs-cli create-question --gpt

This allows for GPT use in generating multiple-choice options and number-input solutions.
