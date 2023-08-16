---
title: Python Powers
topic: Template
author: UNABLE TO ROUNDTRIP
source: UNABLE TO ROUNDTRIP
template_version: UNABLE TO ROUNDTRIP
attribution: standard
gradingMethod: true
partialCredit: true
singleVariant: true
showCorrectAnswer: false
externalGradingOptions:
  enabled: true
  image: prairielearn/grader-python
  entrypoint: /python_autograder/run.sh
outcomes:
- UNABLE TO ROUNDTRIP
difficulty:
- UNABLE TO ROUNDTRIP
randomization:
- UNABLE TO ROUNDTRIP
taxonomy:
- UNABLE TO ROUNDTRIP
span:
- UNABLE TO ROUNDTRIP
length:
- UNABLE TO ROUNDTRIP
tags:
- nothing
autogradeTestFiles:
- ans.py
- setup_code.py
- starter_code.py
- test.py
server:
  imports: |
    import random as rd; rd.seed(111)
    import math
    import problem_bank_helpers as pbh
  generate: |
    # randomized question
    numbers = list(range(4, 11))
    rd.shuffle(numbers)
    randInt = rd.choice(numbers)
    question_dict = {
        f"{randInt}th power": randInt,
        f"{randInt}th root": 1/randInt
    }
    question_list = list(question_dict.keys())
    question = rd.choice(question_list)

    data["params"]["question"] = question
    data["params"]["num"] = question_dict[question]

    # randomized variable names
    name_list = ["giraffe", "warthog", "dog", "crab"]
    function_name = rd.choice(name_list)
    data["params"]["fname"] = function_name

    # create some example inputs and outputs
    for i in range(3):
        input = numbers.pop(0)
        data["params"]["input" + str(i)] = input
        data["params"]["output" + str(i)] = math.pow(input, question_dict[question])

    # variables detected by autograder
    ## list of variables provided to students
    data["params"]["names_for_user"] = [
        {"name": "x", "description": "A random input number", "type": "int"}
    ]

    ## list of variables/references extracted from student answer
    data["params"]["names_from_user"] = [
        {"name": function_name, "description": f"receives a single numerical input, returns its {question}", "type": "function"}
    ]

    # Start code added automatically by problem_bank_scripts

    # Convert backticks to code blocks/fences in answer choices.
    pbh.backticks_to_code_tags(data2)

    # Update data with data2
    data.update(data2)

    # End code added in by problem bank scripts
  prepare: |
    pass
  parse: |
    pass
  grade: |
    pass
part1:
  type: file-editor
  pl-customizations:
    file-name: user_code.py
    ace-mode: ace/mode/python
    source-file-name: tests/starter_code.py
---
# {{ params.vars.title }}

## Part 1

This question requires you to define a function named {{params.fname}}.
    This function should receive a single numerical input and return the {{params.question}} of this input.
    assume all inputs to the function are valid.


    Below are some example uses of the {{params.fname}} function


    {{params.fname}}({{params.input0}})  # returns {{params.output0}}
    {{params.fname}}({{params.input1}})  # returns {{params.output1}}
    {{params.fname}}({{params.input2}})  # returns {{params.output2}}

### Answer Section 

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

## Rubric

UNABLE TO ROUNDTRIP, Defaulting to 'This should be hidden from students until after the deadline.'

## Solution

UNABLE TO ROUNDTRIP, Defaulting to 'This should never be revealed to students.'.

## Comments

UNABLE TO ROUNDTRIP, Defaulting to 'These are random comments associated with this question.'

