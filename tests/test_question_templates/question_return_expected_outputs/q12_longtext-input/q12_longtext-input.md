---
title: Describe an Experiment
topic: Template
author: Michael Kudla
source: original
template_version: 1.4
attribution: standard
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
assets:
- sample.html
server:
  imports: 'import problem_bank_helpers as pbh

    '
  generate: |
    data2 = pbh.create_data2()

    data2["params"]["vars"]["title"] = "Describe an Experiment"

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
  type: longtext
  pl-customizations:
    placeholder: Type your answer here...
    file-name: answer.html
    quill-theme: snow
    directory: clientFilesQuestion
    source-file-name: sample.html
---
# {{ params.vars.title }}

## Part 1

You have at your disposal a measuring tape and a ball. Describe an experiment you could perform to estimate the speed of a ball as it hits the ground, when dropped from any height.
Include any formulas you might use.
Estimate the accuracy of your measurement in terms of the uncertainty in your velocity prediction.
What factors would be unaccounted for in your velocity prediction?

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
