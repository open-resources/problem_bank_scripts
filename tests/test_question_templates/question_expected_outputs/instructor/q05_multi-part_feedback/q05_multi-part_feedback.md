---
title: Electric Field and Direction
topic: Template
author: Jake Bobowski
source: 2.6.67
template_version: 1.1
attribution: openstax-physics-vol2
outcomes:
- undefined
difficulty:
- undefined
randomization:
- undefined
taxonomy:
- undefined
tags:
- unknown
assets: null
part1:
  type: number-input
  pl-customizations:
    label: $E=$
    allow-blank: false
    show-correct-answer: true
    comparison: relabs
    rtol: 0.03
    atol: 0
    show-help-text: true
    suffix: $\rm\ N/C$
    weight: 1
part2:
  type: dropdown
  pl-customizations:
    blank: true
    weight: 1
substitutions:
  params:
    L: '10'
    q: '5.0'
    p: '-7'
    d: '1.1'
    part2:
      ans1:
        value: points towards the negative plate
      ans2:
        value: points towards the positive plate
      ans3:
        value: points parallel to the plates
---
# {{ params.vars.title }}
## Rubric

This should be hidden from students until after the deadline.
## Solution

This should never be revealed to students.
## Comments

These are random comments associated with this question.
Two parallel conducting plates ${{params.L}}\textrm{ cm}$ on a side are given equal and opposite charges of magnitude ${{params.q}}\times 10^{ {{params.p}} }\textrm{ C}$.
The plates are ${{params.d}} \textrm{ mm}$ apart.

## Attribution

Problem is from the [OpenStax University Physics Volume 2](https://openstax.org/details/books/university-physics-volume-2) textbook, licensed under the [CC-BY 4.0 license](https://creativecommons.org/licenses/by/4.0/).
![Image representing the Creative Commons 4.0 BY license.](https://raw.githubusercontent.com/firasm/bits/master/by.png)