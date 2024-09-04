---
title: Electric Field and Direction
topic: Template
author: Jake Bobowski
source: 2.6.67
template_version: 1.4
attribution: openstax-physics-vol2
partialCredit: true
singleVariant: false
showCorrectAnswer: false
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
assets:
server:
    imports: |
        import random as rd; rd.seed(111)
        import numpy as np
        import pandas as pd
        import problem_bank_helpers as pbh

        # Feedback params
        rtol = 0.03
        errorCheck = 'True'

        feedback_dict = {'vars': ['part1_ans'],
                         'stringData': ['E'],
                         'units': [r'$~\mathrm{N}/\mathrm{C}$']
                         }

    generate: |
        data2 = pbh.create_data2()

        # Sample random numbers
        L = rd.choice(np.linspace(7, 15, num = 9))
        q = rd.choice(np.linspace(1, 9, num = 41))
        p = rd.choice(np.linspace(-10, -6, num = 5))
        d = rd.choice(np.linspace(0.5, 2.5, num = 21))

        # Put these numbers into data['params']
        data2["params"]["L"] = "{:.0f}".format(L)
        data2["params"]["q"] = "{:.1f}".format(q)
        data2["params"]["p"] = "{:.0f}".format(p)
        data2["params"]["d"] = "{:.1f}".format(d)

        # Compute the solutions
        e0 = 8.85e-12 # C^2/N m^2
        E = float((q*10**p/(L/100)**2)/e0) # N/C

        # Put the solutions into data['correct_answers']
        data2['correct_answers']['part1_ans'] = E

        # Write the solutions formatted using scientific notation while keeping 3 sig figs.
        data2['correct_answers']['part1_ans_str'] = pbh.roundp(E, sigfigs=3, format = 'sci')

        # define possible answers

        data2["params"]["part2"]["ans1"]["value"] = 'points towards the negative plate'
        data2["params"]["part2"]["ans1"]["correct"] = True

        data2["params"]["part2"]["ans2"]["value"] = 'points towards the positive plate'
        data2["params"]["part2"]["ans2"]["correct"] = False

        data2["params"]["part2"]["ans3"]["value"] = 'points parallel to the plates'
        data2["params"]["part2"]["ans3"]["correct"] = False

        # Update the data object with a new dict
        data.update(data2)
    prepare: |
        pass
    parse: |
        # Call a function to check if the submitted answers should be re-expressed using scientific notation.
        for i,k in enumerate(feedback_dict['vars']):
            data["submitted_answers"][k + '_str'] = pbh.sigFigCheck(data["submitted_answers"][k], feedback_dict['stringData'][i], feedback_dict['units'][i])
    grade: |
        # Call a function to check for easily-identifiable errors.
        # The syntax is pbh.ErrorCheck(errorCheck, submittedAnswer, correctAnswer, LaTeXsyntax, relativeTolerance)
        # To enable error checking, set check = 'true'.

        for i,k in enumerate(feedback_dict['vars']):
            data["feedback"][k] = pbh.ErrorCheck(errorCheck, data["submitted_answers"][k], data["correct_answers"][k], feedback_dict['stringData'][i], rtol)
part1:
  type: number-input
  pl-customizations:
    rtol: 0.05
    label: $E=$
    allow-blank: false
    show-correct-answer: true
    #rtol: 0.03
    show-help-text: true
    suffix: $\rm\ N/C$
    weight: 1
part2:
  type: dropdown
  pl-customizations:
    blank: true
    weight: 1
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

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.
