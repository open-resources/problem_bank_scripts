---
title: Distance travelled
topic: Template
author: Firas Moosvi
source: original
template_version: 1.1
attribution: standard
outcomes:
- 6.1.1.0
- 6.1.1.1
difficulty:
- undefined
randomization:
- undefined
taxonomy:
- undefined
tags:
- unknown
assets: null
part1:
  type: number-input
  pl-customizations:
    weight: 1
    allow-blank: true
    label: $d= $
    suffix: m
    comparison: sigfig
    digits: 2
substitutions:
  params:
    vars:
      name: Maya
      vehicle: a unicycle
      title: Distance travelled
      units: m/s
    v: 5
    t: 6
---
# {{ params.vars.title }}
{{ params.vars.name }} is traveling on {{ params.vars.vehicle }} at {{ params.v }} {{ params.vars.units }}.
## Question Text

How far does {{ params.vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

### Answer Section

Please enter in a numeric value in {{ params.vars.units }}.

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)