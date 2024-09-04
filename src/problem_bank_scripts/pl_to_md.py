# Author: Gavin Kendal-Freedman
# Date: 2023-08-15

import ast
import importlib.util
import inspect
import json
import os
import pathlib
import re
import textwrap
import warnings
from shutil import copy2, rmtree

import bs4
import yaml
from bs4 import BeautifulSoup

from .inputs import OPB_INPUT_TYPES, replace_tags
from .problem_bank_scripts import _ATTRIBUTIONS


_FLAGS = re.DOTALL | re.MULTILINE

START_PATTERN = re.compile(r"(?P<Content>.*)\n\n<!-- #{8} Start of Part 1 #{8} -->", _FLAGS)
PARTS_PATTERN = re.compile(r"<!-- #{8} Start of Part (?P<part>\d+) #{8} -->(?P<Content>.*)<!-- #{8} End of Part (?P=part) #{8} -->", _FLAGS)
END_PATTERN = re.compile(r"<!-- #{8} End of Part \d+ #{8} -->\n\n(?!<!-- #{8} Start of Part \d+ #{8} -->)(?P<Content>.*)", _FLAGS)
IMPORTS_PATTERN = re.compile(r"(^(?:import|from) .*?(?=\n+def))", re.DOTALL)

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
        msg = f"{question} does not exist"
        raise FileNotFoundError(msg)
    if path.is_file():
        msg = f"{question} is not a directory, passing a file as the question directory is not supported for converting PL to MD"
        raise NotADirectoryError(msg)

    output_path = pathlib.Path(output)
    if output_path.is_file():
        msg = f"{output} is not a directory, passing a file as the output directory is not supported for converting PL to MD"
        raise NotADirectoryError(msg)
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

    start = START_PATTERN.match(html)
    parts: list[tuple[str, str]] = PARTS_PATTERN.findall(html)
    end = END_PATTERN.search(html)

    md_result = "# {{ params.vars.title }}\n\n"
    header_dict = {}
    # the start and end sections are special, and don't have an associated part

    # Determine the question title, preamble, and useful info sections
    if start is not None:
        soup = BeautifulSoup(start.group("Content"), "lxml")
        if (preamble_tag := soup.find("pl-question-panel")) is not None:
            md_result += preamble_tag.text.strip()
            md_result += "\n\n"
        if len(usefuL_info := soup.find_all("pl-hidden-hints")) > 0:
            info = usefuL_info[0]
            err_msg = f"Detected presence of useful info components but could not parse it for question {path.name}" 
            if not isinstance(info, bs4.Tag):
                raise ValueError(err_msg)
            info = info.find("markdown") 
            if not isinstance(info, bs4.Tag):
                raise ValueError(err_msg)
            info = info.string
            if not isinstance(info, str):
                raise ValueError(err_msg)
            md_result += f"## Useful Info\n\n{info.strip()}\n\n"

    # Determine the attribution for the question
    if end is not None:
        end_md = BeautifulSoup(end.group("Content"), "lxml").contents
        if not end_md:
            msg = f"Could not find attribution at end of question for question {path.name}"
            raise ValueError(msg)
        end_md = end_md[0].text.strip().replace("---\n", "").replace("\n", "<br>")
        attribution = None
        for possible_attribution, pl_attribution_text in _ATTRIBUTIONS.items():
            if end_md.endswith(pl_attribution_text.replace("<br>", "")):
                attribution = possible_attribution
        if attribution is None:
            msg = f"Could not find attribution at end of question or the found attribution was not recognized for question {path.name}:\n\n{end_md!r}"
            raise ValueError(msg)
    else:
        msg = f"Could not find attribution at end of question for question {path.name}"
        raise ValueError(msg)

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
                "pl-units-input",
                "pl-order-blocks",
                "pl-threejs",
            ]
        )
        if pl_input is not None:
            pl_input = pl_input.extract()
        else:
            msg = f"Could not find input tag for part {part}"
            raise ValueError(msg)
        if isinstance(pl_input, bs4.NavigableString):
            msg = f"Could not find input tag for part {part}"
            raise ValueError(msg)  # noqa: TRY004
        pl_customizations = pl_input.attrs
        pl_input_type = pl_input.name
        opb_input_type = OPB_INPUT_TYPES.get(pl_input_type, None)
        if opb_input_type is None:
            msg = f"Input type {pl_input_type} is not currently supported or is missing from the input types mapping"
            raise NotImplementedError(msg)

        # Extract the different panels and sections of the question part
        submission_panel = _extract_tag_instance(part_soup, "pl-submission-panel")
        answer_panel = _extract_tag_instance(part_soup, "pl-answer-panel")
        question_text = _extract_tag_instance(part_soup, "pl-question-panel", 0)
        
        if opb_input_type in {"multiple-choice", "checkbox", "dropdown"}:
            answers = pl_input.find_all("pl-answer")
            if len(answers) == 0:
                msg = f"Could not find any answers for part {part} in question {path.name}:\n{pl_input.prettify()}"
                raise ValueError(msg)
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
            except:  # noqa: E722, S110
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
    header_dict["gradingMethod"] = info_json.get("gradingMethod")
    header_dict["partialCredit"] = info_json.get("partialCredit")
    header_dict["singleVariant"] = info_json.get("singleVariant")
    header_dict["showCorrectAnswer"] = info_json.get("showCorrectAnswer")
    header_dict["dependencies"] = info_json.get("dependencies")
    header_dict["externalGradingOptions"] = info_json.get("externalGradingOptions")
    header_dict["workspaceOptions"] = metadata.get("workspaceOptions")
    header_dict["outcomes"] = metadata.get("outcomes", ["unknown"])
    header_dict["difficulty"] = metadata.get("difficulty", "undefined")
    header_dict["randomization"] = metadata.get("randomization", ["undefined"])
    header_dict["taxonomy"] = metadata.get("taxonomy", ["undefined"])
    header_dict["span"] = metadata.get("span", ["undefined"])
    header_dict["length"] = metadata.get("length", ["undefined"])
    header_dict["tags"] = sorted(set(info_json["tags"]) - auto_tags)  # Force deterministic order
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
        msg = f"Could not find server.py file for question {path.name}"
        raise ModuleNotFoundError(msg)
    server = importlib.util.module_from_spec(spec) # create a module object from the spec
    loader = spec.loader # get the loader from the spec
    if loader is None: # validate the loader exists, since we need it to get the code objects for the functions
        msg = f"Could not load server.py file for question {path.name}"
        raise ModuleNotFoundError(msg)
    # load the code objects for the module into the module object by executing the module code with the loader
    # and execute the server.py file to get code objects for it that can be access with inspect
    loader.exec_module(server)

    imports = IMPORTS_PATTERN.match(server_py.read_text(encoding="utf8"))
    if imports is None:
        msg = f"Could not find imports in server.py for question {path.name}"
        raise ValueError(msg)

    functions = {"imports": imports.group().strip()+"\n"}

    custom_start_line_no = 0

    for func_name in ("generate", "prepare", "parse", "grade"):
        func = getattr(server, func_name, None)
        if func is None:
            functions[func_name] = "pass\n"
            continue
        # We could use the builtin callable function here, but that would allow classes or callable objects (instances of classes that define __call__ somewhere in the chain)
        if not inspect.isfunction(func):
            msg = f"Could not find a callable function {func_name} in server.py for question {path.name} (found non callable object instead)"
            raise ValueError(msg)
        signature = inspect.signature(func)
        parameters = signature.parameters
        if len(parameters) != 1:
            msg = f"Function {func_name} in server.py for question {path.name} does not have the correct number of arguments (expected 1, got {len(parameters)}: {signature})"
            raise ValueError(msg)
        [parameter] = parameters.values()
        # the argument name should be named data, and we know there is only one argument here (if we wanted to be super precise we could check its the only posarg, but thats too pedantic)
        if parameter.name != "data":
            msg = f"Function {func_name} in server.py for question {path.name} does not have the correct argument name (expected 'data', got {parameter!r})"
            raise ValueError(msg)
        if parameter.kind != inspect.Parameter.POSITIONAL_OR_KEYWORD:
            msg = f"Function {func_name} in server.py for question {path.name} does not have the correct argument kind (expected 'POSITIONAL_OR_KEYWORD', got {parameter})"
            raise ValueError(msg)
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

    def str_presenter(dumper, data2):  # noqa: ANN001
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

    # This removes explicit null values, since implicit nulls are the de-facto standard for OPB  
    def represent_none(self, _):  # noqa: ANN001
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

