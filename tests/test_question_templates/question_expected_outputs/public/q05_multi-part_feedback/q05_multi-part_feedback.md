---
title: Electric Field and Direction
topic: Template
author: Jake Bobowski
source: 2.6.67
template_version: 1.4
attribution: openstax-physics-vol2
partialCredit: true
singleVariant: false
outcomes:
- undefined
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
    label: $E=$
    allow-blank: false
    show-correct-answer: true
    show-help-text: true
    suffix: $\rm\ N/C$
    weight: 1
part2:
  type: dropdown
  pl-customizations:
    blank: true
    weight: 1
myst:
  substitutions: {}
---
# {{ params.vars.title }}
Two parallel conducting plates ${{params.L}}\textrm{ cm}$ on a side are given equal and opposite charges of magnitude ${{params.q}}\times 10^{ {{params.p}} }\textrm{ C}$.
The plates are ${{params.d}} \textrm{ mm}$ apart.

## Part 1

What is the magnitude of the electric field at the centre of the region between the plates?

### Answer Section

Please enter a numeric value.

## Part 2

What is the direction of the electric field at the centre of the region between the plates?

### Answer Section

- {{ params.part2.ans1.value }}
- {{ params.part2.ans2.value }}
- {{ params.part2.ans3.value }}

### pl-submission-panel

{{ submitted_answers.part1_ans_str }}
{{ feedback.part1_ans }}

### pl-answer-panel

$E=$ {{ correct_answers.part1_ans_str }} $\mathrm{N}/\mathrm{C}$

## Attribution

Problem is from the [OpenStax University Physics Volume 2](https://openstax.org/details/books/university-physics-volume-2) textbook, licensed under the [CC-BY 4.0 license](https://creativecommons.org/licenses/by/4.0/).<br>![Image representing the Creative Commons 4.0 BY license.](https://raw.githubusercontent.com/firasm/bits/master/by.png)