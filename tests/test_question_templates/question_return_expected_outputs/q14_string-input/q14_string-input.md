---
title: Code Output
topic: Template
author: Gavin Kendal-Freedman
source: original
template_version: 1.0
attribution: standard
gradingMethod: true
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
server:
  imports: "import random; random.seed(111) \nimport problem_bank_helpers as pbh\n"
  generate: |
    data2 = pbh.create_data2()

    a = random.randint(2, 4)
    stringname = "love"

    data2["params"]["vars"]["title"] = "Code Output"
    data2["params"]["vars"]["a"] = a
    data2["params"]["vars"]["stringname"] = stringname
    data2["correct_answers"]["ans"] = ""
    # we can also add alternate correct answers, which will we can grade as correct
    # lets say we want to accept "Love" as an correct answer as an example, we can do:
    data2["params"]["part1"]["alternate_correct_ans"] = [a * stringname, a * "Love"]

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
  grade: "# Since we want an alternate correct answer, we can check for it here, and\
    \ override the automatic \n# score if it is correct\nif data[\"submitted_answers\"\
    ][\"ans\"] in data[\"params\"][\"part1\"][\"alternate_correct_ans\"]:\n    data[\"\
    partial_scores\"][\"ans\"] = { \"score\": 1 }\n"
part1:
  type: string-input
  pl-customizations:
    display: block
    placeholder: '...'
    ignore-case: true
---
# {{ params.vars.title }}

## Part 1

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

