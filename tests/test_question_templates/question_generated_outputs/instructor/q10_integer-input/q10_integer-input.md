---
title: Integer Math
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
assets: null
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
    data2["params"]["vars"]["title"] = "Integer Math"
    data2["params"]["vars"]["units"] = "m/s"

    # define bounds of the variables
    n = random.randint(2,100)

    # store the variables in the dictionary "params"
    data2["params"]["n"] = n

    # define correct answers
    data2["correct_answers"]["part1_ans"] = int(n*10)

    # Update the data object with a new dict
    data.update(data2)
  prepare: 'pass

    '
  parse: 'pass

    '
  grade: 'pass

    '
part1:
  type: number-input
  label: $d=$
  pl-customizations:
    weight: 1
    allow-blank: true
substitutions:
  params:
    vars:
      name: Maya
      vehicle: a unicycle
      title: Integer Math
      units: m/s
    n: 65
  correct_answers:
    part1_ans: 650
---
# {{ params.vars.title }}
## Question Text

{{ params.vars.name }} is on a {{ params.vars.vehicle }} trying to calculate the result of 10 x {{ params.n }} {{ params.vars.units }}.

### Answer Section

Please enter an integer value in {{ params.vars.units }}.
## Rubric

This should be hidden from students until after the deadline.
## Solution

This should never be revealed to students.
## Comments

These are random comments associated with this question.

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)