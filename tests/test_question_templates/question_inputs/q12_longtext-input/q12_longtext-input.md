---
title: Describe an Experiment
topic: Template
author: Michael Kudla
source: original
template_version: 1.4
attribution: standard
partialCredit: true
singleVariant: false
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
    imports: |
        import problem_bank_helpers as pbh
    generate: |
        data2 = pbh.create_data2()

        # Update the data object with a new dict
        data.update(data2)
part1:
  type: longtext
  gradingMethod: Manual
  pl-customizations:
    placeholder: "Type your answer here..."
    file-name: "answer.html"
    quill-theme: "snow"
    directory: clientFilesQuestion
    source-file-name: sample.html
---
# {{ params.vars.title }}

## Question Text

You have at your disposal a measuring tape and a ball. Describe an experiment you could perform to estimate the speed of a ball as it hits the ground, when dropped from any height.
Include any formulas you might use.
Estimate the accuracy of your measurement in terms of the uncertainty in your velocity prediction.
What factors would be unaccounted for in your velocity prediction?

### Answer Section

Answer in 5-7 sentences, try and use full sentences.

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
