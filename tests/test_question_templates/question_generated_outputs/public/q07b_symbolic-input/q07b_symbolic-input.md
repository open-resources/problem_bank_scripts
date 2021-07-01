---
title: Symbolic Input 2 - Trig
topic: Template
author: Michael Kudla
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
server:
  imports: |
    import random;random.seed(111)
    import pandas as pd
    import sympy as sp
    import prairielearn as pl
    import problem_bank_helpers as pbh
  generate: |
    data2 = pbh.create_data2()

    # define or load names/items/objects
    names = pd.read_csv("data/names.csv")["Names"].tolist()
    vehicles = pd.read_csv("data/vehicles.csv")["Vehicles"].tolist()

    # store phrases etc
    data2["params"]["vars"]["title"] = 'Symbolic Input 2 - Trig'
    data2["params"]["vars"]["name"] = random.choice(names)
    data2["params"]["vars"]["vehicle"] = random.choice(vehicles)

    # Declare math symbols to be used by sympy
    mu_s, g , theta = sp.symbols('mu_s g theta')

    # Describe the solution equation
    amax = g*(mu_s*sp.cos(theta) - sp.sin(theta))

    # Answer to fill in the blank input -- must be stored as JSON.
    data2['correct_answers']['part1_ans'] = pl.to_json(amax)

    # Update the data object with a new dict
    data.update(data2)
  prepare: 'pass

    '
  parse: 'pass

    '
  grade: 'pass

    '
part1:
  type: symbolic-input
  label: $F_r =$
  pl-customizations:
    variables: mu_s, g , theta
    weight: 1
    allow-blank: true
substitutions:
  params:
    vars:
      title: Symbolic Input 2 - Trig
      name: Maya
      vehicle: van
  correct_answers:
    part1_ans:
      _type: sympy
      _value: g*(mu_s*cos(theta) - sin(theta))
      _variables:
      - g
      - theta
      - mu_s
---
# {{ params.vars.title }}

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).
![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)