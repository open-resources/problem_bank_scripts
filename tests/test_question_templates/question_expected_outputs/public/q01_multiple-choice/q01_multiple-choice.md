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
    params_vars_title: Kinematics
    params_vars_name: Maya
    params_vars_vehicle: a unicycle
    params_vars_units: m/s
    params_v: 5
    params_t: 6
    params_part1_ans1_value: <code>42</code>
    params_part1_ans1_feedback: This is a random number, you probably selected this
      choice by mistake! Try again please!
    params_part1_ans2_value: <code>30</code>
    params_part1_ans2_feedback: Great! You got it.
    params_part1_ans3_value: <code>11</code>
    params_part1_ans3_feedback: Hmm, does it make sense to add a velocity and a time?
      Check the units!
    params_part1_ans4_value: <code>0.8333333333333334</code>
    params_part1_ans4_feedback: 'Hmm, check the units of the resulting answer: v/t.'
    params_part1_ans5_value: <code>-1</code>
    params_part1_ans5_feedback: Hmm, does it make sense to subtract a velocity and
      a time? Check the units!
    params_part1_ans6_value: <code>-1.3</code>
    params_part1_ans6_feedback: Hmm, does it make sense to subtract a velocity and
      a time? Check the units!
---
# {{ params_vars_title }}
{{ params_vars_name }} is traveling on {{ params_vars_vehicle }} at {{ params_v }} {{ params_vars_units }}.

<img src="test1.png">

## Part 1

How far does {{ params_vars_name }} travel in {{ params_t }} seconds, assuming they continue at the same velocity?

<img src="test2.png">

### Answer Section

- {{ params_part1_ans1_value }} {{ params_vars_units}}
- {{ params_part1_ans2_value }} {{ params_vars_units}}
- {{ params_part1_ans3_value }} {{ params_vars_units}}
- {{ params_part1_ans4_value }} {{ params_vars_units}}
- {{ params_part1_ans5_value }} {{ params_vars_units}}
- {{ params_part1_ans6_value }} {{ params_vars_units}}

### pl-submission-panel

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

## Attribution

Problem is from the [OpenStax University Physics Volume 2](https://openstax.org/details/books/university-physics-volume-2) textbook, licensed under the [CC-BY 4.0 license](https://creativecommons.org/licenses/by/4.0/).<br>![Image representing the Creative Commons 4.0 BY license.](https://raw.githubusercontent.com/firasm/bits/master/by.png)