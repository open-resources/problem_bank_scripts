from .utils import replace_tags


__all__ = [
    "process_matching",
    "process_file_upload",
    "process_workspace",
    "process_custom_input",
]


def process_matching(part_name: str, parsed_question: dict, data_dict: dict) -> str:
    """Processes markdown format matching questions and returns PL HTML
    
    Arguments
    ---------
        part_name : str
            Name of the question part being processed (e.g., part1, part2, etc...)
        parsed_question : dict
            Dictionary of the MD-parsed question (output of ``read_md_problem``)
        data_dict : dict
            Dictionary of the ``data`` dict created after running server.py using ``exec``

    Returns
    -------
        html : str
            A string of HTML that is part of the final PL question.html file.
    """
    print("Processing matching question...")

    html = f"<pl-question-panel>\n<markdown>{parsed_question['body_parts_split'][part_name]['content']}</markdown>\n</pl-question-panel>\n\n"

    pl_customizations = " ".join(
        [
            f'{k} = "{v}"'
            for k, v in parsed_question["header"][part_name]["pl-customizations"].items()
        ]
    )  # PL-customizations
    html += f'<pl-matching answers-name="{part_name}_matching" {pl_customizations} >\n'

    options = ""
    statements = ""
    ## Note: `|@`` gets converted into `{{` and `@|`` gets converted to `}}` by `replace_tags()`
    for a in data_dict["params"][f"{part_name}"]:
        if "option" in a:
            value = f"|@|@ params.{part_name}.{a}.value @|@|"

            if name := data_dict["params"][f"{part_name}"][a].get("name"):
                options += f"\t<pl-option name='{name}' > {value} </pl-option>\n"
            else:
                options += f"\t<pl-option> {value} </pl-option>\n"

        if "statement" in a:
            matches_with = f"|@ params.{part_name}.{a}.matches @|"
            value = f"|@|@ params.{part_name}.{a}.value @|@|"

            statements += f"\t<pl-statement match= '{matches_with}' > {value} </pl-statement>\n"

    html += statements
    html += options

    html += "</pl-matching>\n"

    return replace_tags(html)


def process_file_upload(part_name: str, parsed_question: dict, data_dict: dict) -> str:
    """Processes markdown format of file-upload questions and returns PL HTML
    
    Arguments
    ---------
        part_name : str
            Name of the question part being processed (e.g., part1, part2, etc...)
        parsed_question : dict
            Dictionary of the MD-parsed question (output of ``read_md_problem``)
        data_dict : dict
            Dictionary of the ``data`` dict created after running server.py using ``exec``

    Returns
    -------
        html : str
            A string of HTML that is part of the final PL question.html file.
    """
    pl_customizations = " ".join(
        [
            f'{k} = "{v}"'
            for k, v in parsed_question["header"][part_name]["pl-customizations"].items()
        ]
    )  # PL-customizations

    html = f"<pl-question-panel>\n<markdown>{parsed_question['body_parts_split'][part_name]['content']}</markdown>\n</pl-question-panel>\n\n"

    html += f"<pl-file-upload {pl_customizations} > </pl-file-upload>"

    html += "<pl-submission-panel>\n\t<pl-file-preview></pl-file-preview>\n\t<pl-external-grader-results></pl-external-grader-results>"

    # TODO: remove this! because automatic feedback will be added
    html += "\n\t|@ #feedback.manual @| \n\t<p>Feedback from course staff:</p>\n\t<markdown>|@|@ feedback.manual @|@|</markdown>\n\t|@ /feedback.manual @|\n</pl-submission-panel>"

    # TODO: Add better support for what students see when they upload a file where many are possible. Currently: Error: The following required files were missing: *.jpg, *.pdf, foo.py, bar.c, filename space.txt
    # TODO: Add support for wildcard *.png
    # TODO: Add better message telling students the question needs to be manually graded.

    return replace_tags(html)


def process_workspace(part_name: str, parsed_question: dict, data_dict: dict) -> str:
    """Processes markdown format of workspace questions and returns PL HTML
    
    Arguments
    ---------
        part_name : str
            Name of the question part being processed (e.g., part1, part2, etc...)
        parsed_question : dict
            Dictionary of the MD-parsed question (output of ``read_md_problem``)
        data_dict : dict
            Dictionary of the ``data`` dict created after running server.py using ``exec``

    Returns
    -------
        html : str
            A string of HTML that is part of the final PL question.html file.
    """
    if (
        "pl-customizations" in parsed_question["header"][part_name]
        and len(parsed_question["header"][part_name]["pl-customizations"]) > 0
    ):
        msg = "pl-customizations are not supported for workspace questions"
        raise ValueError(msg)

    html = f"<pl-question-panel>\n<markdown>{parsed_question['body_parts_split'][part_name]['content']}</markdown>\n</pl-question-panel>\n\n"

    html += "<pl-workspace></pl-workspace>\n<pl-submission-panel>"

    if parsed_question["header"][part_name].get("gradingMethod", None) == "External":
        html += "\n<pl-external-grader-results></pl-external-grader-results>\n<pl-file-preview></pl-file-preview>\n</pl-submission-panel>"
    else:
        html += "\n<ul>\n\t|@ #feedback.results @| \n\t<li>|@ . @|</li>\n\t|@ /feedback.results @|\n</ul>\n</pl-submission-panel>"

    return replace_tags(html)


def process_custom_input(part_name: str, parsed_question: dict, data_dict: dict) -> str:
    """Processes markdown format custom input questions and returns PL HTML
    
    Arguments
    ---------
        part_name : str
            Name of the question part being processed (e.g., part1, part2, etc...)
        parsed_question : dict
            Dictionary of the MD-parsed question (output of ``read_md_problem``)
        data_dict : dict
            Dictionary of the ``data`` dict created after running server.py using ``exec``

    Returns
    -------
        html : str
            A string of HTML that is part of the final PL question.html file.
    """

    return f"<pl-question-panel>\n<markdown>{parsed_question['body_parts_split'][part_name]['content']}</markdown>\n</pl-question-panel>\n\n"
