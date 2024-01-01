---
title: Vectors and Scalars
topic: Template
author: Firas Moosvi
source: original
template_version: 1.4
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
  imports: |
    import random as rd; rd.seed(111)
    import pandas as pd
    import problem_bank_helpers as pbh
  generate: |
    data2 = pbh.create_data2()

    # define or load names/items/objects
    names = pbh.names.copy()

    # store phrases etc
    data2["params"]["vars"]["title"] = 'Vectors and Scalars'
    data2["params"]["vars"]["name"] = rd.choice(names)

    # define useful variables/lists
    vectors = ["displacement", "velocity", "acceleration", "momentum", "force", "lift", "drag", "thrust", "weight"]
    scalars = ["length", "area", "volume", "mass", "density", "pressure", "temperature", "energy", "entropy", "work", "power"]

    # Randomly select 2,3,4 scalars and shuffle the lists
    total_choices = 6
    num_scalars = rd.choice([2,3,4])
    num_vectors = total_choices - num_scalars
    select = rd.choice(["vectors","scalars"])

    data2["params"]["choice"] = select

    # Create ans_choices
    ans_choices = [f"ans{i+1}" for i in range(total_choices)]

    rd.shuffle(scalars)
    rd.shuffle(vectors)

    # define possible answers
    if select == "vectors":
        for i in range(num_vectors):
            choice = ans_choices.pop(0)
            data2["params"]["part1"][choice]["value"] = vectors.pop()
            data2["params"]["part1"][choice]["correct"] = True
            data2["params"]["part1"][choice]["feedback"] = "Correct! Nice work"

        for i in range(num_scalars):
            choice = ans_choices.pop(0)
            data2["params"]["part1"][choice]["value"] = scalars.pop()
            data2["params"]["part1"][choice]["correct"] = False
            data2["params"]["part1"][choice]["feedback"] = "Not quite - Try again!"

    elif select == "scalars":
        for i in range(num_scalars):
            choice = ans_choices.pop(0)
            data2["params"]["part1"][choice]["value"] = scalars.pop()
            data2["params"]["part1"][choice]["correct"] = True
            data2["params"]["part1"][choice]["feedback"] = "Correct! Nice work"

        for i in range(num_vectors):
            choice = ans_choices.pop(0)
            data2["params"]["part1"][choice]["value"] = vectors.pop()
            data2["params"]["part1"][choice]["correct"] = False
            data2["params"]["part1"][choice]["feedback"] = "Not quite - Try again!"

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
  type: checkbox
  pl-customizations:
    weight: 1
    partial-credit: true
    partial-credit-method: EDC
---
# {{ params.vars.title }}

## Part 1

{{ params.vars.name }} is given a list of physical quantities and has to identify all of the {{ params.choice }}. Can you help?

### Answer Section 

- {{{ params.part1.ans1.value }}}
- {{{ params.part1.ans2.value }}}
- {{{ params.part1.ans3.value }}}
- {{{ params.part1.ans4.value }}}
- {{{ params.part1.ans5.value }}}
- {{{ params.part1.ans6.value }}}

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

