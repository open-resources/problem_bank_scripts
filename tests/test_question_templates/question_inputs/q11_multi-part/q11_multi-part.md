---
title: Multi-part Question
topic: Template
author: Firas Moosvi
source: original
template_version: 1.4
attribution: standard
partialCredit: true
singleVariant: false
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
- test1.png
- test2.png
server: 
  imports: |
        import random; random.seed(111)
        import pandas as pd
        import problem_bank_helpers as pbh
  generate: |
        data2 = pbh.create_data2()
        
        # define or load names/items/objects
        names = pbh.names.copy()
        manual_vehicles = pbh.manual_vehicles.copy()

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
    rtol: 0.05
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

<img src="test1.png" width=400>

## Part 1

{{ params.vars.name }} is traveling on {{ params.vars.vehicle }} at {{ params.v }} {{ params.vars.units }}.
How far does {{ vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

<img src="test2.png" width=400>

### Answer Section

Please enter in a numeric value in {{ params.vars.units }}.

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

- {{ params.part2.ans1.value}} {{ params.vars.units}} 
- {{ params.part2.ans2.value}} {{ params.vars.units}} 
- {{ params.part2.ans3.value}} {{ params.vars.units}} 
- {{ params.part2.ans4.value}} {{ params.vars.units}} 
- {{ params.part2.ans5.value}} {{ params.vars.units}} 
- {{ params.part2.ans6.value}} {{ params.vars.units}}

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