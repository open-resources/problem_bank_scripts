---
title: Distance travelled
topic: Template
author: Firas Moosvi
source: 5.45
template_version: 1.4
attribution: openstax-physics-vol2
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
- test1.png
- test2.png
part1:
  type: multiple-choice
  pl-customizations:
    weight: 1
myst:
  substitutions:
    params:
      vars:
        title: Kinematics
        name: Maya
        vehicle: a unicycle
        units: m/s
      v: 5
      t: 6
      part1:
        ans1:
          value: '`42`'
          feedback: This is a random number, you probably selected this choice by
            mistake! Try again please!
        ans2:
          value: '`30`'
          feedback: Great! You got it.
        ans3:
          value: '`11`'
          feedback: Hmm, does it make sense to add a velocity and a time? Check the
            units!
        ans4:
          value: '`0.833`'
          feedback: 'Hmm, check the units of the resulting answer: v/t.'
        ans5:
          value: '`-1`'
          feedback: Hmm, does it make sense to subtract a velocity and a time? Check
            the units!
        ans6:
          value: '`-1.3`'
          feedback: Hmm, does it make sense to subtract a velocity and a time? Check
            the units!
---
# {{ params.vars.title }}
{{ params.vars.name }} is traveling on {{ params.vars.vehicle }} at {{ params.v }} {{ params.vars.units }}.

<img src="test1.png">

## Part 1

How far does {{ params.vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

<img src="test2.png">

### Answer Section

- {{ params.part1.ans1.value }} {{ params.vars.units}}
- {{ params.part1.ans2.value }} {{ params.vars.units}}
- {{ params.part1.ans3.value }} {{ params.vars.units}}
- {{ params.part1.ans4.value }} {{ params.vars.units}}
- {{ params.part1.ans5.value }} {{ params.vars.units}}
- {{ params.part1.ans6.value }} {{ params.vars.units}}

## Attribution

Problem is from the [OpenStax University Physics Volume 2](https://openstax.org/details/books/university-physics-volume-2) textbook, licensed under the [CC-BY 4.0 license](https://creativecommons.org/licenses/by/4.0/).<br>![Image representing the Creative Commons 4.0 BY license.](https://raw.githubusercontent.com/firasm/bits/master/by.png)