---
title: Vectors and Scalars
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
server:
  imports: |
    import random
    import pandas as pd
    import problem_bank_helpers as pbh
  generate: "data2 = pbh.create_data2()\n\n# define or load names/items/objects\n\
    names = pd.read_csv(\"data/names.csv\")[\"Names\"].tolist()\n\n# store phrases\
    \ etc\ndata2[\"params\"][\"vars\"][\"title\"] = 'Vectors and Scalars'\ndata2[\"\
    params\"][\"vars\"][\"name\"] = random.choice(names)\n\n# define useful variables/lists\n\
    vectors = [\"displacement\", \"velocity\", \"acceleration\", \"momentum\", \"\
    force\", \"lift\", \"drag\", \"thurst\", \"weight\"]\nscalars = [\"length\", \"\
    area\", \"volume\", \"mass\", \"density\", \"pressure\", \"temperature\", \"energy\"\
    , \"entropy\", \"work\", \"power\"]\n\n# Randomly select 2,3,4 scalars and shuffle\
    \ the lists\ntotal_choices = 6\nnum_scalars = random.choice([2,3,4])\nnum_vectors\
    \ = total_choices - num_scalars\nselect = random.choice([\"vectors\",\"scalars\"\
    ])\n\ndata2[\"params\"][\"choice\"] = select\n\n# Create ans_choices\nans_choices\
    \ = [\"ans{0}\".format(i+1) for i in range(total_choices)]\n\nrandom.shuffle(scalars)\n\
    random.shuffle(vectors)\n\n# define possible answers\nif select == \"vectors\"\
    :\n    for i in range(num_vectors):\n        choice = ans_choices.pop(0)\n   \
    \     data2[\"params\"][\"part1\"][choice][\"value\"] = vectors.pop()\n      \
    \  data2[\"params\"][\"part1\"][choice][\"correct\"] = True\n\n    for i in range(num_scalars):\n\
    \        choice = ans_choices.pop(0)\n        data2[\"params\"][\"part1\"][choice][\"\
    value\"] = scalars.pop()\n        data2[\"params\"][\"part1\"][choice][\"correct\"\
    ] = False\n\nelif select == \"scalars\":\n    for i in range(num_scalars):\n \
    \       choice = ans_choices.pop(0)\n        data2[\"params\"][\"part1\"][choice][\"\
    value\"] = scalars.pop()\n        data2[\"params\"][\"part1\"][choice][\"correct\"\
    ] = True\n        \n    for i in range(num_vectors):\n        choice = ans_choices.pop(0)\n\
    \        data2[\"params\"][\"part1\"][choice][\"value\"] = vectors.pop()\n   \
    \     data2[\"params\"][\"part1\"][choice][\"correct\"] = False\n\n# Update the\
    \ data object with a new dict\ndata.update(data2)\n"
  prepare: 'pass

    '
  parse: 'pass

    '
  grade: 'pass

    '
part1:
  type: checkbox
  pl-customizations:
    weight: 1
    partial-credit: true
    partial-credit-method: EDC
substitutions:
  params:
    vars:
      title: Vectors and Scalars
      name: Maya
    choice: scalars
    part1:
      ans1:
        value: density
        correct: true
      ans2:
        value: area
        correct: true
      ans3:
        value: power
        correct: true
      ans4:
        value: work
        correct: true
      ans5:
        value: velocity
        correct: false
      ans6:
        value: momentum
        correct: false
---
# {{ params.vars.title }}

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).
![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)