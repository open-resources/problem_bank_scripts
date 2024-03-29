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
assets: null
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
  grade: "# Since we want an alternate correct answer, we can check for it here, and\
    \ override the automatic \n# score if it is correct\nif data[\"submitted_answers\"\
    ][\"ans\"] in data[\"params\"][\"part1\"][\"alternate_correct_ans\"]:\n    data[\"\
    partial_scores\"][\"ans\"] = { \"score\": 1 }\n"
  prepare: 'pass

    '
  parse: 'pass

    '
part1:
  type: string-input
  pl-customizations:
    answers-name: ans
    display: block
    placeholder: '...'
    ignore-case: true
myst:
  substitutions:
    params:
      vars:
        title: Code Output
        a: 2
        stringname: love
      part1:
        alternate_correct_ans:
        - lovelove
        - LoveLove
    correct_answers:
      ans: ''

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

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)