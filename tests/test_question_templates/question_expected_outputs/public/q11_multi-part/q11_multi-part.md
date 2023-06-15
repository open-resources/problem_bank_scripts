---
title: Multi-part Question
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
- test1.png
- test2.png
part1:
  type: number-input
  pl-customizations:
    rtol: 0.05
    weight: 1
    allow-blank: true
    label: $d= $
    suffix: m
    comparison: sigfig
    digits: 2
part2:
  type: multiple-choice
  pl-customizations:
    weight: 1
myst:
  substitutions:
    params_vars_name: Mateo
    params_vars_vehicle: ice skates
    params_vars_title: Distance travelled
    params_vars_units: m/s
    params_v: 2
    params_t: 8
    params_part2_ans1_value: 42
    params_part2_ans2_value: 16
    params_part2_ans3_value: 10
    params_part2_ans4_value: 0.25
    params_part2_ans5_value: -6
    params_part2_ans6_value: -7.800000000000001
---
# {{ params_vars_title }}
This part of the question is common to both Parts 1 and 2.

<img src="test1.png" width=400>

## Part 1

{{ params_vars_name }} is traveling on {{ params_vars_vehicle }} at {{ params_v }} {{ params_vars_units }}.
How far does {{ vars.name }} travel in {{ params_t }} seconds, assuming they continue at the same velocity?

<img src="test2.png" width=400>

### Answer Section

Please enter in a numeric value in {{ params_vars_units }}.

### pl-submission-panel

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

## Part 2

{{ params_vars_name }} is traveling on {{ params_vars_vehicle }} at {{ params_v }} {{ params_vars_units }}.
How far does {{ params_vars_name }} travel in {{ params_t }} seconds, assuming they continue at the same velocity?

### Answer Section

- {{ params_part2_ans1_value}} {{ params_vars_units}}
- {{ params_part2_ans2_value}} {{ params_vars_units}}
- {{ params_part2_ans3_value}} {{ params_vars_units}}
- {{ params_part2_ans4_value}} {{ params_vars_units}}
- {{ params_part2_ans5_value}} {{ params_vars_units}}
- {{ params_part2_ans6_value}} {{ params_vars_units}}

### pl-submission-panel

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)