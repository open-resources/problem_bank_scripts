---
title: Code Output
topic: Template
author: Gavin Kendal-Freedman
source: original
template_version: 1.0
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
  type: string-input
  pl-customizations:
    answers-name: ans
    display: block
    placeholder: '...'
    ignore-case: true
myst:
  substitutions:
    params:
      vars:
        title: Code Output
        a: 2
        stringname: love
      part1: {}
---
# {{ params.vars.title }}

## Question Text

For the following python code snippet, enter below the resulting string:

```python
a = "{{ params.vars.stringname }}" * {{ params.vars.a }}
```

### Answer Section

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)