# Author: Firas Moosvi and Graham Bovett
# Date: 2021-05-09
# This file contains many helper functions that will be used across the question bank project.

from docopt import docopt

## Imports

# Loading and Saving files & others
import pathlib
import sys
import numpy as np
import os
from collections import defaultdict

# Parse Markdown
from markdown_it import MarkdownIt # pip install markdown-it-py 
from mdformat.renderer import MDRenderer # pip install mdformat

# Dealing with YAML
import yaml

def defdict_to_dict(defdict, finaldict):
    """Convert a defaultdict (nested) to a regular dictionary.
        - Answer copied from: https://stackoverflow.com/a/61133504/2217577
    Args:
        defdict (dict): defaultdict
        finaldict (dict): regular dictionary

    Returns:
        dict: Convert to regular dictionary
    """
    # pass in an empty dict for finaldict
    for k, v in defdict.items():
        if isinstance(v, defaultdict):
            # new level created and that is the new value
            finaldict[k] = defdict_to_dict(v, {})
        else:
            finaldict[k] = v
    return finaldict

def rounded(num, digits_after_decimal = 2):
    """Rounds numbers properly to specified digits after decimal place

    Args:
        num (float): Number that is to be rounded
        digits_after_decimal (int, optional): Number of digits to round to. Defaults to 2.

    Returns:
        str: A string that is correctly rounded (you know why it's not a float!)
    """
    """
    This needs to be heavily tested!!
    WARNING: This does not do sig figs yet!
    """

    # Solution attributed to: https://stackoverflow.com/a/53329223

    if type(num) == str:
        return num
    elif type(num) == dict:
        return num
    else:
        from decimal import Decimal, getcontext, ROUND_HALF_UP

        round_context = getcontext()
        round_context.rounding = ROUND_HALF_UP

        tmp = Decimal(num).quantize(Decimal('1.'+'0'*digits_after_decimal))

        return str(tmp)

def split_body_parts(num_parts,body_parts):
    """Parses individual question parts and splits out titles, and content

    Args:
        num_parts (int): An integer corresponding to the number of question parts (from `read_md_problem()`).
        body_parts (dict): A dictionary from `read_md_problem()`.

    Returns:
        body_parts_dict (dict): returns a nested dictionary with title,content,answer keys .
    """
    mdit = MarkdownIt()
    env = {}
    nested_dict = lambda: defaultdict(nested_dict)

    parts_dict = nested_dict()

    for pnum in range(1,num_parts+1):

        part = 'part'+f'{pnum}'
        # Set up tokens by parsing the md file
        tokens = mdit.parse(body_parts[part], env)

        ptt = [i for i,j in enumerate(tokens) if j.tag=='h2']
        parts_dict[part]['title'] = MDRenderer().render(tokens[ptt[0]+1:ptt[1]], mdit.options, env).strip('\n')

        pa = [i for i,j in enumerate(tokens) if j.tag=='h3']
        parts_dict[part]['answer']['title'] = MDRenderer().render(tokens[pa[0]+1:pa[1]], mdit.options, env)

        parts_dict[part]['content'] = MDRenderer().render(tokens[ptt[1]+1:pa[0]], mdit.options, env)
        parts_dict[part]['answer']['content'] = MDRenderer().render(tokens[pa[1]+1:], mdit.options, env)

    return defdict_to_dict(parts_dict,{})

def read_md_problem(filepath):
    """Reads a MystMarkdown problem file and returns a dictionary of the header and body

    Args:
        filepath (str): Path of file to read.

    Returns:
        dict: In this dictionary there are three keys containing useful portions of the parsed md file: 
            - `header` - Header of the problem file (nested dictionary).
            - `body_parts` - Body text of the problem file (nested dictionary).
            - `num_parts` - Number of parts in the problem (integer).
    """

    mdtext = pathlib.Path(filepath).read_text()

    # Deal with YAML header
    header_text = mdtext.rsplit('---\n')[1]
    header = yaml.safe_load('---\n' + header_text)

    # Deal with Markdown Body
    body = mdtext.rsplit('---\n')[2]
    
    # Set up the markdown parser
    # to be honest, not fully sure what's going on here, see this issue: https://github.com/executablebooks/markdown-it-py/issues/164

    mdit = MarkdownIt()
    env = {}

    # Set up tokens by parsing the md file
    tokens = mdit.parse(body, env)

    blocks = {}

    block_count = 0

    num_titles = 0

    for x,t in enumerate(tokens):

        if t.tag == 'h1' and t.nesting == 1: # title
            # oh boy. this is going to break and it will be your fault firas.
            blocks['title'] = [x,x+3]
            num_titles += 1

        elif t.tag == 'h2' and t.nesting == 1:
            block_count += 1

            if block_count == 1:
                blocks['block{0}'.format(block_count)] = [x,]
            else:
                blocks['block{0}'.format(block_count-1)].append(x)
                blocks['block{0}'.format(block_count)] = [x,]

    # Add -1 to the end of the last block
    blocks['block{0}'.format(block_count)].append(len(tokens))

    # Assert statements (turn into tests!)
    assert num_titles == 1, "I see {0} Level 1 Headers (#) in this file, there should only be one!".format(num_titles)
    assert block_count >= 1, "I see {0} Level 2 Headers (##) in this file, there should be at least 1".format(block_count -1)

    # Add the end of the title block; # small hack
    #blocks['title'].append(blocks['block1'][0])

    # Get the preamble before the parts start
    blocks['preamble'] = [blocks['title'][1],blocks['block1'][0]]

    ## Process the blocks into markdown

    body_parts = {}

    part_counter = 0

    for k,v in blocks.items():

        rendered_part = MDRenderer().render(tokens[v[0]:v[1]], mdit.options, env)

        if k == 'title':
            body_parts['title'] = rendered_part
        
        elif k == 'preamble':
            body_parts['preamble'] = rendered_part

        elif 'Rubric' in rendered_part:
            body_parts['Rubric'] = rendered_part

        elif 'Solution' in rendered_part:
            body_parts['Solution'] = rendered_part

        elif 'Comments' in rendered_part:
            body_parts['Comments'] = rendered_part

        else:
            part_counter +=1
            body_parts['part{0}'.format(part_counter)] = rendered_part
    
    return defdict_to_dict({'header': header,
            'body_parts': body_parts,
            'num_parts': part_counter,
            'body_parts_split': split_body_parts(part_counter,body_parts) },{})

def dict_to_md(md_dict, remove_keys = [None,]):
    """ Takes a nested dictionary (e.g. output of read_md_problem()) and returns a multi-line string  that can be written to a file (after removing specified keys).   
    Args:
        md_dict (dict): A nested dictionary, for e.g. the output of `read_md_problem()`
        remove_keys (list, optional): Any keys to remove from the dictionary, for instance solutions. Defaults to [None,].

    Returns:
        str: A multi-line string that can be written to a file.
    """

    md_string = ""

    for k,v in md_dict.items():
        if k in remove_keys:
            continue
        else:
            md_string += md_dict[k]

    return md_string