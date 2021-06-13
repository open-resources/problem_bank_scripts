# Author: Firas Moosvi and Graham Bovett
# Date: 2021-05-09
# This file contains many helper functions that will be used across the question bank project.

from docopt import docopt

# Imports
## Loading and Saving files & others
import uuid
import json
from . import prairielearn as pl
import pathlib
import sys
import numpy as np
import os
from collections import defaultdict
from shutil import copy2
import re
import codecs

## Parse Markdown
from markdown_it import MarkdownIt # pip install markdown-it-py 
from mdformat.renderer import MDRenderer # pip install mdformat

## Dealing with YAML
import yaml

# Start of reading/parsing functions

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

        try:
            parts_dict[part]['answer']['title'] = codecs.unicode_escape_decode(MDRenderer().render(tokens[pa[0]+1:pa[1]], mdit.options, env))[0]
        except IndexError:
            print("Check the heading levels, is there one that doesn't belong? Or is the heading level incorrect? For e.g., it should be ### Answer Section (this is not necessarily where the issue is).")
            raise

        parts_dict[part]['content'] = codecs.unicode_escape_decode(MDRenderer().render(tokens[ptt[1]+1:pa[0]], mdit.options, env))[0]
        parts_dict[part]['answer']['content'] = codecs.unicode_escape_decode(MDRenderer().render(tokens[pa[1]+1:], mdit.options, env))[0]

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

    mdtext = pathlib.Path(filepath).read_text(encoding='utf8')

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

        rendered_part = codecs.unicode_escape_decode(MDRenderer().render(tokens[v[0]:v[1]], mdit.options, env))[0]

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

    md_dict = defdict_to_dict(md_dict,{})

    for k,v in md_dict.items():
        if k in remove_keys:
            continue
        else:
            md_string += md_dict[k]

    return md_string

## Functions from md-to-pl

def write_info_json(output_path, parsed_question):
    """
    Args:
        output_path (Path): [description]
        parsed_question (dict]): [description]
    """

    pathlib.Path(output_path / 'info.json').write_text("""{
            "uuid": \"""" + str(uuid.uuid4()) + """\",
            "title": \"""" + parsed_question['header']['title'] + """",
            "topic": \"""" + parsed_question['header']['topic'] + """",
            "tags":  """ + json.dumps(parsed_question['header']['tags']) + """,
            "type": "v3"
        }""",encoding='utf8')

def write_server_py(output_path,parsed_question):
    """
    Args:
        output_path ([type]): [description]
        parsed_question ([type]): [description]
    """
    
    try:
        imp, func = parsed_question['header']['server'].split('# Start problem code')
    except:
        raise

    func = func.replace('read_csv("','read_csv(data["options"]["client_files_course_path"]+"/')
    func = func.replace('\n','\n    ')

    (output_path / "server.py").write_text(imp+'def generate(data):'+func,encoding='utf8')

def process_multiple_choice(part_name,parsed_question, data_dict):
    """Processes markdown format multiple-choice questions and returns PL HTML
    Args:
        output_path (Path): [description]
        parsed_question (dict): [description]
        data_dict (dict)
    
    Returns:
        str: Multiple choice question is returned as a string with PL-compliant syntax.
    """

    html = f"""<pl-question-panel>\n<markdown>{parsed_question['body_parts_split'][part_name]['content']}</markdown>\n</pl-question-panel>\n\n"""
    
    pl_customizations = " ".join([f'{k} = "{v}"' for k,v in parsed_question['header'][part_name]['pl-customizations'].items()]) # PL-customizations
    html += f"""<pl-multiple-choice answers-name="{part_name}_ans" {pl_customizations} >\n"""

    if data_dict['params'][f'vars']['units']:
        units = f"|@ params.vars.units @|"
    else:
        units = ''

    for a in data_dict['params'][f'{part_name}'].keys():
        if 'ans' in a:
            html += f"\t<pl-answer correct= |@ params.{part_name}.{a}.correct @| > |@ params.{part_name}.{a}.value @| {units} </pl-answer>\n"

    html += '</pl-multiple-choice>\n' 

    return replace_tags(html)

def process_dropdown(part_name,parsed_question, data_dict):
    """Processes markdown format dropdown questions and returns PL HTML

    Args:
        part_name (string): Name of the question part being processed (e.g., part1, part2, etc...)
        parsed_question (dict): Dictionary of the MD-parsed question (output of `read_md_problem`)
        data_dict (dict): Dictionary of the `data` dict created after running server.py using `exec()`

    Returns:
        html: A string of HTML that is part of the final PL question.html file.
    """
    html = process_multiple_choice(part_name,parsed_question, data_dict).replace('-multiple-choice','-dropdown')
    return html
    
def process_number_input(part_name,parsed_question, data_dict):
    """Processes markdown format number-input questions and returns PL HTML

    Args:
        part_name (string): Name of the question part being processed (e.g., part1, part2, etc...)
        parsed_question (dict): Dictionary of the MD-parsed question (output of `read_md_problem`)
        data_dict (dict): Dictionary of the `data` dict created after running server.py using `exec()`

    Returns:
        html: A string of HTML that is part of the final PL question.html file.
    """

    html = f"""<pl-question-panel>\n\t<markdown>{parsed_question['body_parts_split'][part_name]['content']}\t</markdown>\n</pl-question-panel>\n\n"""
    
    pl_customizations = " ".join([f'{k} = "{v}"' for k,v in parsed_question['header'][part_name]['pl-customizations'].items()]) # PL-customizations
    html += f"""<pl-number-input answers-name="{part_name}_ans" {pl_customizations} ></pl-number-input>\n"""

    return replace_tags(html)

def process_checkbox(part_name,parsed_question, data_dict):
    """Processes markdown format checkbox (select all that apply) questions and returns PL HTML

    Args:
        part_name (string): Name of the question part being processed (e.g., part1, part2, etc...)
        parsed_question (dict): Dictionary of the MD-parsed question (output of `read_md_problem`)
        data_dict (dict): Dictionary of the `data` dict created after running server.py using `exec()`

    Returns:
        html: A string of HTML that is part of the final PL question.html file.
    """
    # start with the MCQ version and then...change things for checkbox questions
    html = process_multiple_choice(part_name,parsed_question, data_dict).replace('-multiple-choice','-checkbox')
    return html

def process_symbolic_input(part_name,parsed_question, data_dict):
    """Processes markdown format symbolic questions and returns PL HTML

    Args:
        part_name (string): Name of the question part being processed (e.g., part1, part2, etc...)
        parsed_question (dict): Dictionary of the MD-parsed question (output of `read_md_problem`)
        data_dict (dict): Dictionary of the `data` dict created after running server.py using `exec()`

    Returns:
        html: A string of HTML that is part of the final PL question.html file.
    """

    html = f"""<pl-question-panel>\n\t<markdown>{parsed_question['body_parts_split'][part_name]['content']}\t</markdown>\n</pl-question-panel>\n\n"""
    
    pl_customizations = " ".join([f'{k} = "{v}"' for k,v in parsed_question['header'][part_name]['pl-customizations'].items()]) # PL-customizations
    html += f"""<pl-symbolic-input answers-name="{part_name}_ans" {pl_customizations} ></pl-symbolic-input>\n"""

    return replace_tags(html).replace('\\\\','\\')

def replace_tags(string):
    """Takes in a string with tags: |@ and @| and returns {{ and }} respectively. This is because Python strings can't have double curly braces.

    Args:
        string (str): String to be processed, can be multi-line.

    Returns:
        string (str): returns string with tags replaced with curly braces.
    """
    return string.replace('|@','{{').replace('@|','}}')

def process_attribution(source):
    """Takes in a string and returns the HTML for the attribution

    Args:
        source (string): One of a set of pre-defined values corresponding to a particular attribution.

    Returns:
        string (str): returns the html of the attribution
    """
    try:
        if 'openstax-physics-vol1' in source:
            attribution_text = "![Image representing the Creative Commons 4.0 BY license.](https://i.creativecommons.org/l/by/4.0/88x31.png) Problem is from the [OpenStax University Physics Volume 1](https://openstax.org/details/books/university-physics-volume-1) textbook, licensed under the [CC-BY 4.0 license](https://creativecommons.org/licenses/by/4.0/)."

        elif 'openstax-physics-vol2' in source:
            attribution_text = "![Image representing the Creative Commons 4.0 BY license.](https://i.creativecommons.org/l/by/4.0/88x31.png) Problem is from the [OpenStax University Physics Volume 2](https://openstax.org/details/books/university-physics-volume-2) textbook, licensed under the [CC-BY 4.0 license](https://creativecommons.org/licenses/by/4.0/)."

        elif 'ubc-mech2' in source:
            raise NotImplementedError

        elif 'standard' in source:
            attribution_text = "![Image representing the Creative Commons 4.0 BY-NC-SA license.](https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc-sa.png) Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/)."
    
        return attribution_text
    
    except TypeError:
        print("You probably need to update the template, the 'attribution' key seems to be missing.")

def process_question(input_file, output_path):

    try:
        input_file = pathlib.Path(input_file)
    except:
        print("File does not exist.")
        raise

    output_path = pathlib.Path(output_path)

    # Parse the MD file
    parsed_q = read_md_problem(input_file)

    # Create output dir if it doesn't exist
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

    ############### Start Sketchiest Part
    # Run the python code
    try:
        exec(parsed_q['header']['server'].split('# Update the data object with a new dict')[0],globals())
    except ModuleNotFoundError:
        # AWFUL AWFUL hack because of the prairielearn.py file
        exec(parsed_q['header']['server'].replace('import prairielearn as pl','from . import prairielearn as pl').split('# Update the data object with a new dict')[0],globals())
    ############### End Sketchiest Part

    # Write info.json file
    write_info_json(output_path, parsed_q)

    # Question Preamble
    if parsed_q['body_parts']['preamble']:
        question_html = f"{parsed_q['body_parts']['preamble']}\n\n"
    else:
        question_html = f""

    ## Single part questions
    if parsed_q['num_parts'] == 1:
        q_type = parsed_q['header']['part1']['type']
        if 'multiple-choice' in q_type:
            question_html += process_multiple_choice('part1',parsed_q,data2)
        elif 'number-input' in q_type:
            question_html += process_number_input('part1',parsed_q,data2)
        elif 'checkbox' in q_type:
            question_html += process_checkbox('part1',parsed_q,data2)
        elif 'symbolic-input' in q_type:
            question_html += process_symbolic_input('part1',parsed_q,data2)
        elif 'dropdown' in q_type:
            question_html += process_dropdown('part1',parsed_q,data2)
        else:
            raise NotImplementedError(f"This question type ({q_type}) is not yet implemented.")

    ##### Multi part
    else:
        for pnum in range(1, parsed_q['num_parts'] + 1):
            part = 'part'+f'{pnum}'
            q_type = parsed_q['header'][part]['type']

            question_html += f"""<div class="card my-2">
<div class="card-header">{parsed_q['body_parts_split'][part]['title']}</div>\n
<div class="card-body">\n\n"""

            if 'multiple-choice' in q_type:                
                question_html += f"{process_multiple_choice(part,parsed_q,data2)}"  
            elif 'number-input' in q_type:
                question_html += f"{process_number_input(part,parsed_q,data2)}"
            elif 'checkbox' in q_type:
                question_html += process_checkbox(part,parsed_q,data2)
            elif 'symbolic-input' in q_type:
                question_html += process_symbolic_input(part,parsed_q,data2)
            elif 'dropdown' in q_type:
                question_html += process_dropdown(part,parsed_q,data2)
            else:
                raise NotImplementedError(f"This question type ({q_type}) is not yet implemented.")

            question_html += "</div>\n</div>\n\n\n"

    # Add Attribution
    question_html += f"\n\n<markdown>---\n{process_attribution(parsed_q['header'].get('attribution'))}\n</markdown>"

    # Final pre-processing
    question_html = pl_image_path(question_html)

    # Write question.html file
    (output_path / "question.html").write_text(question_html,encoding='utf8') #,encoding='raw_unicode_escape')

    ### TODO solve the issue with the latex escape sequences, this is a workaround
    # with open((output_path / "question.html"), "w") as qfile:
    #     print(f"{question_html}", file=qfile)

    # Write server.py file
    write_server_py(output_path,parsed_q)

    # Move image assets
    files_to_copy = parsed_q['header'].get('assets')
    if files_to_copy:
        pl_path =  output_path / "clientFilesQuestion"
        pl_path.mkdir(parents=True, exist_ok=True)
        [copy2(input_file.parent / fl, pl_path / fl) for fl in files_to_copy]

def pl_image_path(html):

    """Adds `clientFilesQuestion` directory before the path automatically
    """

    # If image files are included as markdown format, add clientFilesQuestion
    res = re.subn("\((.*\.png)\)",'(clientFilesQuestion/\\1)',html)

    # If image files are included as html format, add clientFilesQuestion
    res = re.subn(r"src=\"(.*\.png)",
              "src=\"clientFilesQuestion/\\1",res[0]) # works


    return res[0]


