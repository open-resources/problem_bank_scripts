---
title: Moving and copying files
topic: Template
author: Jonatan Schroeder; Converted by Gavin Kendal-Freedman
source: original
template_version: 1.0
attribution: standard
partialCredit: true
singleVariant: false
showCorrectAnswer: false
outcomes:
- 6.1.1.0
- 6.1.1.1
difficulty:
- undefined
randomization:
- undefined
taxonomy:
- undefined
span:
- undefined
length:
- undefined
tags:
- unknown
serverFiles:
- file1.txt
- file2.txt
- filebad.txt
server:
  imports: "import base64 \nimport problem_bank_helpers as pbh\n"
  generate: |
    data2 = pbh.create_data2()

    data2["params"]["vars"]["title"] = "Moving and copying files"

    # Update the data object with a new dict
    data.update(data2)

    # Start code added automatically by problem_bank_scripts

    # Convert backticks to code blocks/fences in answer choices.
    pbh.backticks_to_code_tags(data2)

    # Update data with data2
    data.update(data2)

    # End code added in by problem bank scripts
  prepare: |
    pass
  parse: |
    if '_files' in data['format_errors']:
        del data['format_errors']['_files']
  grade: |
    files = { f['name']: f['contents'] for f in data['submitted_answers'].get('_files', []) }
    data['feedback']['results'] = []
    data['score'] = 0

    with open('workspace/file1.txt', 'rb') as f:
        file1_content = base64.b64encode(f.read()).decode()
    with open('workspace/file2.txt', 'rb') as f:
        file2_content = base64.b64encode(f.read()).decode()

    if 'newdir/file1_new.txt' not in files:
        data['feedback']['results'].append('newdir/file1_new.txt was not created.')
    elif files['newdir/file1_new.txt'] != file1_content:
        data['feedback']['results'].append('newdir/file1_new.txt was created, but it is not based on file1.txt.')
    elif 'file1.txt' in files:
        data['feedback']['results'].append('newdir/file1_new.txt was created properly, but the old file still exists.')
        data['score'] += 0.2
    else:
        data['feedback']['results'].append('file1.txt moved successfully.')
        data['score'] += 0.4

    if 'newdir/file2_new.txt' not in files:
        data['feedback']['results'].append('newdir/file2_new.txt was not created.')
    elif files['newdir/file2_new.txt'] != file2_content:
        data['feedback']['results'].append('newdir/file2_new.txt was created, but it is not based on file2.txt.')
    elif 'file2.txt' not in files:
        data['feedback']['results'].append('newdir/file2_new.txt was created properly, but the old file no longer exists.')
        data['score'] += 0.2
    else:
        data['feedback']['results'].append('file2.txt copied successfully.')
        data['score'] += 0.4

    if files and 'filebad.txt' in files:
        data['feedback']['results'].append('filebad.txt still exists.')
    else:
        data['feedback']['results'].append('filebad.txt deleted successfully.')
        data['score'] += 0.2
part1:
  type: workspace
  pl-customizations: {}
---
# {{ params.vars.title }}

## Part 1

Open the Workspace below and perform the following tasks.

- Create a new directory called `newdir`;
- Move the file `file1.txt` to the directory `newdir`, with the new name `file1_new.txt`;
- Copy the file `file2.txt` to the directory `newdir`, with the new name `file2_new.txt`;
- Delete the file `filebad.txt`.

Once you complete these tasks, click on "Save &amp; Grade" below.

### Answer Section 

### pl-submission-panel

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question:

This example problem was originally created by [Jonatan Schroeder](https://www.cs.ubc.ca/people/jonatan-schroeder), and was later converted to the OER markdown layout.

