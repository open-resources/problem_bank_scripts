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
assets: null
part1:
  type: number-input
  pl-customizations:
    rtol: 0.05
    weight: 1
    allow-blank: true
    label: $d= $
    suffix: m
part2:
  type: number-input
  pl-customizations:
    rtol: 0.05
    weight: 1
    allow-blank: true
    label: $d= $
    suffix: m
myst:
  substitutions:
    params_vars_name: Maya
    params_vars_vehicle: a unicycle
    params_vars_title: Distance travelled
    params_vars_units: m/s
    params_v: 5
    params_t: 6
---
# {{ params_vars_title }}
{{ params_vars_name }} is traveling on {{ params_vars_vehicle }} at {{ params_v }} {{ params_vars_units }}.

## Part 1

How far does {{ params_vars_name }} travel in {{ params_t }} seconds, assuming they continue at the same velocity?

### Answer Section

Please enter in a numeric value in {{ params_vars_units }}.

### pl-submission-panel

{{ feedback.part1_ans }}

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

## Part 2

How far does {{ params_vars_name }} travel in {{ params_t }} seconds, assuming they continue at the same velocity?

### Answer Section

Please enter in a numeric value in {{ params_vars_units }}.

### pl-submission-panel

{{ feedback.part1_ans }}

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)