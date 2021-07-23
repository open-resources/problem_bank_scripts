---
title: Distance travelled
topic: Template
author: Firas Moosvi
source: original
template_version: 1.1
attribution: standard
outcomes:
- 6.1.1.0
- 6.1.1.1
difficulty:
- undefined
randomization:
- undefined
taxonomy:
- undefined
tags:
- unknown
assets:
server: 
    imports: |
        import random;random.seed(111)
        import pandas as pd
        import problem_bank_helpers as pbh
    generate: |
        data2 = pbh.create_data2()

        # define or load names/items/objects
        names = pd.read_csv("data/names.csv")["Names"].tolist()
        manual_vehicles = pd.read_csv("data/manual_vehicles.csv")["Manual Vehicles"].tolist()

        # store phrases etc
        data2["params"]["vars"]["name"] = random.choice(names)
        data2["params"]["vars"]["vehicle"] = random.choice(manual_vehicles)
        data2["params"]["vars"]["title"] = "Distance travelled"
        data2["params"]["vars"]["units"] = "m/s"

        # define bounds of the variables
        v = random.randint(2,7)
        t = random.randint(5,10)

        # store the variables in the dictionary "params"
        data2["params"]["v"] = v
        data2["params"]["t"] = t

        # define possible answers
        data2["params"]["part1"]["ans1"]["value"] = pbh.roundp(42)
        data2["params"]["part1"]["ans1"]["correct"] = False

        data2["params"]["part1"]["ans2"]["value"] = pbh.roundp(v*t)
        data2["params"]["part1"]["ans2"]["correct"] = True

        data2["params"]["part1"]["ans3"]["value"] = pbh.roundp(v+t)
        data2["params"]["part1"]["ans3"]["correct"] = False

        data2["params"]["part1"]["ans4"]["value"] = pbh.roundp(v/t)
        data2["params"]["part1"]["ans4"]["correct"] = False

        data2["params"]["part1"]["ans5"]["value"] = pbh.roundp(v-t)
        data2["params"]["part1"]["ans5"]["correct"] = False

        data2["params"]["part1"]["ans6"]["value"] = pbh.roundp(1.3*(v-t))
        data2["params"]["part1"]["ans6"]["correct"] = False

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

- {{ params.part1.ans1}} {{ params.vars.units}} 
- {{ params.part1.ans2}} {{ params.vars.units}} 
- {{ params.part1.ans3}} {{ params.vars.units}} 
- {{ params.part1.ans4}} {{ params.vars.units}} 
- {{ params.part1.ans5}} {{ params.vars.units}} 

## pl-submission-panel

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.

## pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.