---
title: Moving and copying files
topic: Template
author: Jonatan Schroeder; Converted by Gavin Kendal-Freedman
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
workspaceFiles:
- file2.txt
- filebad.txt
workspaceTemplates:
- file1.txt.mustache
serverFiles:
- file1.txt
- file2.txt
- filebad.txt
workspaceOptions:
  image: prairielearn/workspace-xtermjs
  port: 8080
  home: /home/student
  gradedFiles:
  - file1.txt
  - file2.txt
  - filebad.txt
  - newdir/file1_new.txt
  - newdir/file2_new.txt
part1:
  type: workspace
myst:
  substitutions:
    params:
      vars:
        title: Moving and copying files
---
# {{ params.vars.title }}

## Question Text

Open the Workspace below and perform the following tasks.

- Create a new directory called `newdir`;
- Move the file `file1.txt` to the directory `newdir`, with the new name `file1_new.txt`;
- Copy the file `file2.txt` to the directory `newdir`, with the new name `file2_new.txt`;
- Delete the file `filebad.txt`.

Once you complete these tasks, click on "Save & Grade" below.

### Answer Section

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)