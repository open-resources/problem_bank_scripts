---
title: Distance travelled
topic: Template
author: Firas Moosvi
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

    # define possible answers
    data2["params"]["part1"]["ans1"]["value"] = pbh.roundp(42)
    data2["params"]["part1"]["ans1"]["correct"] = False
    data2["params"]["part1"]["ans1"]["feedback"] = "This is a random number, you probably selected this choice by mistake! Try again please!"

    data2["params"]["part1"]["ans2"]["value"] = pbh.roundp(v*t)
    data2["params"]["part1"]["ans2"]["correct"] = True
    data2["params"]["part1"]["ans2"]["feedback"] = "Great! You got it."

    data2["params"]["part1"]["ans3"]["value"] = pbh.roundp(v+t)
    data2["params"]["part1"]["ans3"]["correct"] = False
    data2["params"]["part1"]["ans3"]["feedback"] = "Hmm, does it make sense to add a velocity and a time? Check the units!"

    data2["params"]["part1"]["ans4"]["value"] = pbh.roundp(v/t)
    data2["params"]["part1"]["ans4"]["correct"] = False
    data2["params"]["part1"]["ans4"]["feedback"] = "Hmm, check the units of the resulting answer: v/t."

    data2["params"]["part1"]["ans5"]["value"] = pbh.roundp(v-t)
    data2["params"]["part1"]["ans5"]["correct"] = False
    data2["params"]["part1"]["ans5"]["feedback"] = "Hmm, does it make sense to subtract a velocity and a time? Check the units!"

    data2["params"]["part1"]["ans6"]["value"] = pbh.roundp(1.3*(v-t))
    data2["params"]["part1"]["ans6"]["correct"] = False
    data2["params"]["part1"]["ans6"]["feedback"] = "Hmm, does it make sense to subtract a velocity and a time? Check the units!"

    # Update the data object with a new dict
    data.update(data2)
  prepare: 'pass

    '
  parse: 'pass

    '
  grade: 'pass

    '
part1:
  type: dropdown
  pl-customizations:
    weight: 1
    blank: 'true'
myst:
  substitutions:
    params:
      vars:
        name: Maya
        vehicle: a unicycle
        title: Distance travelled
        units: m/s
      v: 5
      t: 6
      part1:
        ans1:
          value: 42
          correct: false
          feedback: This is a random number, you probably selected this choice by
            mistake! Try again please!
        ans2:
          value: 30
          correct: true
          feedback: Great! You got it.
        ans3:
          value: 11
          correct: false
          feedback: Hmm, does it make sense to add a velocity and a time? Check the
            units!
        ans4:
          value: 0.833
          correct: false
          feedback: 'Hmm, check the units of the resulting answer: v/t.'
        ans5:
          value: -1
          correct: false
          feedback: Hmm, does it make sense to subtract a velocity and a time? Check
            the units!
        ans6:
          value: -1.3
          correct: false
          feedback: Hmm, does it make sense to subtract a velocity and a time? Check
            the units!

---
# {{ params.vars.title }}

## Useful Info

This element is depreciated and `pl-multiple-choice` (or `pl-matching`) should be used instead. See https://prairielearn.readthedocs.io/en/latest/elements/#pl-dropdown-element for more information.

## Question Text

{{ params.vars.name }} is traveling on {{ params.vars.vehicle }} at {{ params.v }} {{ params.vars.units }}.
How far does {{ params.vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

### Answer Section

- {{ params.part1.ans1}} {{ params.vars.units}}
- {{ params.part1.ans2}} {{ params.vars.units}}
- {{ params.part1.ans3}} {{ params.vars.units}}
- {{ params.part1.ans4}} {{ params.vars.units}}
- {{ params.part1.ans5}} {{ params.vars.units}}

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

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)