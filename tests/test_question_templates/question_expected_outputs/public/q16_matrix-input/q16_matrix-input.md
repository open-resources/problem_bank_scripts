---
title: Matrix Input
topic: Template
author: Gavin Kendal-Freedman
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
  type: matrix-component-input
  pl-customizations:
    weight: 1
    allow-fractions: 'false'
    label: $A^{-1}$
    comparison: decdig
part2:
  type: matrix-input
  pl-customizations:
    weight: 1
    allow-complex: 'false'
    label: $A^{-1}$
    comparison: decdig
myst:
  substitutions:
    params_title: Matrix Input
    params_matrixA: null
---
# {{ params.vars.title }}
Given the following matrix, please return the inverse of the matrix.

<pl-matrix-latex params-name="matrixA"></pl-matrix-latex>

## Part 1

Please write your answer as a matrix component input.

### Answer Section

### pl-submission-panel

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

## Part 2

Please write your answer as a matrix input in python or matlab format.

### Answer Section

### pl-submission-panel

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)