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
  type: dropdown
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
    params_part1_ans1_value: 42
    params_part1_ans1_feedback: This is a random number, you probably selected this
      choice by mistake! Try again please!
    params_part1_ans2_value: 30
    params_part1_ans2_feedback: Great! You got it.
    params_part1_ans3_value: 11
    params_part1_ans3_feedback: Hmm, does it make sense to add a velocity and a time?
      Check the units!
    params_part1_ans4_value: 0.833
    params_part1_ans4_feedback: 'Hmm, check the units of the resulting answer: v/t.'
    params_part1_ans5_value: -1
    params_part1_ans5_feedback: Hmm, does it make sense to subtract a velocity and
      a time? Check the units!
    params_part1_ans6_value: -1.3
    params_part1_ans6_feedback: Hmm, does it make sense to subtract a velocity and
      a time? Check the units!
---
# {{ params_vars_title }}

## Question Text

{{ params_vars_name }} is traveling on {{ params_vars_vehicle }} at {{ params_v }} {{ params_vars_units }}.
How far does {{ params_vars_name }} travel in {{ params_t }} seconds, assuming they continue at the same velocity?

### Answer Section

- {{ params.part1.ans1}} {{ params_vars_units}}
- {{ params.part1.ans2}} {{ params_vars_units}}
- {{ params.part1.ans3}} {{ params_vars_units}}
- {{ params.part1.ans4}} {{ params_vars_units}}
- {{ params.part1.ans5}} {{ params_vars_units}}

### pl-submission-panel

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)