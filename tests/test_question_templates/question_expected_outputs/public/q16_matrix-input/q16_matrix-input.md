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
    params:
      title: Matrix Input
      matrixA: null
---
# {{ params.vars.title }}
Given the following matrix, please return the inverse of the matrix.

<pl-matrix-latex params-name="matrixA"></pl-matrix-latex>

## Part 1

Please write your answer as a matrix component input.

### Answer Section

## Part 2

Please write your answer as a matrix input in python or matlab format.

### Answer Section

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)