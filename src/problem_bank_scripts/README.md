# TUI instructions
Creates a barebones OPB markdown question via a series of tui prompts.

## Table of Contents
- [Getting started](#getting-started)
- [Usage](#usage)
- [Variables](#variables)
- [Terminal commands](#terminal-commands)
- [Saving results](#saving-results)
- [Creating a PR](#creating-a-pr)
- [GPT](#gpt)

## Getting started

Install the package via pip:
```shell
pip install "problem_bank_scripts[tui] @ git+https://github.com/open-resources/problem_bank_scripts"
```

Create a `.env` file in the directory you will be running the TUI. In it, fill in the required variables below, and any optional variables you wish to use.

```
# REQUIRED VARIABLES
GITHUB_USERNAME=
WRITE_PATH=         # This is used with the --create-pr flag. This should go to <your_path>/instructor_stats_bank/source/unsorted
PL_QUESTION_PATH=   # Path the local prairielearn. <your_path>/pl-opb-ind100/questions/FM
MY_NAME=
MY_INITIALS=

# OPTIONAL VARIABLES
TEXTBOOK=            # ex. openstax-stats-2e
GITHUB_ACCESS_TOKEN= # allows writing PRs
OPENAI_API_KEY=      # allows using OpenAI API
```

## Usage

Create a question via:
```shell
pbs-cli create-question
# OR
python -m problem_bank_scripts.tui
```

For more information run `pbs-cli create-question --help`

To see all available commands, run `pbs-cli --help`.

## Variables
To designate certain values as variables, wrap it in curly braces, and prefix it with the variable name you want as follows:
`{<variablename>:<original value>}`

#### Example
To make `12.6` a variable in the sentence `12.6% are age 65 and over.`, you would write it as:
```shell
{percent_senior:12.6}% are age 65 and over.
```

So for the following input
![alt text](variable_example.png "Title")
would result in:
```yml
  generate: |
        ...

        percent_senior = round(random.uniform(11.3, 13.9), 1)  # 12.6

        data2['params']['percent_senior'] = percent_senior

        ...
---

{{ params.percent_senior }}% are age 65 and over.

```
For string variables, make sure add quotes around the value:
```shell
{percent_senior:"12.6"}% are age 65 and over.
```

## Terminal commands
<kbd>Ctrl</kbd> + <kbd>C</kbd> Exit the program
<kbd>Ctrl</kbd> + <kbd>U</kbd> clears the line for the input you are in.

## Saving results
In case you run into an issue where either you cancel the program before it terminates or it crashes due to an exception being thrown, the data you have already inputted will be saved in a file called `saved.json`.

You will be given the option to use this file the next time you run `pbs-cli create-question`, so that you do not need to re-enter all the data again.

> [!WARNING]
> `saved.json` is overwritten each time you run the program. If you want to keep the file for future use, create a copy of it.

## Creating a PR
To automatically have your generated Markdown question committed to Github with a draft PR created for it, add the `--create-pr` flag to the command. Make sure `WRITE_PATH` in your `.env` file is set correctly.

## GPT
> [!WARNING]
> OpenStax forbids using their material in LLMs without permission, so do not use the --gpt flag with OpenStax textbooks.

To allow use of GPT add the `--gpt` flag to the command.
```shell
pbs-cli create-question --gpt
```

This allows for GPT use in generating multiple-choice options and number-input solutions.
