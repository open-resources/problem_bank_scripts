---
title: Multi-part Question
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
- test1.png
- test2.png
server:
  imports: |
    import random
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
    allow-blank: true
    weight: 1
part2:
  type: multiple-choice
  pl-customizations:
    weight: 1
substitutions:
  params:
    vars:
      name: Abbas
      vehicle: a skateboard
      title: Distance travelled
      units: m/s
    v: 3
    t: 9
    part2:
      ans1:
        value: 42
        correct: false
      ans2:
        value: 27
        correct: true
      ans3:
        value: 12
        correct: false
      ans4:
        value: 0.3333333333333333
        correct: false
      ans5:
        value: -6
        correct: false
      ans6:
        value: -7.800000000000001
        correct: false
  correct_answers:
    part1_ans: 27
---
# {{ params.vars.title }}
This part of the question is common to both Parts 1 and 2.

<img src="test1.png" width=400>

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).
![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)