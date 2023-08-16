---
title: Multi-part Question
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
assets:
- test1.png
- test2.png
autogradeTestFiles:
workspaceFiles:
serverFiles:
server:
  imports: |
    import random as rd; rd.seed(111)
    import pandas as pd
    import problem_bank_helpers as pbh
  generate: |
    data2 = pbh.create_data2()

    # define or load names/items/objects
    names = pbh.names.copy()
    manual_vehicles = pbh.manual_vehicles.copy()

    # store phrases etc
    data2["params"]["vars"]["name"] = rd.choice(names)
    data2["params"]["vars"]["vehicle"] = rd.choice(manual_vehicles)
    data2["params"]["vars"]["title"] = "Distance travelled"
    data2["params"]["vars"]["units"] = "m/s"

    # define bounds of the variables
    v = rd.randint(2,7)
    t = rd.randint(5,10)

    # store the variables in the dictionary "params"
    data2["params"]["v"] = v
    data2["params"]["t"] = t

    ## Part 1

    # define correct answers
    data2["correct_answers"]["part1_ans"] = v*t

    ## Part 2

    # define possible answers
    data2["params"]["part2"]["ans1"]["value"] = pbh.roundp(42)
    data2["params"]["part2"]["ans1"]["correct"] = False

    data2["params"]["part2"]["ans2"]["value"] = pbh.roundp(v*t)
    data2["params"]["part2"]["ans2"]["correct"] = True

    data2["params"]["part2"]["ans3"]["value"] = pbh.roundp(v+t)
    data2["params"]["part2"]["ans3"]["correct"] = False

    data2["params"]["part2"]["ans4"]["value"] = pbh.roundp(v/t)
    data2["params"]["part2"]["ans4"]["correct"] = False

    data2["params"]["part2"]["ans5"]["value"] = pbh.roundp(v-t)
    data2["params"]["part2"]["ans5"]["correct"] = False

    data2["params"]["part2"]["ans6"]["value"] = pbh.roundp(1.3*(v-t))
    data2["params"]["part2"]["ans6"]["correct"] = False

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
  type: number-input
  pl-customizations:
    rtol: 0.05
    weight: 1
    allow-blank: true
    label: $d= $
    suffix: m
    comparison: sigfig
    digits: 2
part2:
  type: multiple-choice
  pl-customizations:
    weight: 1
---
# {{ params.vars.title }}

This part of the question is common to both Parts 1 and 2.

## Part 1

{{ params.vars.name }} is traveling on {{ params.vars.vehicle }} at {{ params.v }} {{ params.vars.units }}.
How far does {{ vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

### Answer Section 

### pl-submission-panel

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

## Part 2

{{ params.vars.name }} is traveling on {{ params.vars.vehicle }} at {{ params.v }} {{ params.vars.units }}.
How far does {{ params.vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

### Answer Section 

- {{{ params.part2.ans1.value }}} {{ params.vars.units }}
- {{{ params.part2.ans2.value }}} {{ params.vars.units }}
- {{{ params.part2.ans3.value }}} {{ params.vars.units }}
- {{{ params.part2.ans4.value }}} {{ params.vars.units }}
- {{{ params.part2.ans5.value }}} {{ params.vars.units }}
- {{{ params.part2.ans6.value }}} {{ params.vars.units }}

### pl-submission-panel

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

## Rubric

UNABLE TO ROUNDTRIP, Defaulting to 'This should be hidden from students until after the deadline.'

## Solution

UNABLE TO ROUNDTRIP, Defaulting to 'This should never be revealed to students.'.

## Comments

UNABLE TO ROUNDTRIP, Defaulting to 'These are random comments associated with this question.'

