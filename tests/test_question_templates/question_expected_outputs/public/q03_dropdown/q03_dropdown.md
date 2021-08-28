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
  type: dropdown
  pl-customizations:
    weight: 1
    blank: 'true'
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
      ans1:
        value: 42
      ans2:
        value: 30
      ans3:
        value: 11
      ans4:
        value: 0.8333333333333334
      ans5:
        value: -1
      ans6:
        value: -1.3
---
# {{ params.vars.title }}
## Question Text

{{ params.vars.name }} is traveling on {{ params.vars.vehicle }} at {{ params.v }} {{ params.vars.units }}.
How far does {{ params.vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

### Answer Section

- {{ params.part1.ans1}} {{ params.vars.units}}
- {{ params.part1.ans2}} {{ params.vars.units}}
- {{ params.part1.ans3}} {{ params.vars.units}}
- {{ params.part1.ans4}} {{ params.vars.units}}
- {{ params.part1.ans5}} {{ params.vars.units}}

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)