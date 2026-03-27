---
title: Median
topic: Template
author: Gavin Kendal-Freedman
source: original
template_version: 1.4
attribution: standard
partialCredit: true
singleVariant: false
showCorrectAnswer: false
outcomes:
- 6.1.1.0
- 6.1.1.1
difficulty:
- easy
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
server:
    imports: |
        import random
        from statistics import median
        import problem_bank_helpers as pbh
    generate: |
        data2 = pbh.create_data2()

        numbers = sorted(random.randint(1, 100) for _ in range(9))
        # store the variables in the dictionary "params"
        data2["params"]["vars"]["numbers"] = numbers

        # define correct answers
        data2["correct_answers"]["part1_ans"] = median(numbers)

        # Update the data object with a new dict
        data.update(data2)
    prepare: |
        pass
    parse: |
        pass
    grade: |
        pass
part1:
  type: integer-input
  pl-customizations:
    weight: 1
    allow-blank: true
    label: $n= $
---
# {{ params.vars.title }}

Given a list of numbers ${{ params.vars.numbers }}$, what is the `median` of the list?

## Part 1


### Answer Section

Please enter in a numeric value in.

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
