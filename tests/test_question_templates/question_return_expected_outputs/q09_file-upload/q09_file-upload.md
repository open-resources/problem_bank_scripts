---
title: File Upload
topic: Template
author: UNABLE TO ROUNDTRIP
source: UNABLE TO ROUNDTRIP
template_version: UNABLE TO ROUNDTRIP
attribution: standard
gradingMethod: true
partialCredit: true
singleVariant: false
showCorrectAnswer: false
outcomes:
- UNABLE TO ROUNDTRIP
difficulty:
- UNABLE TO ROUNDTRIP
randomization:
- UNABLE TO ROUNDTRIP
taxonomy:
- UNABLE TO ROUNDTRIP
span:
- UNABLE TO ROUNDTRIP
length:
- UNABLE TO ROUNDTRIP
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

{{ #feedback.manual }} 
	Feedback from course staff:
{{{ feedback.manual }}}
	{{ /feedback.manual }}

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

## Rubric

UNABLE TO ROUNDTRIP, Defaulting to 'This should be hidden from students until after the deadline.'

## Solution

UNABLE TO ROUNDTRIP, Defaulting to 'This should never be revealed to students.'.

## Comments

UNABLE TO ROUNDTRIP, Defaulting to 'These are random comments associated with this question.'

