---
title: Distance travelled
topic: Template
author: Christina Yang
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
  type: matching
  pl-customizations:
    weight: 1
    blank: 'true'
myst:
  substitutions:
    params_vars_name: Maya
    params_vars_vehicle: a unicycle
    params_vars_title: Distance travelled
    params_vars_units: m/s
    params_v: 5
    params_t: 6
    params_part1_option1_value: true
    params_part1_option2_value: false
    params_part1_statement1_value: 42
    params_part1_statement1_matches: option2
    params_part1_statement2_value: 30
    params_part1_statement2_matches: option1
    params_part1_statement3_value: 11
    params_part1_statement3_matches: option2
    params_part1_statement4_value: 0.8333333333333334
    params_part1_statement4_matches: option2
---
# {{ params_vars_title }}

## Question Text

{{ params_vars_name }} is traveling on {{ params_vars_vehicle }} at {{ params_v }} {{ params_vars_units }}.
How far does {{ params_vars_name }} travel in {{ params_t }} seconds, assuming they continue at the same velocity?

### Answer Section

### pl-submission-panel

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)