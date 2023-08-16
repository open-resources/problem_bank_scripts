---
title: Simple Harmonic Spring
topic: Energy
author: UNABLE TO ROUNDTRIP
source: UNABLE TO ROUNDTRIP
template_version: UNABLE TO ROUNDTRIP
attribution: standard
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
- MP
server:
  imports: |
    import random
    import math
    import pandas as pd
    import problem_bank_helpers as pbh
  generate: |
    data2 = pbh.create_data2()

    # store phrases etc
    data2["params"]["vars"]["title"] = "Simple harmonic spring"
    data2["params"]["vars"]["units1"] ="m/s"
    data2["params"]["vars"]["units2"] ="N/m"
    data2["params"]["vars"]["units3"] = "m"

    # define bounds of the variables
    m = random.randint(315,335)
    T = pbh.roundp(random.uniform(0.2,2.0), sigfigs=2)
    E = pbh.roundp(random.uniform(4,7), sigfigs = 2)

    # store the variables in the dictionary "params"
    data2["params"]["m"] = m
    data2["params"]["T"] = T
    data2["params"]["E"] = E

    # define correct answers
    # m is divided by 1000 since it is given in grams
    data2["correct_answers"]["part1_ans"] = pbh.roundp(math.sqrt(2*E/(m/1000)), sigfigs = 2)
    data2["correct_answers"]["part2_ans"] = pbh.roundp((m/1000)*((2*math.pi/T)**2), sigfigs = 2)
    data2["correct_answers"]["part3_ans"] = pbh.roundp(math.sqrt(2*E/((m/1000)*((2*math.pi/T)**2))), sigfigs = 2)

    # Update the data object with a new dict
    data.update(data2)
  prepare: |
    pass
  parse: |
    pass
  grade: "pass      \n"
part1:
  type: number-input
  pl-customizations:
    rtol: 0.05
    weight: 1
    allow-blank: true
    label: $v= $
    suffix: m/s
part2:
  type: number-input
  pl-customizations:
    rtol: 0.05
    weight: 1
    allow-blank: true
    label: $k= $
    suffix: N/m
part3:
  type: number-input
  pl-customizations:
    rtol: 0.05
    weight: 1
    allow-blank: true
    label: $A=$
    suffix: m
---
# {{ params.vars.title }}

A {{params.m}} g object is attached to a spring and executes simple harmonic motion with a period of {{params.T}} s.
If the total energy of the system is {{params.E}} J, find:

## Part 1

(a) the maximum speed of the object

### Answer Section 

## Part 2

(b) the spring constant of the spring

### Answer Section 

## Part 3

(c) the amplitude of the motion

### Answer Section 

### pl-submission-panel

No feedback is provided.

### pl-answer-panel

No feedback is provided.

## Rubric

UNABLE TO ROUNDTRIP, Defaulting to 'This should be hidden from students until after the deadline.'

## Solution

UNABLE TO ROUNDTRIP, Defaulting to 'This should never be revealed to students.'.

## Comments

UNABLE TO ROUNDTRIP, Defaulting to 'These are random comments associated with this question.'

