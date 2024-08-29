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
assets:
server:
    imports: |
        import random as rd
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

        # define correct answers
        data2["correct_answers"]["part1_ans"] = v*t
        data2["correct_answers"]["part2_ans"] = v*t

        # Update the data object with a new dict
        data.update(data2)
    prepare: |
        pass
    parse: |
        pass
    grade: |
        data = pbh.automatic_feedback(data,rtol=0.03)
        #pass
part1:
  type: number-input
  pl-customizations:
    rtol: 0.05
    weight: 1
    allow-blank: true
    label: $d= $
    suffix: m
part2:
  type: number-input
  pl-customizations:
    rtol: 0.05
    weight: 1
    allow-blank: true
    label: $d= $
    suffix: m
---
# {{ params.vars.title }}

{{ params.vars.name }} is traveling on {{ params.vars.vehicle }} at {{ params.v }} {{ params.vars.units }}.

## Part 1

How far does {{ params.vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

### Answer Section

Please enter in a numeric value in {{ params.vars.units }}.

### pl-submission-panel

{{ feedback.part1_ans }}

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

## Part 2

How far does {{ params.vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

### Answer Section

Please enter in a numeric value in {{ params.vars.units }}.

### pl-submission-panel

{{ feedback.part1_ans }}

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.
