# Author: Firas Moosvi and Graham Bovett
# Date: 2021-05-09
# This file contains many helper functions that will be used across the question bank project.


# Imports
## Loading and Saving files & others
import errno
import uuid
import json
import pathlib
from collections import defaultdict
from shutil import copy2
import re
import codecs
import importlib.util
import problem_bank_helpers as pbh
import pandas as pd
import warnings
import tempfile
import traceback
import os

## Parse Markdown
import markdown_it
import mdformat.renderer

## Dealing with YAML
import yaml

## Loading files : https://stackoverflow.com/a/60687710
import importlib.resources

from .inputs import INPUT_TYPE_PROCESSORS

## Getting file modification time
import datetime
import git

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
        elif isinstance(v, dict) and v.get("_type", None) == "sympy":
            for k2, v2 in v.items():
                if isinstance(v2, (set, list)):
                    try:
                        v[k2] = sorted(v2, key=str)
                    except:
                        pass
                elif isinstance(v2, dict):
                    v[k2] = dict(sorted(v2.items(), key=lambda i: i[0]))
                
            finaldict[k] = v
        # Somewhere around Aug 2024, something changed in how objects were serialized and anything stored as a `numpy` object wasn't correctly parsed by `pyyaml`
        # See here for our history on this: (https://moosvilab.ok.ubc.ca/moosvilab/pl/zfp63dh6hjy5zdkzemzmtzqffr)
        # And the jupyterbook PR where this was also addressed: https://github.com/jupyter-book/jupyter-book/pull/2167

        elif hasattr(v, "dtype"):
            try:
                finaldict[k] = v.item()
            except Exception:
                finaldict[k] = v
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


def read_md_problem(filepath):
    """Reads a MystMarkdown problem file and returns a dictionary of the header and body

    Args:
        filepath (str): Path of file to read.

    Returns:
        dict: In this dictionary there are four keys containing useful portions of the parsed md file:
            - ``header`` - Header of the problem file (nested dictionary).
            - ``body_parts`` - Body text of the problem file (nested dictionary).
            - ``num_parts`` - Number of parts in the problem (integer).
            - ``body_parts_split`` - Dictionary with each part split into individual components.
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
                blocks[f"block{block_count}"] = [x]
            else:
                blocks[f"block{block_count - 1}"].append(x)
                blocks[f"block{block_count}"] = [x]
    ###
    # Add -1 to the end of the last block
    blocks[f"block{block_count}"].append(len(tokens))

    # Assert statements (turn into tests!)
    assert (
        num_titles == 1
    ), f"I see {num_titles} Level 1 Headers (#) in this file, there should only be one!"
    assert (
        block_count >= 1
    ), f"I see {block_count - 1} Level 2 Headers (##) in this file, there should be at least 1"

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


def _remove_l3_headers(text: str, remove: set[str]) -> str:
    """Removes specific level 3+ headers from a markdown string; useful for removing sections like pl-answer-panel and pl-submission panel for the public version of the site.
    
    Args:
        text (str): Markdown text to process
        remove (set[str]): Set of strings to remove from the markdown text

    Returns:
        str: Processed markdown text
    """
    tokens_to_rerender = []
    next_is_new_header_text = False
    current_header_text = None

    mdit = markdown_it.MarkdownIt()
    env = {}
    tokens = mdit.parse(text, env)

    for token in tokens:
        if token.type == "heading_open":
            next_is_new_header_text = True
            tokens_to_rerender.append(token)
            current_header_text = None
            continue

        if next_is_new_header_text:
            next_is_new_header_text = False
            current_header_text = token.content
        
            if current_header_text in remove:
                tokens_to_rerender.pop()
        
        if current_header_text not in remove:
            tokens_to_rerender.append(token)
    
    return (
        mdformat.renderer.MDRenderer()
        .render(tokens_to_rerender, mdit.options, env)
        .replace(r"\\", "\\")
    )


def dict_to_md(md_dict: dict[str, str], remove_keys=None):
    """Takes a nested dictionary (e.g. output of read_md_problem()) and returns a multi-line string  that can be written to a file (after removing specified keys).
    Args:
        md_dict (dict): A nested dictionary, for e.g. the output of `read_md_problem()`
        remove_keys (list[str], optional): Any keys to remove from the dictionary, for instance solutions. Defaults to removing no keys.

    Returns:
        str: A multi-line string that can be written to a file.
    """

    # md_dict: dict[str, str] = defdict_to_dict(md_dict, {})

    # Question Title and Preamble
    md_string = md_dict.pop("title", "")
    md_string += md_dict.pop("preamble", "")

    _remove = set() if remove_keys is None else set(remove_keys)

    for heading, content in md_dict.items():
        if heading in _remove:
            continue
        
        if _remove and "###" in content:
            md_string += "\n" + _remove_l3_headers(content, _remove)
        else:
            md_string += "\n" + content

    return md_string


## Functions from md-to-pl


def write_info_json(output_path, parsed_question, modified_time: str | None = None):
    """
    Args:
        output_path (Path): [description]
        parsed_question (dict]): [description]
        modified_time (str | None, optional): Last commit timestamp or modified timestamp of the file
    """

    # Deal with optional tags in info.json
    # optional = ""

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

    if (difficulties := parsed_question["header"].get("difficulty", ["undefined"])) != ["undefined"]:
        if not isinstance(difficulties, list):
            difficulties = [difficulties]
        auto_tags.extend(difficulty.lower() for difficulty in difficulties)

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
            msg = "workspaceOptions must contain image, port, and home keys"
            raise SyntaxError(msg)
        if not isinstance(info_json["workspaceOptions"]["port"], int):
            msg = f"workspaceOptions.port must be an integer, got {type(info_json['workspaceOptions']['port'])!r} instead"
            raise TypeError(msg)

    if modified_time:
        info_json["comment"] = {"lastModified": modified_time}

    # End add tags
    with pathlib.Path(output_path / "info.json").open("w") as output_file:
        json.dump(info_json, output_file, indent=4)


def assemble_server_py(parsed_question, location):
    """Assembles a string version of the server.py file from the YAML header of the md file.

    Args:
        parsed_question (dict): dictionary that is created upon reading of the md problem.
        location (string): 'local' or 'prairielearn' ; the import statements are different depending on if it's local or on a PL server.
    """

    server_dict = parsed_question["header"]["server"].copy()

    if location == "local":
        # This is needed to run this locally compared to when it gets run on a PL server
        server_dict["imports"] = parsed_question["header"]["server"]["imports"].replace(
            "import prairielearn as pl",
            "import problem_bank_scripts.prairielearn as pl",
        )

    if "import problem_bank_helpers as pbh" not in server_dict["imports"]:
        server_dict["imports"] += "\nimport problem_bank_helpers as pbh # Added in by problem bank scripts" 

    server_py = ""

    server_py += server_dict.get("imports", "") + "\n"

    for function, code in server_dict.items():
        indented_code = code.replace("\n", "\n    ")
        # With the custom header, add functions to server.py as-is
        if function == "custom":
            server_py += f"{code}"
        elif function == "imports":
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
        return True

    none_of_the_above = parsed_question["header"][part_name]["pl-customizations"].get("none-of-the-above", "false")

    return none_of_the_above in {"correct", "random"}


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


_ATTRIBUTIONS: dict[str, str] = json.loads(importlib.resources.files("problem_bank_scripts").joinpath("attributions.json").read_bytes())
KNOWN_ATTRIBUTIONS: list[str] = list(_ATTRIBUTIONS.keys())

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
            f"`Attribution` value of {attribution} is not recognized.",
            f"Currently, the only possible values are: {KNOWN_ATTRIBUTIONS}.",
            "You need to update your md file and fix the `attribution` in the header",
        )
        raise


def process_question_md(
    source_filepath: os.PathLike[str] | str,
    output_path: os.PathLike[str] | str | None = None,
    instructor: bool = False,
    ) -> None:
    """Processes an OPB markdown file and writes the output to a file.

    Args:
        source_filepath (os.PathLike[str] | str): Path to the markdown file to be processed.
        output_path (os.PathLike[str] | str, optional): Path to the output file. Defaults to None.
        instructor (bool, optional): Flag to determine if the output is for an instructor or not. Defaults to False.
            This determines if the solutions are included in the output or not.
    """
    try:
        source_filepath = pathlib.Path(source_filepath).resolve(strict=True)
    except:
        print(f"{source_filepath} - File does not exist.")
        raise

    if output_path is None:
        path_replace = "output/instructor" if instructor else "output/public"

        if "source" in (_src := str(source_filepath)):
            output_path = pathlib.Path(_src.replace("source", path_replace))
        else:
            msg = f"Check the source filepath; it does not have 'source' in it: {source_filepath}"
            raise ValueError(msg)
    else:
        ## TODO: Make this a bit more robust, perhaps by switching encodings!?
        output_path = pathlib.Path(output_path)

    # deal with multi-line strings in YAML Dump
    ## Code copied from here: https://stackoverflow.com/a/33300001/2217577

    def str_presenter(dumper, data2):
        if len(data2.splitlines()) > 1:  # check for multiline string
            # data2 = re.sub('\\n[\s].*\\n','\n\n',data2) # THIS IS WRONG!!!
            data2 = re.sub(
                r"\n\s+\n", "\n\n", data2
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
    server = {}
    data2 = pbh.create_data2()

    with tempfile.TemporaryDirectory(suffix=f"_{output_path.stem}", ignore_cleanup_errors=True) as dirpath:
        file = pathlib.Path(dirpath).joinpath("server.py")
        file.write_text(server_py, encoding="utf8")
        try:
            code = compile(server_py, file.as_posix(), "exec")
            exec(code, server)        
            server["generate"](data2)
        except Exception as e:
            msg = f"Error in running the server code, please review the below traceback: \n\n{traceback.format_exc()}"
            raise type(e)(msg) from None

    #################################################################################

    # Remove the solutions from the server section
    if instructor is False:
        # Remove python solution from the public view
        header.pop("server", None)

        # Remove correct answers from the data2 dict
        data2_sanitized = defdict_to_dict(data2, {})
        data2_sanitized = defdict_to_dict(remove_correct_answers(data2_sanitized), {})

        # Update the YAML header to add substitutions
        header.update({"myst": {"substitutions": data2_sanitized} })

        # Update the YAML header to add substitutions, unsort it, and process for file
        header_yml = yaml.dump(header, sort_keys=False, allow_unicode=True)

        # Write the YAML to a file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            "---\n"
            + header_yml
            + "---\n"
            + dict_to_md(
                body_parts,
                remove_keys=[
                    "Rubric",
                    "Solution",
                    "Comments",
                    "pl-submission-panel",
                    "pl-answer-panel",
                ],
            )
            + "\n## Attribution\n\n"
            + process_attribution(header.get("attribution")),
            encoding="utf8",
        )

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
                    
    # Move workspace files
    files_to_copy = header.get("workspaceTemplates")
    if files_to_copy:
        pl_path = output_path.parent / "workspaceTemplates"
        pl_path.mkdir(parents=True, exist_ok=True)
        for file in files_to_copy:
            try:
                copy2(pathlib.Path(source_filepath).parent / "workspaceTemplates" / file, pl_path / file)
            except (FileExistsError, FileNotFoundError, IsADirectoryError, PermissionError) as e:
                os_errors.append(str(e))

    if os_errors:
        error_msg = "\n    ".join(os_errors)
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"Error(s) copying specified files:\n    {error_msg}")


def process_question_pl(
    source_filepath: os.PathLike[str] | str,
    output_path: os.PathLike[str] | str | None = None,
    dev: bool = False,
    ):
    """Processes an OPB markdown file and converts it to a prairielearn compatible question.

    Args:
        source_filepath (os.PathLike[str] | str): Path to the markdown file to be processed.
        output_path (os.PathLike[str] | str, optional): Path to the output file. Defaults to None.
        dev (bool, optional): Flag to determine if the question is under development. Defaults to False.
    """
    try:
        _path = pathlib.Path(source_filepath).resolve()
    except:
        print(f"{source_filepath} - File does not exist.")
        raise

    if not _path.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), source_filepath)
    
    if not _path.is_file():
        raise IsADirectoryError(errno.EISDIR, os.strerror(errno.EISDIR), source_filepath)

    if output_path is None:
        if "source" in str(_path):
            output_path = pathlib.Path(_path.as_posix().replace("source", "output/prairielearn")).parent
        else:
            msg = f"Check the source filepath; it does not have 'source' in it: {source_filepath}"
            raise ValueError(msg)
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
    server = {}
    data2 = pbh.create_data2()

    with tempfile.TemporaryDirectory(suffix=f"_{output_path.stem}", ignore_cleanup_errors=True) as dirpath:
        file = pathlib.Path(dirpath).joinpath("server.py")
        file.write_text(server_py, encoding="utf8")
        try:
            code = compile(server_py, file.as_posix(), "exec")
            exec(code, server)        
            server["generate"](data2)
        except Exception as e:
            msg = f"Error in running the server code, please review the below traceback: \n\n{traceback.format_exc()}"
            raise type(e)(msg) from None

    #################################################################################

    if dev:
        tags = parsed_q["header"].get("tags", [])
        tags.append("DEV")
        parsed_q["header"]["tags"] = tags

    try:
        repo = git.Repo(_path.parent, search_parent_directories=True)
        repo.working_dir
        commit = next(repo.iter_commits(None, source_filepath, max_count=1))
        modified_time = commit.committed_datetime
    except:
        modified_time = datetime.datetime.fromtimestamp(_path.stat().st_mtime, tz=datetime.timezone.utc)

    # Write info.json file
    write_info_json(output_path, parsed_q, modified_time.strftime("%Y-%m-%dT%H:%M:%S%z"))

    # Question Preamble
    preamble = parsed_q["body_parts"].get("preamble", None)
    # TODO: Remove Debugging print statement
    # print(f"premable: {preamble}")

    if preamble:
        question_html = f"<pl-question-panel>\n<markdown>\n{ preamble }\n</markdown>\n</pl-question-panel>\n\n"
    else:
        question_html = ""

    # Useful info panel

    if (useful_info := parsed_q["body_parts"].get("Useful_info", None)):
        useful_info = useful_info.replace("## Useful Info\n", "")
        question_html += f"""<pl-hidden-hints>
<pl-hint hint-name="Helpful Information"><markdown>{useful_info}</markdown></pl-hint>
</pl-hidden-hints>
"""

    # Single and Multi-part question construction

    for pnum in range(1, parsed_q["num_parts"] + 1):
        part = "part" + f"{pnum}"
        q_type = parsed_q["header"][part]["type"]

        question_html += f"\n<!-- ######## Start of Part {pnum} ######## -->\n\n"

        if parsed_q["num_parts"] > 1:
            question_html += f'<pl-card header="{parsed_q["body_parts_split"][part]["title"]}">\n'

        if "multiple-choice" in q_type and not validate_multiple_choice(part,parsed_q,data2):
                msg = (
                    f"Multiple choice question {part} does not have a correct answer and "
                    "the pl-customization `none-of-the-above` was not set to `correct` or `random`."
                )
                raise ValueError(msg)
        
        converter = INPUT_TYPE_PROCESSORS.get(q_type)
        if converter is None:
            msg = f"The question type ({q_type}) is not yet implemented."
            raise NotImplementedError(msg)
        else:
            question_html += f"{converter(part,parsed_q,data2)}"

        if parsed_q["num_parts"] > 1:
            question_html += "</pl-card>\n"

        # Add pl-submission-panel and pl-answer-panel (if they exist)
        subm_panel = parsed_q["body_parts_split"][part].get("pl-submission-panel", None)
        q_panel = parsed_q["body_parts_split"][part].get("pl-answer-panel", None)

        if subm_panel:
            question_html += f"\n<pl-submission-panel>{subm_panel}</pl-submission-panel>\n"
        if q_panel:
            question_html += f"\n<pl-answer-panel>{q_panel}</pl-answer-panel>\n"


        question_html += f"\n<!-- ######## End of Part {pnum} ######## -->\n"

    # Add Attribution
    question_html += f"\n<pl-question-panel>\n<markdown>\n---\n{process_attribution(parsed_q['header'].get('attribution'))}\n</markdown>\n</pl-question-panel>\n"

    # Fix Latex over-escaping from mdformat (i.e. _, [, and ]being replaced with \_, \[, and \])
    # See https://github.com/open-resources/problem_bank_scripts/issues/89
    # Also see https://github.com/open-resources/problem_bank_scripts/pull/92
    question_html = question_html.replace("\\_", "_").replace("\\[","[").replace("\\]","]")
    question_html = question_html.replace("\\*", "*").replace("\\<","<").replace("\\`","`")

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
    
    # Move workspace files
    files_to_copy = parsed_q["header"].get("workspaceTemplates")
    if files_to_copy:
        pl_path = output_path / "workspaceTemplates"
        pl_path.mkdir(parents=True, exist_ok=True)
        for file in files_to_copy:
            try:
                copy2(pathlib.Path(source_filepath).parent / "workspaceTemplates" / file, pl_path / file)
            except (FileExistsError, FileNotFoundError, IsADirectoryError, PermissionError) as e:
                os_errors.append(f"{e} {e.filename}")

    if os_errors:
        error_msg = "\n    ".join(os_errors)
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"Error(s) copying specified files:\n    {error_msg}")


def pl_image_path(html):
    """Adds ``{{options.client_files_question_url}}`` directory before the path automatically"""

    ext_group = r"((?!http).*\.(?:png|gif|jpg|jpeg))"
    base_repl = r"{{options.client_files_question_url}}/\1"

    # If image files are included as markdown format, add {{options.client_files_question_url}}
    res = re.sub(rf"\({ext_group}\)", rf"({base_repl})", html)

    # If image files are included as html format, add {{options.client_files_question_url}}
    return re.sub(rf"src[\s,=]*\"{ext_group}", f'src="{base_repl}', res)


def validate_header(header_dict):
    # check if topic is valid (i.e. from the list of topics in the learning_outcomes repo for this subject)

    if topics.get(topic := header_dict["topic"], None) is None:
        msg = f"topic '{topic}' is not listed in the learning outcomes"
        raise ValueError(msg)

