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
    params:
      question: 7th power
      num: 7
      fname: warthog
      input0: 8
      output0: 2097152.0
      input1: 9
      output1: 4782969.0
      input2: 4
      output2: 16384.0
      names_for_user:
      - name: x
        description: A random input number
        type: int
      names_from_user:
      - name: warthog
        description: receives a single numerical input, returns its 7th power
        type: function
---
# {{ params.vars.title }}

## Question Text

This question requires you to define a function named `{{params.fname}}`.
This function should receive a single numerical input and return the {{params.question}} of this input.
assume all inputs to the function are valid.

Below are some example uses of the `{{params.fname}}` function:

```python
{{params.fname}}({{params.input0}})  # returns {{params.output0}}
{{params.fname}}({{params.input1}})  # returns {{params.output1}}
{{params.fname}}({{params.input2}})  # returns {{params.output2}}
```

### Answer Section

import math

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)