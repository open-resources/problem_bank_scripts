---
title: File Upload
topic: Template
author: Michael Kudla
source: original
template_version: 1.4
attribution: standard
gradingMethod: Manual
partialCredit: true
singleVariant: false
showCorrectAnswer: false
outcomes:
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
server:
  imports: 'import problem_bank_helpers as pbh

    '
  generate: |
    data2 = pbh.create_data2()

    data2["params"]["vars"]["title"] = "File Upload"

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
    pass
  grade: |
    pass
part1:
  type: file-upload
  pl-customizations:
    file-names: file.png, file.jpg, file.pdf, filename space.png
---
# {{ params.vars.title }}

## Part 1

A block sits on an incline plane of angle 30 degrees to the horizontal.
Draw a free body diagram for the block by hand, take a picture, and upload it.
Your file must be a png, jpg, or pdf.

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

These are random comments associated with this question.

