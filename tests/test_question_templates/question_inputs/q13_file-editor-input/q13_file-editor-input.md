---
title: Python Powers
topic: Template
author: Aidan Murphy
source: original
template_version: 1.0
attribution: standard
partialCredit: true
singleVariant: true
showCorrectAnswer: false
gradingMethod: External
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
- nothing
assets:
autogradeTestFiles:
- ans.py
- setup_code.py
- starter_code.py
- test.py
externalGradingOptions:
  enabled: true
  image: prairielearn/grader-python
  entrypoint: "/python_autograder/run.sh"
server:
    imports: |
        import random as rd
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
## Question Text

<p>
    This question requires you to define a function named <code>{{params.fname}}</code>.<br>
    This function should receive a single numerical input and return the {{params.question}} of this input.<br>
    assume all inputs to the function are valid.<br>
</p>
<p>
    Below are some example uses of the <code>{{params.fname}}</code> function
</p>
<markdown>
    {{params.fname}}({{params.input0}})  # returns {{params.output0}}
    {{params.fname}}({{params.input1}})  # returns {{params.output1}}
    {{params.fname}}({{params.input2}})  # returns {{params.output2}}
</markdown>

### Answer Section
import math

### pl-submission-panel
<pl-external-grader-results></pl-external-grader-results>
<pl-file-preview></pl-file-preview>

### pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.
Please remove this section if it is not application for this question.

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.
