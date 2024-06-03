# Author: Firas Moosvi and Graham Bovett
# Date: 2021-05-09
# This file contains many helper functions that will be used across the question bank project.

from docopt import docopt

# Imports
## Loading and Saving files & others
import uuid
import json
import pathlib
import os
from collections import defaultdict
from collections.abc import Callable
from shutil import copy2, rmtree
import re
import codecs
import importlib.util
import problem_bank_helpers as pbh
import pandas as pd
import warnings

## Parse Markdown
import markdown_it
import mdformat

## Dealing with YAML
import yaml

## Loading files : https://stackoverflow.com/a/60687710
import importlib.resources

## Roundtrip PL questions back to OPB MD
import ast
import inspect
import textwrap
import bs4
from bs4 import BeautifulSoup

## Topic Validation

path = pathlib.Path().resolve().as_posix()
topics = {"Template": "000.Template"}  # Start with special cased topics

try:
    subjects = [path.split("instructor_")[1].split("_bank")[0]]
except:
    subjects = ["physics", "datascience", "stats"]

for subject in subjects:
    url = f"https://raw.githubusercontent.com/open-resources/learning_outcomes/main/outputs_csv/LO_{subject}.csv"
    learning_outcomes = pd.read_csv(url)
    topics |= learning_outcomes[["Topic", "Numbered Topic"]].drop_duplicates().values

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


def parse_body_part(pnum, md_text):
    """Parses markdown and returns a dictionary split by header

    Args:
        md_text (str): A string of markdown format

    Returns:
        parsed_md_text (dict): A dictionary split of the text
    """

    part = "part" + f"{pnum}"

    # Special dict to store stuff
    nested_dict = pbh.create_data2()

    # Create Markdown parser
    mdit = markdown_it.MarkdownIt()
    env = {}
    tokens = mdit.parse(md_text, env)

    # Get Level 2 headers and make sure there's only one!
    level2_headers = [
        i for i, j in enumerate(tokens) if j.tag == "h2" if j.nesting == 1
    ]
    assert (
        len(level2_headers) == 1
    ), "There is a problem in the question, there seem to be multiple level two headers in a body part, or there is a weird edge-case in the parse_body_part() function"

    assert (
        len(tokens[level2_headers[0] + 1].content) < 20
    ), "There is an (arbitrary/opinionated) restriction on the length of 20 chars for a a 'part' title."

    nested_dict[part]["title"] = tokens[level2_headers[0] + 1].content

    # Store the content of the level 2 header
    try:
        content = mdformat.renderer.MDRenderer().render(
            tokens[3 : get_next_headerloc(3, tokens, 3)], mdit.options, env
        )  # Note the 3 is there to exclude header start,header content,header end tokens
        nested_dict[part]["content"] = content.replace(r"\\", "\\")
    except IndexError:
        print(
            "It looks like there is an empty section of header level 2 in your md file."
        )
        raise

    # Get all Level 3 headers
    level3_headers = [
        i for i, j in enumerate(tokens) if j.tag == "h3" if j.nesting == 1
    ]

    for hd in level3_headers:
        header = tokens[hd + 1].content
        assert (
            len(header) < 20
        ), "There is an (arbitrary/opinionated) restriction on the length of 20 chars for a a 'sub-part' title."
        if "Answer Section" in header:
            header = "answer"
        try:
            content = codecs.unicode_escape_decode(
                mdformat.renderer.MDRenderer().render(
                    tokens[hd + 3 : get_next_headerloc(hd + 3, tokens, 3)],
                    mdit.options,
                    env,
                )
            )[
                0
            ]  # Note the +3 is there to exclude header start,header content,header end tokens
            nested_dict[part][header] = content
        except IndexError:
            print(
                "It looks like there is an empty section of header level 3 in your md file."
            )
            # TODO: in the future, suggest ignoring empty sections instead of throwing an error
            raise

    return defdict_to_dict(nested_dict, {})


def get_next_headerloc(start, tokens, header_level):
    """Some annoying code that takes in a token to start looking from, and returns the token at the start of the next header level.

    Args:
        start (int): Token # to start looking from
        tokens (token): Parsed MD file
        header_level (int): "Next" Header level to look for.

    Returns:
        int: Token # to "end" looking at
    """

    # no header found, set close to end
    close = len(tokens)

    for i, j in enumerate(tokens[start:]):
        if j.tag == f"h{header_level}" and j.nesting == 1:
            # next header found
            close = i + start
            break
    return close


# def split_body_parts(num_parts, body_parts):
#     """Parses individual question parts and splits out titles, and content

#     Args:
#         num_parts (int): An integer corresponding to the number of question parts (from `read_md_problem()`).
#         body_parts (dict): A dictionary from `read_md_problem()`.

#     Returns:
#         body_parts_dict (dict): returns a nested dictionary with title,content,answer keys .
#     """
#     mdit = markdown_it.MarkdownIt()
#     env = {}
#     nested_dict = lambda: defaultdict(nested_dict)

#     parts_dict = nested_dict()

#     for pnum in range(1, num_parts + 1):

#         part = "part" + f"{pnum}"
#         # Set up tokens by parsing the md file
#         tokens = mdit.parse(body_parts[part], env)

#         ptt = [i for i, j in enumerate(tokens) if j.tag == "h2"]
#         parts_dict[part]["title"] = (
#             mdformat.renderer.MDRenderer()
#             .render(tokens[ptt[0] + 1 : ptt[1]], mdit.options, env)
#             .strip("\n")
#         )

#         # Get the "### Answer section from the parts_dict"
#         pa = [i
#                 for i, j in enumerate(tokens)
#                 if j.tag == "h3"
#                 if "pl-submission-panel" not in j.content
#                 if "pl-answer-panel" not in j.content
#             ]

#         try:
#             parts_dict[part]["answer"]["title"] = codecs.unicode_escape_decode(
#                 mdformat.renderer.MDRenderer().render(
#                     tokens[pa[0] + 1 : pa[1]], mdit.options, env
#                 )
#             )[0]
#         except IndexError:
#             print(
#                 "Check the heading levels, is there one that doesn't belong? Or is the heading level incorrect? For e.g., it should be ### Answer Section (this is not necessarily where the issue is)."
#             )
#             raise

#         parts_dict[part]["content"] = codecs.unicode_escape_decode(
#             mdformat.renderer.MDRenderer().render(
#                 tokens[ptt[1] + 1 : pa[0]], mdit.options, env
#             )
#         )[0]
#         parts_dict[part]["answer"]["content"] = codecs.unicode_escape_decode(
#             mdformat.renderer.MDRenderer().render(
#                 tokens[pa[1] + 1 :], mdit.options, env
#             )
#         )[0]

#         # Get the ### pl-submission-panel and ### pl-answer-panel
#         p_extra = [i
#                 for i, j in enumerate(tokens)
#                 if j.tag == "h3"
#                 if "pl-submission-panel" in j.content
#                 if "pl-answer-panel" in j.content
#             ]

#         if p_extra:
#             try:
#                 parts_dict[part]["pl-submission-panel"] = codecs.unicode_escape_decode(
#                     mdformat.renderer.MDRenderer().render(
#                         tokens[p_extra[0] + 1 : p_extra[1]], mdit.options, env
#                     )
#                 )[0]
#             except IndexError:
#                 print(
#                     "Check the heading levels, is there one that doesn't belong? Or is the heading level incorrect? For e.g., it should be ### Answer Section (this is not necessarily where the issue is)."
#                 )
#                 raise


#         # for key in body_parts.keys():
#         #     print(f'outside: {key}')
#         #     if key in ['pl-submission-panel','pl-answer-panel']:
#         #         # Set up tokens by parsing the md file
#         #         tokens = mdit.parse(body_parts[key], env)

#         #         print(key)

#         #         ptt = [i for i,j in enumerate(tokens) if j.tag=='h3']
#         #         try:
#         #             parts_dict[part][key] = codecs.unicode_escape_decode(MDRenderer().render(tokens[ptt[-1]+1:], mdit.options, env))[0]
#         #         except IndexError:
#         #             print("It's possible you have '### pl-submission-panel' or '### pl-answer-panel' with the wrong heading level - H2 instead of the required H3.")

#         # Remove parts from body_parts
#         body_parts.pop(part)

#     return defdict_to_dict(parts_dict, {})


def read_md_problem(filepath):
    """Reads a MystMarkdown problem file and returns a dictionary of the header and body

    Args:
        filepath (str): Path of file to read.

    Returns:
        dict: In this dictionary there are three keys containing useful portions of the parsed md file:
            - `header` - Header of the problem file (nested dictionary).
            - `body_parts` - Body text of the problem file (nested dictionary).
            - `num_parts` - Number of parts in the problem (integer).
            - `body_parts_split` - Dictionary with each part split into individual components.
    """

    mdtext = pathlib.Path(filepath).read_text(encoding="utf8")

    # Deal with YAML header
    header_text = mdtext.rsplit("---\n")[1]
    header = yaml.safe_load("---\n" + header_text)
    validate_header(header)
    # Deal with Markdown Body
    body = mdtext.rsplit("---\n")[2]

    # Set up the markdown parser
    # to be honest, not fully sure what's going on here, see this issue: https://github.com/executablebooks/markdown-it-py/issues/164

    mdit = markdown_it.MarkdownIt()
    env = {}

    # Set up tokens by parsing the md file
    tokens = mdit.parse(body, env)

    blocks = {}

    block_count = 0

    num_titles = 0

    ###
    for x, t in enumerate(tokens):
        if t.tag == "h1" and t.nesting == 1:  # title
            # oh boy. this is going to break and it will be your fault firas.
            blocks["title"] = [x, x + 3]
            num_titles += 1

        elif t.tag == "h2" and t.nesting == 1:
            block_count += 1

            if block_count == 1:
                blocks["block{0}".format(block_count)] = [
                    x,
                ]
            else:
                blocks["block{0}".format(block_count - 1)].append(x)
                blocks["block{0}".format(block_count)] = [
                    x,
                ]
    ###
    # Add -1 to the end of the last block
    blocks[f"block{block_count}"].append(len(tokens))

    # Assert statements (turn into tests!)
    assert (
        num_titles == 1
    ), "I see {0} Level 1 Headers (#) in this file, there should only be one!".format(
        num_titles
    )
    assert (
        block_count >= 1
    ), "I see {0} Level 2 Headers (##) in this file, there should be at least 1".format(
        block_count - 1
    )

    # Add the end of the title block; # small hack
    # blocks['title'].append(blocks['block1'][0])

    # Get the preamble before the parts start
    blocks["preamble"] = [blocks["title"][1], blocks["block1"][0]]

    ## Process the blocks into markdown

    body_parts = {}
    parts_dict = {}

    part_counter = 0

    for k, v in blocks.items():
        rendered_part = (
            mdformat.renderer.MDRenderer()
            .render(tokens[v[0] : v[1]], mdit.options, env)
            .replace(r"\\", "\\")
        )

        if k == "title":
            body_parts["title"] = rendered_part

        elif k == "preamble":
            body_parts["preamble"] = rendered_part

        elif "Rubric" in rendered_part:
            body_parts["Rubric"] = rendered_part

        elif "Solution" in rendered_part:
            body_parts["Solution"] = rendered_part

        elif "Comments" in rendered_part:
            body_parts["Comments"] = rendered_part

        elif "Useful Info" in rendered_part:
            body_parts["Useful_info"] = rendered_part

        else:
            part_counter += 1
            body_parts[f"part{part_counter}"] = rendered_part

            parts_dict.update(parse_body_part(part_counter, rendered_part))

    return_dict = {
        "header": header,
        "body_parts": body_parts,
        "num_parts": part_counter,
        "body_parts_split": parts_dict,
    }
    return defdict_to_dict(return_dict, {})


def dict_to_md(
    md_dict,
    remove_keys=[
        None,
    ],
):
    """Takes a nested dictionary (e.g. output of read_md_problem()) and returns a multi-line string  that can be written to a file (after removing specified keys).
    Args:
        md_dict (dict): A nested dictionary, for e.g. the output of `read_md_problem()`
        remove_keys (list, optional): Any keys to remove from the dictionary, for instance solutions. Defaults to [None,].

    Returns:
        str: A multi-line string that can be written to a file.
    """

    md_string = ""

    md_dict = defdict_to_dict(md_dict, {})

    # Question Title and Preamble
    md_string += md_dict.pop("title", None)
    md_string += md_dict.pop("preamble", None)

    # TODO: Refactor this to use the elegant solution provided here: https://stackoverflow.com/a/49723101/2217577

    for k, v in md_dict.items():
        if k in remove_keys:
            continue
        else:
            md_string += "\n" + md_dict[k]

    return md_string


## Functions from md-to-pl


def write_info_json(output_path, parsed_question):
    """
    Args:
        output_path (Path): [description]
        parsed_question (dict]): [description]
    """

    ## *** IMPORTANT: If more auto-tags or optional keys are added, make sure to update the `pl_to_md` function to take them into account properly for the roundtrip ***

    optional_keys = {
        "gradingMethod",
        "partialCredit",
        "dependencies",
        "singleVariant",
        "showCorrectAnswer",
        "externalGradingOptions",
        "workspaceOptions"
    }

    # Add tags based on part type
    q_types = []

    for pnum in range(1, parsed_question["num_parts"] + 1):
        part = "part" + f"{pnum}"
        q_types.append(parsed_question["header"][part]["type"])

    auto_tags = []
    if len(q_types) > 1:
        auto_tags.append("multi_part")
    auto_tags.extend(list(set(q_types)))

    # tags is technically an optional key for a question author to specify
    auto_tags.extend(parsed_question["header"].get("tags", []))
    auto_tags = [v for v in auto_tags if v != "unknown"]

    info_json = {
        "uuid": str(uuid.uuid3(uuid.NAMESPACE_DNS, str(output_path))),
        "title": parsed_question["header"]["title"],
        "topic": parsed_question["header"]["topic"],
        "tags": auto_tags,
        "type": "v3",
    }
    info_json.update(
        {
            key: parsed_question["header"][key]
            for key in parsed_question["header"].keys() & optional_keys
        }
    )

    if "workspaceOptions" in info_json: # validate workspaceOptions contains the required keys if it exists
        image = "image" in info_json["workspaceOptions"]
        port = "port" in info_json["workspaceOptions"]
        home = "home" in info_json["workspaceOptions"]
        if not (image and port and home):
            raise SyntaxError("workspaceOptions must contain image, port, and home keys")
        if not isinstance(info_json["workspaceOptions"]["port"], int):
            raise TypeError(f"workspaceOptions.port must be an integer, got {type(info_json['workspaceOptions']['port'])!r} instead")

    comment_keys = (
        "author",
        "source",
        "template_version",
        "outcomes",
        "difficulty",
        "randomization",
        "taxonomy",
        "span",
        "length",
    )

    comment = {key: parsed_question["header"][key] for key in comment_keys if key in parsed_question["header"]}

    # Get keys that need to get added to the comment from the question body (Rubric, Solution, Comments)

    comment |= {
        key: parsed_question["body_parts"][key].split("\n\n", 1)[-1].strip()
        for key in ("Rubric", "Solution", "Comments")
        if key in parsed_question["body_parts"]
    }

    # Add the comment to the info_json, under a metadata key in the comment object of info_json

    info_json["comment"] = {"METADATA": comment}

    # End add tags
    with pathlib.Path(output_path / "info.json").open("w") as output_file:
        json.dump(info_json, output_file, indent=4)


def assemble_server_py(parsed_question, location):
    """Assembles a string version of the server.py file from the YAML header of the md file.

    Args:
        parsed_question (_type_): dictionary that is created upon reading of the md problem.
        location (string): 'local' or 'prairielearn' ; the import statements are different depending on if it's local or on a PL server.
    """

    server_dict = parsed_question["header"]["server"].copy()

    if location == "local":
        # This is needed to run this locally compared to when it gets run on a PL server
        server_dict["imports"] = parsed_question["header"]["server"]["imports"].replace(
            "import prairielearn as pl",
            "import problem_bank_scripts.prairielearn as pl",
        )
    elif "import problem_bank_helpers as pbh" not in server_dict["imports"]:
        server_dict["imports"] += "\nimport problem_bank_helpers as pbh # Added in by problem bank scripts"

    server_py = f""""""

    server_py += server_dict.get("imports", "") + "\n"

    try:
        for function, code in server_dict.items():
            indented_code = code.replace("\n", "\n    ")
            # With the custom header, add functions to server.py as-is
            if function == "custom":
                continue
            else:
                if code:
                    server_py += f"def {function}(data):\n    {indented_code}\n"
            if location == "prairielearn" and function == "generate":
                server_py += """\
    # Start code added automatically by problem_bank_scripts

    # Convert backticks to code blocks/fences in answer choices.
    pbh.backticks_to_code_tags(data2)

    # Update data with data2
    data.update(data2)

    # End code added in by problem bank scripts

"""
    except:
        raise

    if "custom" in server_dict.keys():
        server_py += f"{server_dict['custom']}"

    return server_py


def write_server_py(output_path, parsed_question):
    """Writes the server.py file to disk
    Args:
        output_path ([type]): [description]
        parsed_question ([type]): [description]
    """

    output_path = pathlib.Path(output_path)

    server_file = assemble_server_py(parsed_question, "prairielearn")

    # Deal with path differences when using PL
    server_file = server_file.replace(
        'read_csv("', 'read_csv(data["options"]["client_files_course_path"]+"/'
    )

    # Write server.py
    (output_path / "server.py").write_text(server_file, encoding="utf8")


def BasicInputConverter(pl_tag: str, ans_name: bool=True):
    """Creates a basic input type converter for a given PL tag, such as `pl-number-input` or `pl-string-input`.
    
    Basic is determined by the fact that the processor just needs to set the appropriate tag,
    group the pl-customizations, and return the HTML including the markdown content for the question.

    More complex processors will need to be created manually, or with a different factory function.

    Args:
        pl_tag (str): The tag to be used for the input type, such as `number-input` (for `pl-number-input`) or `string-input` (for `pl-string-input`).
        ans_name (bool, optional): Wether the answers-name attribute should be autogenerated. Defaults to True.

    Returns:
        function: A function that processes markdown format of the given input type and returns PL HTML.
    """

    def closure(part_name: str, parsed_question: dict, data_dict: dict):
        pl_customizations = " ".join(
            [
                f'{k} = "{v}"'
                for k, v in parsed_question["header"][part_name][
                    "pl-customizations"
                ].items()
            ]
        )  # PL-customizations

        html = f"""<pl-question-panel>\n<markdown>{parsed_question['body_parts_split'][part_name]['content']}</markdown>\n</pl-question-panel>\n\n"""

        if "answers-name" in pl_customizations or ans_name is False:
            html += f"""<pl-{pl_tag} {pl_customizations} ></pl-{pl_tag}>\n"""
        else:
            html += f"""<pl-{pl_tag} answers-name="{part_name}_ans" {pl_customizations} ></pl-{pl_tag}>\n"""

        return replace_tags(html)
    
    closure.__name__ = f"process_{pl_tag.replace('-', '_')}"
    closure.__doc__ = f"""Processes markdown format of {pl_tag} questions and returns PL HTML\

Args:
    part_name (string): Name of the question part being processed (e.g., part1, part2, etc...)
    parsed_question (dict): Dictionary of the MD-parsed question (output of `read_md_problem`)
    data_dict (dict): Dictionary of the `data` dict created after running server.py using `exec()`

Returns:
    html: A string of HTML that is part of the final PL question.html file.
"""

    return closure


def MCInputConverter(pl_tag: str):
    """Creates a input type converter for a given multiple choice style tag, such as `pl-multiple-choice` or `pl-dropdown`.


    Args:
        pl_tag (str): The tag to be used for the input type, such as `multiple-choice` (for `pl-multiple-choice`) or `dropdown` (for `pl-dropdown`).

    Returns:
        function: A function that processes markdown format of the given input type and returns PL HTML.
    """

    def closure(part_name: str, parsed_question: dict, data_dict: dict):

        if pl_tag == "multiple-choice":
            validate_multiple_choice(part_name, parsed_question, data_dict)
        
        html = f"""<pl-question-panel>\n<markdown>{parsed_question['body_parts_split'][part_name]['content']}</markdown>\n</pl-question-panel>\n\n"""

        pl_customizations = " ".join(
            [
                f'{k} = "{v}"'
                for k, v in parsed_question["header"][part_name][
                    "pl-customizations"
                ].items()
            ]
        )  # PL-customizations
        html += f"""<pl-{pl_tag} answers-name="{part_name}_ans" {pl_customizations} >\n"""

        ###### LOOKHERE
        if (data_dict["params"][f"vars"]["units"]) and (
            "units" in parsed_question["body_parts_split"][part_name]["answer"]
        ):
            units = f"|@ params.vars.units @|"
        else:
            units = ""

        ## Note: `|@`` gets converted into `{{` and `@|`` gets converted to `}}` by `replace_tags()`
        for a in data_dict["params"][f"{part_name}"].keys():
            if "ans" in a:
                if data_dict["params"][f"{part_name}"][f"{a}"]["feedback"]:
                    feedback = f"|@ params.{part_name}.{a}.feedback @|"
                else:
                    feedback = f"Feedback for this choice is not available yet."

                correctness = f"|@ params.{part_name}.{a}.correct @|"
                value = f"|@|@ params.{part_name}.{a}.value @|@|"

                ## Hack to remove feedback for Dropdown questions
                if parsed_question["header"][part_name]["type"] == "dropdown":
                    html += f"\t<pl-answer correct= {correctness} > {value} {units} </pl-answer>\n"
                else:
                    html += f"\t<pl-answer correct= {correctness} feedback = '{feedback}' > {value} {units} </pl-answer>\n"

        html += f"</pl-{pl_tag}>\n"

        return replace_tags(html)
    
    closure.__name__ = f"process_{pl_tag.replace('-', '_')}"
    closure.__doc__ = f"""Processes markdown format of {pl_tag} questions and returns PL HTML\

Args:
    part_name (string): Name of the question part being processed (e.g., part1, part2, etc...)
    parsed_question (dict): Dictionary of the MD-parsed question (output of `read_md_problem`)
    data_dict (dict): Dictionary of the `data` dict created after running server.py using `exec()`

Returns:
    html: A string of HTML that is part of the final PL question.html file.
"""

    return closure


def process_matching(part_name, parsed_question, data_dict):
    """Processes markdown format matching questions and returns PL HTML
    Args:
        output_path (Path): [description]
        parsed_question (dict): [description]
        data_dict (dict)

    Returns:
        str: Matching question is returned as a string with PL-compliant syntax.
    """
    print("Processing matching question...")

    html = f"""<pl-question-panel>\n<markdown>{parsed_question['body_parts_split'][part_name]['content']}</markdown>\n</pl-question-panel>\n\n"""

    pl_customizations = " ".join(
        [
            f'{k} = "{v}"'
            for k, v in parsed_question["header"][part_name][
                "pl-customizations"
            ].items()
        ]
    )  # PL-customizations
    html += (
        f"""<pl-matching answers-name="{part_name}_matching" {pl_customizations} >\n"""
    )

    options = ""
    statements = ""
    ## Note: `|@`` gets converted into `{{` and `@|`` gets converted to `}}` by `replace_tags()`
    for a in data_dict["params"][f"{part_name}"].keys():
        if "option" in a:
            value = f"|@|@ params.{part_name}.{a}.value @|@|"

            if name := data_dict["params"][f"{part_name}"][a].get("name"):
                options += f"\t<pl-option name='{name}' > {value} </pl-option>\n"
            else:
                options += f"\t<pl-option> {value} </pl-option>\n"

        if "statement" in a:
            matches_with = f"|@ params.{part_name}.{a}.matches @|"
            value = f"|@|@ params.{part_name}.{a}.value @|@|"

            statements += (
                f"\t<pl-statement match= '{matches_with}' > {value} </pl-statement>\n"
            )

    html += statements
    html += options

    html += "</pl-matching>\n"

    return replace_tags(html)


def process_file_upload(part_name, parsed_question, data_dict):
    """Processes markdown format of file-upload questions and returns PL HTML
    Args:
        part_name (string): Name of the question part being processed (e.g., part1, part2, etc...)
        parsed_question (dict): Dictionary of the MD-parsed question (output of `read_md_problem`)
        data_dict (dict): Dictionary of the `data` dict created after running server.py using `exec()`

    Returns:
        html: A string of HTML that is part of the final PL question.html file.
    """
    pl_customizations = " ".join(
        [
            f'{k} = "{v}"'
            for k, v in parsed_question["header"][part_name][
                "pl-customizations"
            ].items()
        ]
    )  # PL-customizations

    html = f"""<pl-question-panel>\n<markdown>{parsed_question['body_parts_split'][part_name]['content']}</markdown>\n</pl-question-panel>\n\n"""

    html += f"""<pl-file-upload { pl_customizations } > </pl-file-upload>"""

    html += f"""<pl-submission-panel>\n\t<pl-file-preview></pl-file-preview>\n\t<pl-external-grader-results></pl-external-grader-results>"""

    # TODO: remove this! because automatic feedback will be added
    html += f"""\n\t|@ #feedback.manual @| \n\t<p>Feedback from course staff:</p>\n\t<markdown>|@|@ feedback.manual @|@|</markdown>\n\t|@ /feedback.manual @|\n</pl-submission-panel>"""

    # TODO: Add better support for what students see when they upload a file where many are possible. Currently: Error: The following required files were missing: *.jpg, *.pdf, foo.py, bar.c, filename space.txt
    # TODO: Add support for wildcard *.png
    # TODO: Add better message telling students the question needs to be manually graded.

    return replace_tags(html)


def process_workspace(part_name, parsed_question, data_dict):
    """Processes markdown format of workspace questions and returns PL HTML
    Args:
        part_name (string): Name of the question part being processed (e.g., part1, part2, etc...)
        parsed_question (dict): Dictionary of the MD-parsed question (output of `read_md_problem`)
        data_dict (dict): Dictionary of the `data` dict created after running server.py using `exec()`

    Returns:
        html: A string of HTML that is part of the final PL question.html file.
    """
    if "pl-customizations" in parsed_question["header"][part_name]:
        if len(parsed_question["header"][part_name]["pl-customizations"]) > 0:
            raise ValueError("pl-customizations are not supported for workspace questions")


    html = f"""<pl-question-panel>\n<markdown>{parsed_question['body_parts_split'][part_name]['content']}</markdown>\n</pl-question-panel>\n\n"""

    html += f"""<pl-workspace></pl-workspace>"""

    html += f"""\n<pl-submission-panel>"""

    if parsed_question["header"][part_name].get("gradingMethod", None) == "External":
        html += f"""\n<pl-external-grader-results></pl-external-grader-results>\n<pl-file-preview></pl-file-preview>"""
    
    html += f"""\n<ul>\n\t|@ #feedback.results @| \n\t<li>|@ . @|</li>\n\t|@ /feedback.results @|\n</ul>\n</pl-submission-panel>"""


    return replace_tags(html)


def validate_multiple_choice(part_name, parsed_question, data_dict):
    """Validates a markdown format multiple-choice question
    Args:
        part_name (string): Name of the question part being processed (e.g., part1, part2, etc...)
        parsed_question (dict): Dictionary of the MD-parsed question (output of `read_md_problem`)
        data_dict (dict): Dictionary of the `data` dict created after running server.py using `exec()`

    Returns:
        bool: True if the question is valid, False otherwise.
    """

    def validate_ans(val, ans_name, part_name):
        try:
            json.dumps(val)
            if not isinstance(val, bool):
                msg = (
                    f"Object of type {val.__class__.__name__!r} for the value of correct for {ans_name!r} of {part_name!r} is not a boolean value."
                    "\n Implicitly relying on truthiness of the value is not recommended. Please use `True` or `False`."
                )
                warnings.warn(msg, SyntaxWarning)
            return bool(val)
        except TypeError as err:
            msg = f"Object of type {val.__class__.__name__!r} is not valid for the correct key for answer {ans_name!r} of {part_name!r}."
            raise TypeError(msg) from err

    if any(
        validate_ans(ans["correct"], key, part_name)
        for key, ans in data_dict["params"][f"{part_name}"].items()
        if "ans" in key
    ):
        return

    none_of_the_above = parsed_question["header"][part_name]["pl-customizations"].get("none-of-the-above", "false")

    if none_of_the_above in {"correct", "random"}:
        return

    raise ValueError(
        f"Multiple choice question {part_name} does not have a correct answer and "
        "the pl-customization `none-of-the-above` was not set to `correct` or `random`."
    )

def replace_tags(string):
    """Takes in a string with tags: |@ and @| and returns {{ and }} respectively. This is because Python strings can't have double curly braces.

    Args:
        string (str): String to be processed, can be multi-line.

    Returns:
        string (str): returns string with tags replaced with curly braces.
    """
    return (
        string.replace("|@|@", "{{{")
        .replace("@|@|", "}}}")
        .replace("|@", "{{")
        .replace("@|", "}}")
    )

_SUPPORTED_INPUTS: dict[str, tuple[Callable[[str, dict, dict], str], str]] = {
    "number-input":           (BasicInputConverter("number-input"), "pl-number-input"),
    "symbolic-input":         (BasicInputConverter("symbolic-input"), "pl-symbolic-input"),
    "matrix-input":           (BasicInputConverter("matrix-input"), "pl-matrix-input"),
    "matrix-component-input": (BasicInputConverter("matrix-component-input"), "pl-matrix-component-input"),
    "string-input":           (BasicInputConverter("string-input", False), "pl-string-input"),
    "longtext":               (BasicInputConverter("rich-text-editor", False), "pl-rich-text-editor"),
    "file-editor":            (BasicInputConverter("file-editor", False), "pl-file-editor"),
    "multiple-choice":        (MCInputConverter("multiple-choice"), "pl-multiple-choice"),
    "checkbox":               (MCInputConverter("checkbox"), "pl-checkbox"),
    "dropdown":               (MCInputConverter("dropdown"), "pl-dropdown"),
    "file-upload":            (process_file_upload, "pl-file-upload"),
    "matching":               (process_matching, "pl-matching"),
    "workspace":              (process_workspace, "pl-workspace"),
}

INPUT_TYPE_PROCESSORS = {opb_name: func for opb_name, (func, _) in _SUPPORTED_INPUTS.items()}
OPB_INPUT_TYPES = {tag: opb_name for opb_name, (_, tag) in _SUPPORTED_INPUTS.items()}

def remove_correct_answers(data2_dict):
    """Magical recursive function that removes particular keys from a nested dictionary: https://stackoverflow.com/a/29652561/2217577

    Args:
        data2_dict (dict): Dictionary (nested) from which to remove key:value

    Returns:
        data2_dict (dict): Dictionary with the offending keys removed
    """

    # This was adapted from this SO: https://stackoverflow.com/a/29652561/2217577
    def gen_dict_extract(key_to_remove, dict_object):
        if hasattr(dict_object, "items"):
            for k, v in list(dict_object.items()):
                if key_to_remove in k:
                    dict_object.pop(k, None)
                if isinstance(v, dict):
                    for result in gen_dict_extract(key_to_remove, v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in gen_dict_extract(key_to_remove, d):
                            yield result

    list(gen_dict_extract("correct", data2_dict))

    return data2_dict


with importlib.resources.files(__package__).joinpath("attributions.json").open("rb") as file:
    _ATTRIBUTIONS: dict[str, str] = json.load(file)
    _KNOWN_ATTRIBUTIONS = list(_ATTRIBUTIONS.keys())

def process_attribution(attribution):
    """Takes in a string and returns the HTML for the attribution

    Args:
        attribution (string): One of a set of pre-defined values corresponding to a particular attribution.

    Returns:
        string (str): returns the html of the attribution
    """

    try:
        return _ATTRIBUTIONS[attribution]

    except KeyError:
        print(
            f"`Attribution` value of {attribution} is not recognized. Currently, the only possible values are: {_KNOWN_ATTRIBUTIONS}. You need to update your md file and fix the `attribution` in the header"
        )
        raise


def process_question_md(source_filepath, output_path=None, instructor=False):
    try:
        pathlib.Path(source_filepath)
    except:
        print(f"{source_filepath} - File does not exist.")
        raise

    if output_path is None:
        if instructor:
            path_replace = "output/instructor"
        else:
            path_replace = "output/public"

        if "source" in source_filepath:
            output_path = pathlib.Path(source_filepath.replace("source", path_replace))
        else:
            raise NotImplementedError(
                "Check the source filepath; it does not have 'source' in it!! "
            )
    else:
        ## TODO: Make this a bit more robust, perhaps by switching encodings!?
        output_path = pathlib.Path(output_path)

    # deal with multi-line strings in YAML Dump
    ## Code copied from here: https://stackoverflow.com/a/33300001/2217577

    def str_presenter(dumper, data2):
        if len(data2.splitlines()) > 1:  # check for multiline string
            # data2 = re.sub('\\n[\s].*\\n','\n\n',data2) # THIS IS WRONG!!!
            data2 = re.sub(
                "\\n\s+\\n", "\n\n", data2
            )  # # Try \s{3,} for three or more spaces
            return dumper.represent_scalar("tag:yaml.org,2002:str", data2, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data2)

    yaml.add_representer(str, str_presenter)

    parsed_q = read_md_problem(source_filepath)

    header = parsed_q["header"]
    body_parts = parsed_q["body_parts"]

    #################################################################################
    # Run the python code; this improved way was suggested by Phil Austin of UBC EOAS

    server_py = assemble_server_py(parsed_q, "local")

    spec = importlib.util.spec_from_loader("server", loader=None)
    server = importlib.util.module_from_spec(spec)
    exec(server_py, server.__dict__)

    data2 = pbh.create_data2()
    server.generate(data2)
    #################################################################################

    # Remove the solutions from the server section
    if instructor is False:
        # Remove python solution from the public view
        header.pop("server", None)

        # Remove correct answers from the data2 dict
        data2_sanitized = defdict_to_dict(data2, {})
        data2_sanitized = defdict_to_dict(remove_correct_answers(data2_sanitized), {})

        ####################################################
        #### Start Temporary Fix for issue of myst no longer permitting nested dicts
        #### GitHub issue: https://github.com/executablebooks/MyST-Parser/issues/761

        df = pd.json_normalize(data2_sanitized, sep="_")
        data2_sanitized_flattened = df.to_dict(orient="records")[0]

        repl_keys = {
            k.replace("_", "."): k for k in list(data2_sanitized_flattened.keys())
        }

        text = dict_to_md(
            body_parts,
            remove_keys=[
                "Rubric",
                "Solution",
                "Comments",
                "pl-submission-panel",  # FIXME: This will not remove level 3 headings because it's all a string!
                "pl-answer-panel",  # FIXME: This will not remove level 3 headings because it's all a string!
            ],
        )

        for k, v in repl_keys.items():
            text = text.replace(k, v)

        # Update the YAML header to add substitutions
        header.update({"myst": {"substitutions": data2_sanitized_flattened}})

        # Update the YAML header to add substitutions, unsort it, and process for file
        header_yml = yaml.dump(header, sort_keys=False, allow_unicode=True)

        # Write the YAML to a file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            "---\n"
            + header_yml
            + "---\n"
            + text
            + "\n## Attribution\n\n"
            + process_attribution(header.get("attribution")),
            encoding="utf8",
        )

        ####################################################
        #### End Temporary Fix for issue of myst no longer permitting nested dicts
        #### Uncomment below when the fix is implemented to recover past behaviour

        # # Update the YAML header to add substitutions
        # header.update({"myst": {"substitutions": data2_sanitized} })

        # # Update the YAML header to add substitutions, unsort it, and process for file
        # header_yml = yaml.dump(header, sort_keys=False, allow_unicode=True)

        # # Write the YAML to a file
        # output_path.parent.mkdir(parents=True, exist_ok=True)
        # output_path.write_text(
        #     "---\n"
        #     + header_yml
        #     + "---\n"
        #     + dict_to_md(
        #         body_parts,
        #         remove_keys=[
        #             "Rubric",
        #             "Solution",
        #             "Comments",
        #             "pl-submission-panel", #FIXME: This will not remove level 3 headings because it's all a string!
        #             "pl-answer-panel",     #FIXME: This will not remove level 3 headings because it's all a string!
        #         ],
        #     )
        #     + "\n## Attribution\n\n"
        #     + process_attribution(header.get("attribution")),
        #     encoding="utf8",
        # )

    else:
        # Update the YAML header to add substitutions
        header.update({"myst": {"substitutions": defdict_to_dict(data2, {})}})

        # return {'header':header,
        #         'body_parts':body_parts,
        #         'output_path':output_path}

        # Update the YAML header to add substitutions, unsort it, and process for file
        header_yml = yaml.dump(header, sort_keys=False, allow_unicode=True)

        # Write the YAML to a file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            "---\n"
            + header_yml
            + "\n---\n"
            + dict_to_md(body_parts)
            + "\n## Attribution\n\n"
            + process_attribution(header.get("attribution")),
            encoding="utf8",
        )

    # Create the file errors list
    os_errors = []

    # Move client assets (generally images)
    files_to_copy = header.get("assets")
    if files_to_copy:
        pl_path = output_path.parent
        for file in files_to_copy:
            try:
                copy2(pathlib.Path(source_filepath).parent / file, pl_path / file)
            except (FileExistsError, FileNotFoundError, IsADirectoryError, PermissionError) as e:
                os_errors.append(str(e))

    # Move server assets
    files_to_copy = header.get("serverFiles")
    if files_to_copy and instructor:
        pl_path = output_path.parent
        for file in files_to_copy:
            try:
                copy2(pathlib.Path(source_filepath).parent / file, pl_path / file)
            except (FileExistsError, FileNotFoundError, IsADirectoryError, PermissionError) as e:
                os_errors.append(str(e))

    # Move autograde py test files
    files_to_copy = header.get("autogradeTestFiles")
    if files_to_copy:
        pl_path = output_path.parent / "tests"
        pl_path.mkdir(parents=True, exist_ok=True)
        for file in files_to_copy:
            if file != "starter_code.py" and not instructor:
                continue
            try:
                copy2(pathlib.Path(source_filepath).parent / "tests" / file, pl_path / file)
            except (FileExistsError, FileNotFoundError, IsADirectoryError, PermissionError) as e:
                os_errors.append(str(e))
    
    # Move workspace files
    files_to_copy = header.get("workspaceFiles")
    if files_to_copy:
        pl_path = output_path.parent / "workspace"
        pl_path.mkdir(parents=True, exist_ok=True)
        for file in files_to_copy:
            try:
                copy2(pathlib.Path(source_filepath).parent / "workspace" / file, pl_path / file)
            except (FileExistsError, FileNotFoundError, IsADirectoryError, PermissionError) as e:
                os_errors.append(str(e))

    if os_errors:
        error_msg = "\n    ".join(os_errors)
        raise FileNotFoundError(f"Error(s) copying specified files:\n    {error_msg}")


def process_question_pl(source_filepath, output_path=None, dev=False):
    try:
        pathlib.Path(source_filepath)
    except:
        print(f"{source_filepath} - File does not exist.")
        raise

    path_replace = "output/prairielearn"

    if output_path is None:
        if "source" in source_filepath:
            output_path = pathlib.Path(
                source_filepath.replace("source", path_replace)
            ).parent
        else:
            raise NotImplementedError(
                "Check the source filepath; it does not have 'source' in it!! "
            )
    else:
        ## TODO: It's annoying that here output_path.parent is used, but for md problems, it's just output_path
        output_path = pathlib.Path(output_path).parent

    # Parse the MD file
    parsed_q = read_md_problem(source_filepath)
    parsed_q["header"]["topic"] = topics[
        parsed_q["header"]["topic"]
    ]  # Add integer topic id, this is safe because we validated the header in read_md_problem

    # Create output dir if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    #################################################################################
    # Run the python code; this improved way was suggested by Phil Austin of UBC EOAS

    server_py = assemble_server_py(parsed_q, "local")

    spec = importlib.util.spec_from_loader("server", loader=None)
    server = importlib.util.module_from_spec(spec)
    exec(server_py, server.__dict__)

    data2 = pbh.create_data2()

    server.generate(data2)
    #################################################################################

    if dev:
        tags = parsed_q["header"].get("tags", [])
        tags.append("DEV")
        parsed_q["header"]["tags"] = tags

    # Write info.json file
    write_info_json(output_path, parsed_q)

    # Question Preamble
    preamble = parsed_q["body_parts"].get("preamble", None)
    # TODO: Remove Debugging print statement
    # print(f"premable: {preamble}")

    if preamble:
        question_html = f"<pl-question-panel>\n<markdown>\n{ preamble }\n</markdown>\n</pl-question-panel>\n\n"
    else:
        question_html = f""

    # Useful info panel
    useful_info = parsed_q["body_parts"].get("Useful_info", None)

    # TODO: When PrairieLearn updates to BootStrap5, update this box as described here: https://github.com/open-resources/problem_bank_scripts/issues/30#issuecomment-1177101211
    # *** IMPORTANT: If you update how this works, make sure you update the `pl_to_md` function to be able to properly parse and understand the new implementation! ***
    if useful_info:
        question_html += f"""<p>
   <button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#collapseExample" aria-expanded="false" aria-controls="collapseExample">
   <i class="fa fa-info-circle" aria-hidden="true"></i> Helpful Information
   </button>
</p>
<div class="collapse" id="collapseExample">
   <div class="card card-body">
      <markdown>
{parsed_q['body_parts']['Useful_info']}
      </markdown>
   </div>
</div>"""

    # Single and Multi-part question construction

    for pnum in range(1, parsed_q["num_parts"] + 1):
        part = "part" + f"{pnum}"
        q_type = parsed_q["header"][part]["type"]

        question_html += f"\n<!-- ######## Start of Part {pnum} ######## -->\n\n"

        if parsed_q["num_parts"] > 1:
            question_html += f"""<div class="card my-2">
<div class="card-header">{parsed_q['body_parts_split'][part]['title']}</div>\n
<div class="card-body">\n\n"""
        
        converter = INPUT_TYPE_PROCESSORS.get(q_type, None)
        if converter is None:
            raise NotImplementedError(f"The question type ({q_type}) is not yet implemented.")
        else:
            question_html += f"{converter(part,parsed_q,data2)}"

        if parsed_q["num_parts"] > 1:
            question_html += "</div>\n</div>\n"

        # Add pl-submission-panel and pl-answer-panel (if they exist)
        subm_panel = parsed_q["body_parts_split"][part].get("pl-submission-panel", None)
        q_panel = parsed_q["body_parts_split"][part].get("pl-answer-panel", None)

        if subm_panel:
            question_html += (
                f"\n<pl-submission-panel>{ subm_panel } </pl-submission-panel>\n"
            )
        if q_panel:
            question_html += f"\n<pl-answer-panel>{ q_panel } </pl-answer-panel>\n"

        # TODO: Add support for other panels here as well !

        question_html += f"\n<!-- ######## End of Part {pnum} ######## -->\n"

    # Add Attribution
    question_html += f"\n<pl-question-panel>\n<markdown>\n---\n{process_attribution(parsed_q['header'].get('attribution'))}\n</markdown>\n</pl-question-panel>\n"

    # Fix Latex over-escaping from mdformat (i.e. _, [, and ]being replaced with \_, \[, and \])
    # See https://github.com/open-resources/problem_bank_scripts/issues/89
    # Also see https://github.com/open-resources/problem_bank_scripts/pull/92
    question_html = question_html.replace("\\_", "_").replace("\\[","[").replace("\\]","]")
    question_html = question_html.replace("\\*", "*").replace("\\<","<").replace("\\`","`")
    # Fix empty <markdown> block
    # See this issue: https://github.com/PrairieLearn/PrairieLearn/issues/8346
    # TODO: this can be removed once issue 8346 is resolved
    question_html = question_html.replace("<markdown></markdown>", 
                                          "<markdown> </markdown>")

    # Final pre-processing
    question_html = pl_image_path(question_html)

    # Write question.html file
    (output_path / "question.html").write_text(question_html, encoding="utf8")

    ### TODO solve the issue with the latex escape sequences, this is a workaround
    # with open((output_path / "question.html"), "w") as qfile:
    #     print(f"{question_html}", file=qfile)

    # Write server.py file
    write_server_py(output_path, parsed_q)

    # Create the file errors list
    os_errors = []

    # Move client assets (generally images)
    files_to_copy = parsed_q["header"].get("assets")
    if files_to_copy:
        pl_path = output_path / "clientFilesQuestion"
        pl_path.mkdir(parents=True, exist_ok=True)
        for file in files_to_copy:
            try:
                copy2(pathlib.Path(source_filepath).parent / file, pl_path / file)
            except (FileExistsError, FileNotFoundError, IsADirectoryError, PermissionError) as e:
                os_errors.append(str(e))

    # Move server assets
    files_to_copy = parsed_q["header"].get("serverFiles")
    if files_to_copy:
        pl_path = output_path / "serverFilesQuestion"
        pl_path.mkdir(parents=True, exist_ok=True)
        for file in files_to_copy:
            try:
                copy2(pathlib.Path(source_filepath).parent / file, pl_path / file)
            except (FileExistsError, FileNotFoundError, IsADirectoryError, PermissionError) as e:
                os_errors.append(str(e))

    # Move autograde py test files
    files_to_copy = parsed_q["header"].get("autogradeTestFiles")
    if files_to_copy:
        pl_path = output_path / "tests"
        pl_path.mkdir(parents=True, exist_ok=True)
        for file in files_to_copy:
            try:
                copy2(pathlib.Path(source_filepath).parent / "tests" / file, pl_path / file)
            except (FileExistsError, FileNotFoundError, IsADirectoryError, PermissionError) as e:
                os_errors.append(str(e))
    
    # Move workspace files
    files_to_copy = parsed_q["header"].get("workspaceFiles")
    if files_to_copy:
        pl_path = output_path / "workspace"
        pl_path.mkdir(parents=True, exist_ok=True)
        for file in files_to_copy:
            try:
                copy2(pathlib.Path(source_filepath).parent / "workspace" / file, pl_path / file)
            except (FileExistsError, FileNotFoundError, IsADirectoryError, PermissionError) as e:
                os_errors.append(str(e))

    if os_errors:
        error_msg = "\n    ".join(os_errors)
        raise FileNotFoundError(f"Error(s) copying specified files:\n    {error_msg}")


def pl_image_path(html):
    """Adds `{{options.client_files_question_url}}` directory before the path automatically"""

    # TODO: Figure out the regex to make this into a single expression, maybe with |
    # If image files are included as markdown format, add {{options.client_files_question_url}}
    res = re.subn(
        r"\(((?!http).*\.png)\)", "({{options.client_files_question_url}}/\\1)", html
    )
    res = re.subn(
        r"\(((?!http).*\.gif)\)", "({{options.client_files_question_url}}/\\1)", html
    )
    res = re.subn(
        r"\(((?!http).*\.jpeg)\)", "({{options.client_files_question_url}}/\\1)", html
    )
    res = re.subn(
        r"\(((?!http).*\.jpg)\)", "({{options.client_files_question_url}}/\\1)", html
    )

    # If image files are included as html format, add {{options.client_files_question_url}}
    res = re.subn(
        r"src[\s,=]*\"(?!http)(.*\.png)",
        'src="{{options.client_files_question_url}}/\\1',
        res[0],
    )  # works
    res = re.subn(
        r"src[\s,=]*\"(?!http)(.*\.gif)",
        'src="{{options.client_files_question_url}}/\\1',
        res[0],
    )  # works
    res = re.subn(
        r"src[\s,=]*\"(?!http)(.*\.jpeg)",
        'src="{{options.client_files_question_url}}/\\1',
        res[0],
    )  # works
    res = re.subn(
        r"src[\s,=]*\"(?!http)(.*\.jpg)",
        'src="{{options.client_files_question_url}}/\\1',
        res[0],
    )  # works

    return res[0]


def validate_header(header_dict):
    # check if topic is valid (i.e. from the list of topics in the learning_outcomes repo for this subject)

    if topics.get(topic := header_dict["topic"], None) is None:
        raise ValueError(f"topic '{topic}' is not listed in the learning outcomes")


def _identify_button_html(tag: bs4.Tag) -> bool:
    """Identifies if the tag is a button

    Args:
        tag (bs4.Tag): BeautifulSoup tag

    Returns:
        bool: True if the tag is a button, False otherwise
    """
    if tag.name == "p":
        button = tag.find("button", class_="btn btn-primary")
        if button is not None:
            if button.text.strip() == "Helpful Information":
                return True
    elif tag.name == "div" and tag.attrs.get("id") == "collapseExample":
        return True
    return False

def _extract_tag_instance(soup: bs4.BeautifulSoup, tag: str, index: int = -1) -> str:
    """Extracts the specified instance of a tag from a BeautifulSoup object

    Args:
        soup (bs4.BeautifulSoup): BeautifulSoup object
        tag (str): Tag to search for
        index (int, optional): Index of the tag to extract. Defaults to -1.

    Returns:
        str: The complete contents of the of the tag (with HTML comments) or an empty string if the tag was not found
    """
    try:
        tag = soup.find_all(tag)[-1]
    except IndexError:
        return ""
    else:
        if isinstance(tag, bs4.Tag):
            try:
                while tag.markdown is not None:
                    tag.markdown.unwrap()
            except AttributeError:
                pass
            return textwrap.dedent("\n".join(line.lstrip(" ") for line in tag.prettify().splitlines()[1:-1]))
        else:
            return ""

def pl_to_md(
    question: os.PathLike[str] | str | pathlib.Path, output: os.PathLike[str] | str | pathlib.Path, file_name: str | None = None
) -> None:
    """Converts a PL question to the OPB MD format

    Args:
        question (os.PathLike[str] | str | pathlib.Path): Path to the PL question directory
        output (os.PathLike[str] | str | pathlib.Path): Path to the output directory
        file_name (str, optional): Name of the output file. Defaults to the name of last segment of the output filepath.

    Raises:
        FileNotFoundError: If the question directory does not exist
        NotADirectoryError: If the question or output path is a file
        ModuleNotFoundError: If the server.py file fails to be able to be dynamically imported
        ValueError: If the question directory is missing any of the required files, the files are not in the expected format, or the attribution at the end of the question is not recognized
        UserWarning: If the output directory already exists
        NotImplementedError: If the question contains a question type that is not yet supported
    """
    # Validate the inputs from the user
    path = pathlib.Path(question)
    if not path.exists():
        raise FileNotFoundError(f"{question} does not exist")
    if path.is_file():
        raise NotADirectoryError(
            f"{question} is not a directory, passing a file as the question directory is not supported for converting PL to MD"
        )

    output_path = pathlib.Path(output)
    if output_path.is_file():
        raise NotADirectoryError(
            f"{output} is not a directory, passing a file as the output directory is not supported for converting PL to MD"
        )
    if output_path.exists():
        warnings.warn(
            f"Directory {output!r} already exists, any files with the same name will be overwritten",
            UserWarning,
            stacklevel=2,
        )
    output_path.mkdir(parents=True, exist_ok=True)
    output_md_file = output_path / (file_name or f"{path.name}.md")

    question_file = path / "question.html"
    info_json_file = path / "info.json"
    server_py = path / "server.py"

    if not (question_file.exists() and info_json_file.exists() and server_py.exists()):
        error = "Error: the following files are missing and are required to convert a question:"
        if not question_file.exists():
            error += f"\n\tquestion.html does not exist in {question}"
        if not info_json_file.exists():
            error += f"\n\tinfo.json does not exist in {question}"
        if not server_py.exists():
            error += f"\n\tserver.py does not exist in {question}"
        raise FileNotFoundError(error)

    html = question_file.read_text(encoding="utf8")
    start = re.match(
        r"(?P<Content>.*)\n\n<!-- #{8} Start of Part 1 #{8} -->",
        html,
        re.DOTALL | re.MULTILINE,
    )
    parts: list[tuple[str, str]] = re.findall(
        r"<!-- #{8} Start of Part (?P<part>\d+) #{8} -->(?P<Content>.*)<!-- #{8} End of Part (?P=part) #{8} -->",
        html,
        re.DOTALL | re.MULTILINE,
    )
    end = re.search(
        r"<!-- #{8} End of Part \d+ #{8} -->\n\n(?!<!-- #{8} Start of Part \d+ #{8} -->)(?P<Content>.*)",
        html,
        re.DOTALL | re.MULTILINE,
    )
    md_result = "# {{ params.vars.title }}\n\n"
    header_dict = {}
    # the start and end sections are special, and don't have an associated part

    # Determine the question title, preamble, and useful info sections
    if start is not None:
        soup = BeautifulSoup(start.group("Content"), "lxml")
        if (preamble_tag := soup.find("pl-question-panel")) is not None:
            md_result += preamble_tag.text.strip()
            md_result += "\n\n"
        if len(usefuL_info := soup.find_all(_identify_button_html)) > 0:
            info = usefuL_info[1]
            if not isinstance(info, bs4.Tag):
                raise ValueError(
                    f"Detected presence of useful info button components but could not parse it for question {path.name}"
                )
            md_result += f"## Useful Info\n\n{info.text.strip()}\n\n"

    # Determine the attribution for the question
    if end is not None:
        end_md = BeautifulSoup(end.group("Content"), "lxml").contents
        if not end_md:
            raise ValueError(
                f"Could not find attribution at end of question for question {path.name}"
            )
        end_md = end_md[0].text.strip().replace("---\n", "").replace("\n", "<br>")
        attribution = None
        for possible_attribution, pl_attribution_text in _ATTRIBUTIONS.items():
            if end_md.endswith(pl_attribution_text.replace("<br>", "")):
                attribution = possible_attribution
        if attribution is None:
            raise ValueError(
                f"Could not find attribution at end of question or the found attribution was not recognized for question {path.name}:\n\n{end_md!r}"
            )
    else:
        raise ValueError(
            f"Could not find attribution at end of question for question {path.name}"
        )

    auto_tags = {"multi_part", "DEV"} | set(OPB_INPUT_TYPES.values())

    # we want to try and eagerly parse the markdown for each part so we can get the question text in
    # as early as possible, but this means we need to delay adding the part metadata to the
    # header dictionary since insert order is preserved in python dictionaries which will preserve it on yaml dump
    parts_dict = {}  

    for part, content in parts:
        # print(part, content)
        part_soup = BeautifulSoup(content, "lxml")
        # Find the input tag for the question part
        pl_input = part_soup.find(
            [
                *OPB_INPUT_TYPES.keys(),
                "pl-big-o-input",
                "pl-integer-input",
                "pl-units-input",
                "pl-order-blocks",
                "pl-threejs",
            ]
        )
        if pl_input is not None:
            pl_input = pl_input.extract()
        else:
            raise ValueError(f"Could not find input tag for part {part}")
        if isinstance(pl_input, bs4.NavigableString):
            raise ValueError(f"Could not find input tag for part {part}")
        pl_customizations = pl_input.attrs
        pl_input_type = pl_input.name
        opb_input_type = OPB_INPUT_TYPES.get(pl_input_type, None)
        if opb_input_type is None:
            raise NotImplementedError(
                f"Input type {pl_input_type} is not currently supported or is missing from the input types mapping"
            )

        # Extract the different panels and sections of the question part
        submission_panel = _extract_tag_instance(part_soup, "pl-submission-panel")
        answer_panel = _extract_tag_instance(part_soup, "pl-answer-panel")
        question_text = _extract_tag_instance(part_soup, "pl-question-panel", 0)
        
        if opb_input_type in {"multiple-choice", "checkbox", "dropdown"}:
            answers = pl_input.find_all("pl-answer")
            if len(answers) == 0:
                raise ValueError(f"Could not find any answers for part {part} in question {path.name}:\n{pl_input.prettify()}")
            answer_list = [replace_tags(answer.text.strip()) for answer in answers]
        else:
            answer_list = []

        md_result += f"## Part {part}\n\n"
        if question_text:
            md_result += f"{question_text}\n\n"

        md_result += "### Answer Section \n\n"

        if answer_list:
            for answer in answer_list:
                md_result += f"- {answer}\n"
            md_result += "\n"

        if submission_panel:
            md_result += f"### pl-submission-panel\n\n{submission_panel}\n\n"

        if answer_panel:
            md_result += f"### pl-answer-panel\n\n{answer_panel}\n\n"

        pl_customizations.pop("answers-name", None)

        for customization, value in pl_customizations.items():
            # we want to try and parse the values of the customizations as python literals
            # so that we can roundtrip them through yaml and get the same values back
            # but we don't want to fail if we can't parse them, nor do we want to try and parse non literals
            # so using ast.literal_eval is preferred over eval here
            try:
                if (val := ast.literal_eval(value)) is not Ellipsis:  # Ellipsis is ..., and is a valid python literal, but we don't want to unstringify it
                    pl_customizations[customization] = val
            except:
                pass

        parts_dict[f"part{part}"] = {
            "type": opb_input_type,
            "pl-customizations": pl_customizations,
        }

    # Parse the info.json file, and pull all possible fields from it (and populate as much of the yaml header as we can here)

    info_json: dict = json.loads(info_json_file.read_text(encoding="utf8"))
    metadata: dict = info_json.get("comment", {}).get("METADATA", {})

    md_result += f"## Rubric\n\n{metadata.get('Rubric', '')}\n\n"
    md_result += f"## Solution\n\n{metadata.get('Solution', '')}\n\n"
    md_result += f"## Comments\n\n{metadata.get('Comments', '')}\n\n"

    header_dict["title"] = info_json["title"]
    header_dict["topic"] = info_json["topic"].split(".", 1)[-1]
    header_dict["author"] = metadata.get("author", "Unknown")
    header_dict["source"] = metadata.get("source", "Unknown")
    header_dict["template_version"] = metadata.get("template_version", "Unknown")
    header_dict["attribution"] = attribution
    header_dict["gradingMethod"] = info_json.get("gradingMethod", None)
    header_dict["partialCredit"] = info_json.get("partialCredit", None)
    header_dict["singleVariant"] = info_json.get("singleVariant", None)
    header_dict["showCorrectAnswer"] = info_json.get("showCorrectAnswer", None)
    header_dict["dependencies"] = info_json.get("dependencies", None)
    header_dict["externalGradingOptions"] = info_json.get("externalGradingOptions", None)
    header_dict["workspaceOptions"] = metadata.get("workspaceOptions", None)
    header_dict["outcomes"] = metadata.get("outcomes", ["unknown"])
    header_dict["difficulty"] = metadata.get("difficulty", "undefined")
    header_dict["randomization"] = metadata.get("randomization", ["undefined"])
    header_dict["taxonomy"] = metadata.get("taxonomy", ["undefined"])
    header_dict["span"] = metadata.get("span", ["undefined"])
    header_dict["length"] = metadata.get("length", ["undefined"])
    header_dict["tags"] = sorted(list(set(info_json["tags"]) - auto_tags))  # Force deterministic order
    header_dict["assets"] = []  # Populated with _copy_assets(...) later
    header_dict["autogradeTestFiles"] = []  # Populated with _copy_assets(...) later
    header_dict["workspaceFiles"] = []  # Populated with _copy_assets(...) later
    header_dict["serverFiles"] = []  # Populated with _copy_assets(...) later

    if header_dict["tags"] == []:
        header_dict["tags"] = ["unknown"]

    # Get the module spec for the server.py file so we can load it and get the functions from it
    spec = importlib.util.spec_from_file_location(
        f"server_{path.name}", str(server_py.absolute())
    )
    # validate the file exists and a module spec was created for it
    if spec is None:
        raise ModuleNotFoundError(f"Could not find server.py file for question {path.name}")
    server = importlib.util.module_from_spec(spec) # create a module object from the spec
    loader = spec.loader # get the loader from the spec
    if loader is None: # validate the loader exists, since we need it to get the code objects for the functions
        raise ModuleNotFoundError(f"Could not load server.py file for question {path.name}")
    loader.exec_module( # load the code objects for the module into the module object by executing the module code with the loader
        server
    )  # execute the server.py file to get code objects for it that can be access with inspect

    functions = {}

    custom_start_line_no = 0

    for func_name in ("imports", "generate", "prepare", "parse", "grade"):
        func = getattr(server, func_name, None)
        if func is None:
            functions[func_name] = "pass\n"
            continue
        # We could use the builtin callable function here, but that would allow classes or callable objects (instances of classes that define __call__ somewhere in the chain)
        if not inspect.isfunction(func):
            raise ValueError(
                f"Could not find a callable function {func_name} in server.py for question {path.name} (found non callable object instead)"
            )
        signature = inspect.signature(func)
        parameters = signature.parameters
        if len(parameters) != 1:
            raise ValueError(
                f"Function {func_name} in server.py for question {path.name} does not have the correct number of arguments (expected 1, got {len(parameters)}: {signature})"
            )
        [parameter] = parameters.values()
        # the argument name should be named data, and we know there is only one argument here (if we wanted to be super precise we could check its the only posarg, but thats too pedantic)
        if parameter.name != "data":
            raise ValueError(
                f"Function {func_name} in server.py for question {path.name} does not have the correct argument name (expected 'data', got {parameter!r})"
            )
        if parameter.kind != inspect.Parameter.POSITIONAL_OR_KEYWORD:
            raise ValueError(
                f"Function {func_name} in server.py for question {path.name} does not have the correct argument kind (expected 'POSITIONAL_OR_KEYWORD', got {parameter})"
            )
        # get the source code for the function and the line number of the first line of the function
        lines, firstlineno = inspect.getsourcelines(func)
        # remove "def <name>(data):"" line, and remove unnecessary indentation to prevent the function from being indented too far in the yaml dump
        functions[func_name] = textwrap.dedent("".join(lines[1:]))
        # keep track of the last line number of the custom functions so we can get the custom functions at the end of the file
        custom_start_line_no = max(custom_start_line_no, len(lines) + firstlineno)

    # get custom functions
    func_code = inspect.getsource(server).split("\n", custom_start_line_no)[-1].strip()
    if func_code:
        functions["custom"] = func_code

    header_dict["server"] = functions

    for part, info in parts_dict.items():  # now add them in to force them to the bottom
        header_dict[part] = info

    for opt_key in (
        "gradingMethod",
        "partialCredit",
        "dependencies",
        "singleVariant",
        "showCorrectAnswer",
        "externalGradingOptions",
        "workspaceOptions",
    ):  # trim optional keys that don't exist, since they are optional and we don't want to include them if they don't exist as that would pollute the output
        if header_dict[opt_key] is None:
            del header_dict[opt_key]

    ### Get assets

    def _copy_assets(source: pathlib.Path, dest: pathlib.Path, key: str):
        dest.mkdir(parents=True, exist_ok=True)
        if source.exists():
            files = []
            # copy the files from the source directory to the output directory
            for file in source.iterdir():
                copy2(file, dest / file.name)
                files.append(str(file.relative_to(source)))

            header_dict[key] = sorted(files)
        else:
            try:
                del header_dict[key]  # remove the key if it the directory doesn't exist
            except KeyError:
                pass # ignore if the key doesn't exist, since that means we don't need to remove it

    client_assets = path / "clientFilesQuestion"
    server_assets = path / "serverFilesQuestion"
    test_assets = path / "tests"
    workspace_assets = path / "workspaceFiles"

    _copy_assets(client_assets, output_path, "assets")
    _copy_assets(server_assets, output_path, "serverFiles")
    _copy_assets(test_assets, output_path / "tests", "autogradeTestFiles")
    _copy_assets(workspace_assets, output_path / "workspace", "workspaceFiles")

    ### START Yaml Dump Configuration ###

    def str_presenter(dumper, data2):
        if len(data2.splitlines()) > 1:  # check for multiline string
            # data2 = re.sub('\\n[\s].*\\n','\n\n',data2) # THIS IS WRONG!!!
            data2 = re.sub(
                r"\n\s+\n", "\n\n", data2
            )  # # Try \s{3,} for three or more spaces
            return dumper.represent_scalar("tag:yaml.org,2002:str", data2, style="|")
        if data2.startswith("pass"):  # Check for default server.py functions
            return dumper.represent_scalar("tag:yaml.org,2002:str", data2, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data2)

    yaml.add_representer(str, str_presenter)

    def represent_none(self, _):  # This removes explicit null values, since implicit nulls are the de-facto standard for OPB
        return self.represent_scalar("tag:yaml.org,2002:null", "")

    yaml.add_representer(type(None), represent_none)

    ### END Yaml Dump Configuration ###

    # Write the completed converted question to a file
    output_md_file.write_text(
        f"---\n{yaml.dump(header_dict, sort_keys=False)}---\n{md_result}",
        encoding="utf8",
    )

    pycache = path / "__pycache__"
    if pycache.exists():
        rmtree(pycache, ignore_errors=True) # remove the pycache directory, we don't want to leave a mess of pyc files behind

