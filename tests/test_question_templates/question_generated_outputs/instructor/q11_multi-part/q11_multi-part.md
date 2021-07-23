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
      name: Maya
      vehicle: a unicycle
      title: Distance travelled
      units: m/s
    v: 5
    t: 6
    part2:
      ans1:
        value: 42
      ans2:
        value: 30
      ans3:
        value: 11
      ans4:
        value: 0.8333333333333334
      ans5:
        value: -1
      ans6:
        value: -1.3
---
# {{ params.vars.title }}
## Rubric

This should be hidden from students until after the deadline.
## Solution

This should never be revealed to students.
## Comments

These are random comments associated with this question.
This part of the question is common to both Parts 1 and 2.

<img src="test1.png" width=400>

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).
![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)