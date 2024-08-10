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
assets: null
autogradeTestFiles:
- ans.py
- setup_code.py
- starter_code.py
- test.py
externalGradingOptions:
  enabled: true
  image: prairielearn/grader-python
  entrypoint: /python_autograder/run.sh
part1:
  type: file-editor
  pl-customizations:
    file-name: user_code.py
    ace-mode: ace/mode/python
    source-file-name: tests/starter_code.py
myst:
  substitutions:
    params_question: 7th power
    params_num: 7
    params_fname: warthog
    params_input0: 8
    params_output0: 2097152.0
    params_input1: 9
    params_output1: 4782969.0
    params_input2: 4
    params_output2: 16384.0
    params_names_for_user:
    - name: x
      description: A random input number
      type: int
    params_names_from_user:
    - name: warthog
      description: receives a single numerical input, returns its 7th power
      type: function
---
# {{ params.vars.title }}

## Question Text

<p>
    This question requires you to define a function named <code>{{params_fname}}</code>.<br>
    This function should receive a single numerical input and return the {{params_question}} of this input.<br>
    assume all inputs to the function are valid.<br>
</p>
<p>
    Below are some example uses of the <code>{{params_fname}}</code> function
</p>
<markdown>
    {{params_fname}}({{params_input0}})  # returns {{params_output0}}
    {{params_fname}}({{params_input1}})  # returns {{params_output1}}
    {{params_fname}}({{params_input2}})  # returns {{params_output2}}
</markdown>

### Answer Section

import math

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)