---
title: Code Output
topic: Template
author: Gavin Kendal-Freedman
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
assets:
server:
    imports: |
        import random; random.seed(111) 
        import problem_bank_helpers as pbh
    generate: |
        data2 = pbh.create_data2()

        a = random.randint(2, 4)
        stringname = "love"

        data2["params"]["vars"]["title"] = "Code Output"
        data2["params"]["vars"]["a"] = a
        data2["params"]["vars"]["stringname"] = stringname
        data2["correct_answers"]["ans1"] = a * stringname

        # Update the data object with a new dict
        data.update(data2)
part1:
  type: string-input
  gradingMethod: Manual
  pl-customizations:
    answers-name: ans1
    display: block
    placeholder: "..."
    ignore-case: true
---
# {{ params.vars.title }}

## Question Text

For the following python code snippet, enter below the resulting string:

```python
a = "{{ params.vars.stringname }}" * {{ params.vars.a }}
```

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

This example problem is adapted from PrairieLearn's Examples: https://github.com/PrairieLearn/PrairieLearn/tree/master/exampleCourse/questions/element/stringInput

