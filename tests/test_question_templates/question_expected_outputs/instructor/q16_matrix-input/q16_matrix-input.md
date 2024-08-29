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
server:
  imports: |
    import numpy as np
    import problem_bank_helpers as pbh
    import prairielearn as pl
  generate: |
    data2 = pbh.create_data2()
    data2["params"]["title"] = "Matrix Input"

    matrix = np.random.random((2,2))
    inv_matrix = np.linalg.inv(matrix)

    # store phrases, info etc
    data2["params"]["matrixA"] = pl.to_json(matrix)

    # store the correct answers
    data2["correct_answers"]["part1_ans"] = pl.to_json(inv_matrix)
    data2["correct_answers"]["part2_ans"] = pl.to_json(inv_matrix)

    data.update(data2)
  prepare: 'pass

    '
  parse: 'pass

    '
  grade: 'pass

    '
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
    correct_answers:
      part1_ans: null
      part2_ans: null

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

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)