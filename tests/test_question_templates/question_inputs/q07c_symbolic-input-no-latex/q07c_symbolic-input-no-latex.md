---
title: Centripetal Motion
topic: Template
author: Michael Kudla
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
server:
    imports: |
        import random as rd; rd.seed(111)
        import pandas as pd
        import sympy as sp
        import prairielearn as pl
        import problem_bank_helpers as pbh
    generate: |
        data2 = pbh.create_data2()

        # store phrases etc
        data2["params"]["vars"]["title"] = 'Centripetal Motion'

        # Declare math symbols to be used by sympy
        m, v, r = sp.symbols('m v r')

        # Describe the solution equation
        F = m*v**2/r

        # Answer to fill in the blank input stored as JSON.
        data2['correct_answers']['part1_ans'] = pl.to_json(F)

        # Update the data object with a new dict
        data.update(data2)
    prepare: |
        pass
    parse: |
        pass
    grade: |
        pass
part1:
  type: symbolic-input
  latex: false
  pl-customizations:
    label: $F_r = $
    variables: "m, v, r"
    weight: 1
    allow-blank: false
latex:
    preamble: false
    part1:
        question: false
        submission: false
        answer: false
---
# {{ params.vars.title }}

This question is a duplicate of q07a_symbolic-input, demonstrating the ability to disable latex parsing and rendering.

## Question Text

Write the centripetal force $F_r$ in terms of the mass $m$, velocity $v$, and radius $r$.

Note that it may not be necessary to use every variable. Use the following table as a reference for each variable:

| For  | Use   |
|----------|-------|
| $m$  | m  |
| $v$  | v  |
| $r$  | r  |


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
