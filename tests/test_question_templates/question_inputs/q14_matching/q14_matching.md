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

        # define all options for right side of matching
        data2["params"]["part1"]["option1"]["value"] = 1
        data2["params"]["part1"]["option2"]["value"] = 2
        data2["params"]["part1"]["option3"]["value"] = 3

        data2["params"]["part1"]["statement1"]["value"] = pbh.roundp(42)
        data2["params"]["part1"]["statement1"]["matches"] = "option1"
        data2["params"]["part1"]["statement2"]["value"] = pbh.roundp(v*t)
        data2["params"]["part1"]["statement2"]["matches"] = "option1"
        data2["params"]["part1"]["statement3"]["value"] = pbh.roundp(v+t)
        data2["params"]["part1"]["statement3"]["matches"] = "option2"
        data2["params"]["part1"]["statement4"]["value"] = pbh.roundp(v/t)
        data2["params"]["part1"]["statement4"]["matches"] = "option3"

        # Update the data object with a new dict
        data.update(data2)

    prepare: |
        pass
    parse: |
        pass
    grade: |
        pass
part1:
  type: dropdown
  pl-customizations:
    weight: 1
    blank: "true"
---
# {{ params.vars.title }}

## Question Text

{{ params.vars.name }} is traveling on {{ params.vars.vehicle }} at {{ params.v }} {{ params.vars.units }}.
How far does {{ params.vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

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
