---
title: Distance travelled
topic: Template
author: Christina Yang
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
  type: matching
  pl-customizations:
    weight: 1
    blank: 'true'
myst:
  substitutions:
    params:
      vars:
        name: Maya
        vehicle: a unicycle
        title: Distance travelled
        units: m/s
      v: 5
      t: 6
      part1:
        option1:
          value: true
          name: 'True'
        option2:
          value: false
          name: 'False'
        statement1:
          value: 42
          matches: 'False'
        statement2:
          value: 30
          matches: 'True'
        statement3:
          value: 11
          matches: 'False'
        statement4:
          value: 0.833
          matches: 'False'
---
# {{ params.vars.title }}

## Question Text

{{ params.vars.name }} is traveling on {{ params.vars.vehicle }} at {{ params.v }} {{ params.vars.units }}.
How far does {{ params.vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

### Answer Section

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)