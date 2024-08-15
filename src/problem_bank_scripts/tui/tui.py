import importlib.resources
import json
import os
import pathlib
import shlex
import shutil
import subprocess
import traceback
from copy import deepcopy

import questionary


from problem_bank_scripts import KNOWN_ATTRIBUTIONS, process_question_pl
from problem_bank_scripts.scripts.lint_server import main as lint_server
from .utils import write_json, read_json, split_comma, string_is_int, string_is_number_range, get_number_suffix, string_is_approx_numeric, string_num_digits_after_decimal, remove_edge_non_numeric
from .generate_questions import generate_true_false_choices, generate_yes_no_choices
from .write_md import write_md
from .inputs import ask_int

KNOWN_QUESTIONS: dict[str, dict] = {
    file.stem: json.loads(file.read_bytes())
    for file in importlib.resources.files("problem_bank_scripts.tui").glob("known_questions/*.json")  # pyright: ignore[reportAttributeAccessIssue]
}

ch1_matching_type = {
    "type": "matching",
    "options": [
        '"Not a variable in the study"',
        '"Numerical and discrete variable"',
        '"Numerical and continuous variable"',
        '"Categorical"',
        # 'option4': 'Categorical and not ordinal variable',
    ],
    "statements": [
        {"value": '"Statement 1"', "matches": "Not a variable in the study"},
        {"value": '"Statement 2"', "matches": "Numerical and discrete variable"},
        {"value": '"Statement 3"', "matches": "Numerical and continuous variable"},
        {"value": '"Statement 4"', "matches": "Categorical"},
    ],
}


def generate_given_choices(options: list[str], answer: str, question: str, use_gpt: bool):
    if answer:
        answer = answer.strip().lower()
    # Count how many empty string options
    num_empty = len([x for x in options if not x.strip()])
    options = [x.strip() for x in options if x.strip()]
    if num_empty > 0:
        if use_gpt:
            from .gpt import ask_mc_options

            options += ask_mc_options(options, answer, question, num_empty)
        else:
            options += ["Placeholder"] * num_empty

    choices = [
        {"value": f'"{option}"', "correct": False, "feedback": '"Try again please!"'}
        for option in options
    ]

    correct = len(choices)
    if answer in options:
        correct = options.index(answer)
    else:
        choices.append({})
    choices[correct]["value"] = f'"{answer}"'
    choices[correct]["correct"] = True
    choices[correct]["feedback"] = '"Correct!"'
    # TODO: replace empty options with GPT generated text
    return choices


QUESTION_TYPES = {
    "multiple-choice": {},
    "number-input": {},
    "longtext": {},
    "dropdown": {"type": "multiple-choice", "display": "dropdown"},
    "checkbox": {},
    "matrix": {"type": "matrix-component-input"},
    "matching": {},
    "true-false": {"type": "multiple-choice"},
    "yes-no": {"type": "multiple-choice", "choices": generate_yes_no_choices()},
    "file-upload": {},
    "integer-input": {},
    "symbolic-input": {},
}

def convert_solution_to_type(solution: str, key: str):
    if key in {"number-input", "integer-input"}:
        # remove ',' from solution
        return remove_edge_non_numeric(solution.replace(",", ""))
    if key in {"matrix", "matrix-component-input"}:
        if solution.startswith('[') and solution.endswith(']'):
            return solution
        if '-' in solution and len(solution.split('-')) == 2:
            split = solution.split('-')
            return f'[{split[0].strip()}, {split[1].strip()}]'
        return solution
    return solution

def other_asks(part: dict, solution: str, use_gpt: bool, exercise: dict | None = None):
    key = part["type"]
    question = part["question"]
    info = deepcopy(QUESTION_TYPES[key])
    if "type" not in info:
        info["type"] = key
    match key:
        case "multiple-choice" | "dropdown" | "checkbox":
            options: list[str] = []
            # answer = questionary.text("Solution").ask()
            num_options = ask_int("Number of options", default=4)
            for i in range(num_options):
                options.append(
                    questionary.text(f"Option {i+1}. Press enter to generate with GPT.").ask()
                )
            info["choices"] = generate_given_choices(options, solution, question, use_gpt)
        case "yes-no":
            info["choices"] = generate_yes_no_choices(solution)
            info["fixed-order"] = "true"
        case "true-false":
            info["choices"] = generate_true_false_choices(solution)
            info["fixed-order"] = "true"
        case "number-input" | "matrix":
            digits = ask_int("Digits", default=str(string_num_digits_after_decimal(solution)))
            info["digits"] = digits
            prefix = questionary.text("Prefix", default="$p=$").ask()

            if prefix:
                info["label"] = prefix
            suffix = questionary.text("Suffix", default=get_number_suffix(solution)).ask()

            if suffix:
                info["suffix"] = suffix
            if use_gpt:
                from .gpt import ask_number_code

                info["code"] = ask_number_code(question, solution) # code is optional parameter
            if key == "matrix" and exercise is not None:
                if "imports" not in exercise:
                    exercise["imports"] = []
                exercise["imports"].append("import numpy as np")
                exercise["imports"].append("import prairielearn as pl")
        case "matching":
            statements_str = questionary.text("List the statements, comma separated").ask()
            statements = split_comma(statements_str)
            info["statements"] = []
            for statement in statements:
                if statement:
                    info["statements"].append(
                        {
                            "value": statement,
                            "matches": questionary.text(f"{statement} matches").ask(),
                        }
                    )
            extra_options_str = questionary.text(
                "List the extra (unused) options, comma separated"
            ).ask()
            info["options"] = split_comma(extra_options_str)
        case "integer-input":
            prefix = questionary.text("Prefix", default="$p=$").ask()
            if prefix:
                info["label"] = prefix
        case "symbolic-input":
            prefix = questionary.text("Prefix", default="$p=$").ask()
            if prefix:
                info["label"] = prefix
            custom_functions = questionary.text('custom_functions (ex. "N") (optional)').ask()
            if custom_functions:
                info["custom_functions"] = custom_functions
            variables_str = questionary.text('variables (ex. "mu, sigma")').ask()
            info["variables"] = variables_str
            if exercise is not None:
                if "imports" not in exercise:
                    exercise["imports"] = []
                exercise["imports"].append("import prairielearn as pl")
                exercise["imports"].append("from sympy import sp")
        case _:
            print("No other asks for", key)
    part["info"] = info


def extract_variables(text: str, variables: dict) -> str:
    res = ""
    open_i = None
    for i in range(len(text)):
        if text[i] == "{":
            open_i = i
        if open_i is None:  # has to be in the middle
            res += text[i]
        if text[i] == "}" and open_i is not None:
            var = text[open_i+1:i]  # fmt: skip
            name = ""
            value = None
            split = var.split(":")
            name = split[0].strip()
            if len(split) > 1:
                value = split[1].strip()
            if value:
                variables[name] = value
            res += f"{{{{ params.{name} }}}}"
            open_i = None
    if open_i is not None:
        msg = "Unmatched {"
        raise ValueError(msg)
    return res.strip()


def guess_question_type_from_solution(solution: str) -> str | None:
    # return value must be key of QUESTION_TYPES
    if solution.lower() in ["true", "false"]:
        return "true-false"
    if solution.lower() in ["yes", "no"]:
        return "yes-no"
    if string_is_number_range(solution) or (solution.startswith('[') and solution.endswith(']')):
        return "matrix"
    if string_is_int(solution):
        return "integer-input"
    if string_is_approx_numeric(solution):
        return "number-input"
    if solution.isalpha():
        return "multiple-choice"
    return None


def ask_if_not_exists(
    exercise: dict,
    key: str,
    question: str,
    variables: dict,
    saved: pathlib.Path,
    default="",
    parser=lambda x: x,
):
    if key not in exercise:
        value = parser(questionary.text(question, default=default).ask())
        if isinstance(value, str):
            value = extract_variables(value, variables=variables)
        exercise[key] = value
        write_json(exercise, saved)
    return exercise[key]


def set_default(exercise: dict, key: str, value: str | list, saved: pathlib.Path):
    if key not in exercise:
        exercise[key] = value
        write_json(exercise, saved)
    return exercise[key]


def run_tui(
    *,
    create_pr: bool = False,
    use_gpt: bool = False,
    saved: pathlib.Path = pathlib.Path("saved.json"),
):
    exercise = {}
    variables = {}
    if saved.exists() and questionary.confirm("Would you like to use saved data?").ask():
        exercise = read_json(saved)
        if "variables" in exercise:
            variables = exercise["variables"]
    try:
        set_default(exercise, key="assets", value=[], saved=saved)

        textbook = exercise.get("attribution", None)
        if textbook is None:
            textbook = os.environ.get("TEXTBOOK") or questionary.select(
                message="What textbook is this from? (Select standard if not from any on the list)",
                choices=KNOWN_ATTRIBUTIONS,
            ).ask()
            exercise["attribution"] = textbook

        textbook_file = KNOWN_QUESTIONS.get(textbook)

        chapter = ask_if_not_exists(
            exercise, key="chapter", question="Chapter", saved=saved, variables=variables
        )

        question_numbers = ask_if_not_exists(
            exercise,
            key="question_numbers",
            question="Question numbers (comma separated)",
            variables=variables,
            parser=lambda x: [int(s) for s in split_comma(x)],
            saved=saved,
        )

        if textbook_file is not None:
            print(f"Loading known question and solution data for {textbook!r}")
            file_question_index = next(
                i
                for i, v in enumerate(textbook_file["questions"][str(chapter)])
                if any(x["questionNumber"] == question_numbers[0] for x in v["parts"])
            )
            file_question = textbook_file["questions"][str(chapter)][file_question_index]
            file_question["parts"] = [
                x for x in file_question["parts"] if x["questionNumber"] in question_numbers
            ]
            file_questions = file_question["parts"]
            file_solutions = {
                str(key): textbook_file["solutions"][str(chapter)][str(key)]
                for key in question_numbers
                if str(key) in textbook_file["solutions"][str(chapter)]
            }
            print(
                "here is a link to the question section (or nearby)\n", file_question["sectionHref"]
            )
        else:
            print(f"No known question and solution data known for {textbook!r}")
            file_question = {}
            file_questions = []
            file_solutions = {}

        branch_name = (
            f"{textbook.split('-')[0]}_C{chapter}{''.join(f'_Q{x}' for x in question_numbers)}"
        )
        exercise["branch_name"] = branch_name
        exercise["path"] = f"{branch_name}.md"
        issues = ask_if_not_exists(
            exercise,
            key="issues",
            question="What issues does this resolve (comma separated, numbers only)",
            variables=variables,
            parser=split_comma,
            saved=saved,
        )
        title = ask_if_not_exists(
            exercise, key="title", question="Title", variables=variables, saved=saved
        )
        default_description = file_question.get("description", "")
        if len(file_questions) == 1:
            if default_description and file_questions[0]["questionText"]:
                default_description = default_description + '\n'
            default_description = default_description + file_questions[0]["questionText"]
        desc = ask_if_not_exists(
            exercise,
            key="description",
            question="Description",
            saved=saved,
            variables=variables,
            default=default_description, # add questionText
        )

        if textbook_file is not None:
            part_tables = [
                {"matrix": table} for p in file_questions if "tables" in p for table in p["tables"]
            ]
            solution_tables = [
                {"matrix": table}
                for p in file_solutions.values()
                if "tables" in p
                for table in p["tables"]
            ]
            exercise["tables"] = part_tables + solution_tables
            if "tables" in file_question:
                # next((True for x in v["parts"] if x["questionNumber"]==question_numbers[0]), False)
                exercise["tables"] += file_question["tables"]
            if len(exercise["tables"]) > 0:
                print(
                    f"this question has {len(exercise['tables'])} table(s), we've included it already. Only select it below (in 'Select extra') if you have additional tables."
                )
            else:
                del exercise["tables"]

        if "extras" not in exercise:
            exercise["extras"] = questionary.checkbox(
                "Select extra",
                choices=[
                    "table",
                    "image",
                    "graph",
                    "matrix",
                ],
            ).ask()

        if "image" in exercise["extras"]:
            exercise["assets"] += split_comma(
                questionary.text("Image paths (comma separated)").ask()
            )
        if "table" in exercise["extras"]:
            num_tables = ask_int("How many tables", default=1)
            tables = []
            for i in range(num_tables):
                table = {"matrix": []}
                table_str: str = questionary.text("Paste in table").ask()
                table["first_row_is_header"] = questionary.confirm(
                    "Is the first row a header?"
                ).ask()
                table["first_col_is_header"] = questionary.confirm(
                    "Is the first column a header?"
                ).ask()
                rows = table_str.split("\n")
                for row_str in rows:
                    row_str = row_str.strip()  # ruff # noqa: PLW2901
                    if not row_str:
                        continue
                    row = [x.strip() for x in row_str.split("\t")]
                    print("row", row)
                    table["matrix"].append(row)
                tables.append(table)
                # [["a", "b", "c"], ["x", "1"]]
            exercise["tables"] = tables
        if "matrix" in exercise["extras"]:
            # if has_matrix:
            #   result += ['<pl-matrix-latex params-name="matrixA"></pl-matrix-latex>']
            num_tables = ask_int("How many matrices", default=1)
            matrices = []
            for i in range(num_tables):
                matrices.append(questionary.text(f"Matrix {i+1}? ex. [1,2,3]").ask())
            exercise["matrices"] = matrices
        if "graph" in exercise["extras"]:
            num_graphs = ask_int(
                "How many graphs",
                default=1 if "graphs" not in exercise else len(exercise["graphs"]),
            )
            exercise["graphs"] = exercise.get("graphs", [])
            graphs_done = len(exercise["graphs"])
            for i in range(graphs_done, num_graphs):
                graph: dict = {
                    "variables": {},
                }
                graph["type"] = questionary.select(
                    f"Graph {i+1} type",
                    choices=["bar", "line", "scatter", "box plot", "histogram", "other"],
                    default="box plot",
                ).ask()
                if graph["type"] == "box plot":
                    is_vertical = questionary.confirm("Is the box plot vertical?").ask()
                    graph["is_vertical"] = is_vertical
                    num_box = ask_int("Number of box plots", default=1)
                    if num_box > 1:
                        graph["data"] = [[None] for i in range(num_box)]
                    else:
                        graph["data"] = [None]
                default_graph_dict = {
                    "box plot": "q3",
                    "histogram": "num_bins",
                }
                known_info = questionary.checkbox(
                    "Select known/controlled params",
                    choices=[
                        "title",
                        "x_label",
                        "y_label",
                        "data",
                        "mean",
                        "median",
                        "std",
                        "num_bins",
                        "min_val",
                        "max_val",
                        "q1",
                        "q3",
                        "whislow",
                        "whishigh",
                        "sample_size",
                    ],
                    default=default_graph_dict.get(graph["type"], None),
                ).ask()
                if "median" in known_info and "mean" in known_info:
                    print("Cannot have both mean and median. Only median will be applied.")
                for op in known_info:
                    graph["variables"][op] = questionary.text(
                        f"{i+1}) {graph['type']} {op} ="
                    ).ask()
                if len(exercise["graphs"]) > i:
                    exercise["graphs"][i] = graph
                else:
                    exercise["graphs"].append(graph)
                write_json(exercise, saved)

        num_parts = ask_int(
            "Number of parts", default=len(exercise["parts"]) if "parts" in exercise else ""
        )
        print("num_parts", num_parts)
        #     {
        #         "question": f"A market researcher polls every {nth} person who walks into a store.",
        #         "options": options_sampling
        #     },
        #     {
        #         "question": f"A computer generates {rand_n} random numbers, and {rand_n} people whose names correspond with the numbers on the list are chosen.",
        #         "options": options_sampling_2
        #     }

        if textbook_file is not None:
            use_questions_as_parts = num_parts == len(question_numbers)
            solution_choices: list[str] = [part for sol in file_solutions.values() for part in sol["parts"]]
        else:
            use_questions_as_parts = False
            solution_choices = []

        print(f"{title} v1")
        variant = {"desc": desc, "parts": set_default(exercise, "parts", [], saved=saved)}
        solutions = exercise.get("solutions", None) or [
            part["solution"] for part in variant["parts"]
        ]
        # solutions = [] if "solutions" not in exercise else exercise["solutions"]
        # parts_start_at = 0 if "parts" not in exercise else len(exercise["parts"])
        for p in range(num_parts):
            if p >= len(solutions):
                if use_questions_as_parts:
                    question_solutions = file_solutions.get(
                        str(file_questions[p]["questionNumber"]), {}
                    ).get("parts", [])
                    default_solution = '\n'.join(question_solutions)
                elif len(file_questions) == 1:
                    question_solutions = file_solutions.get(
                        str(file_questions[0]["questionNumber"]), {}
                    ).get("parts", [])
                    default_solution = question_solutions[p]
                else:
                    question_solutions = solution_choices
                    default_solution = ""
                cur_solution = questionary.autocomplete(
                    f"pt.{p+1} solution? (press tab to see helpers)",
                    default=default_solution,
                    choices=question_solutions,
                ).ask()
                solutions.append(cur_solution)
        print("solutions", solutions)
        # create_part
        for p in range(num_parts):
            part = variant["parts"][p] if p < len(variant["parts"]) else {}

            if "question" not in part:
                if use_questions_as_parts:
                    default_question_text = file_questions[p]["questionText"]
                    question_text_choices = file_questions[p]["parts"] + [file_questions[p]["questionText"]]
                elif len(file_questions) == 1 and p < len(file_questions[0]["parts"]):
                    default_question_text = file_questions[0]["parts"][p]
                    question_text_choices = file_questions[0]["parts"]
                else:
                    default_question_text = ""
                    question_text_choices = [part for question in file_questions for part in ([question["questionText"]] + question["parts"])]
                part["question"] = extract_variables(
                    questionary.autocomplete(
                        f"Question text for v1 - pt.{p+1}, solution: {solutions[p][:8]}{'...' if len(solutions[p]) > 8 else ''}\n(press tab for helpers, Ctrl U to delete line)",
                        default=default_question_text,
                        choices=question_text_choices
                    ).ask(),
                    variables=variables,
                )
                # cur_solution = questionary.autocomplete(
                #     f"pt.{p+1} solution? (press tab to see helpers)",
                #     default=default_solution,
                #     choices=question_solutions,
                # ).ask()
            if "type" not in part:
                part["type"] = questionary.select(
                    f"pt.{p+1} question type?",
                    choices=list(QUESTION_TYPES.keys()),
                    default=guess_question_type_from_solution(solutions[p]), # use solution from before variables are extracted
                ).ask()  # returns value of selection
            if "info" not in part:
                other_asks(part, solutions[p], use_gpt, exercise=exercise)

            part["solution"] = extract_variables(solutions[p], variables=variables)
            part["solution"] = convert_solution_to_type(part["solution"], part["type"])

            if p < len(variant["parts"]):
                variant["parts"][p] = part
            else:
                variant["parts"].append(part)

        exercise = {
            "num_variables": {},
            "imports": [],
            **exercise,
            "title": title,
            "description": variant["desc"],
            "parts": variant["parts"],
            "chapter": chapter,
            "path": f"{branch_name}.md",
            "variables": variables,
            "solutions": solutions,
            "finished": True,
        }
        write_json(exercise, saved)
        print("Wrote to saved.json")
        full_path = pathlib.Path(write_md(exercise))
        lint_server([str(full_path)])
        if create_pr:
            GITHUB_USERNAME: str = os.environ["GITHUB_USERNAME"]
            WRITE_PATH = pathlib.Path(os.environ["WRITE_PATH"])
            print(f"Copying question to {WRITE_PATH / full_path.parent.name}")
            shutil.copytree(
                src=full_path.parent, dst=WRITE_PATH / full_path.parent.name, dirs_exist_ok=True
            )
            CWD = WRITE_PATH / full_path.parent.name
            pr_body = [f"Closes #{issue}" for issue in issues]
            pr_body.append(
                "OPB 000: https://ca.prairielearn.com/pl/course_instance/4024/instructor/course_admin/questions"
            )
            pr_body = "\n".join(pr_body)
            commands = [
                f"git checkout --no-track -b {branch_name!r} origin/main",
                "git add .",
                "git commit -m 'Autogenerated Template' --no-verify",
                f"git push -u origin {branch_name!r}",
                f"gh pr create --draft -t {branch_name!r} -b '{pr_body}' --assignee {GITHUB_USERNAME!r}",
            ]
            for command in commands:
                print(f"Running: {command!r}")
                ret = subprocess.run(
                    shlex.split(command),
                    cwd=CWD,
                    capture_output=True,
                    check=True,
                    text=True,
                )
                print(ret.stdout)
        PL_QUESTION_PATH = pathlib.Path(os.environ["PL_QUESTION_PATH"])
        process_question_pl(
            full_path, output_path=PL_QUESTION_PATH / full_path.parent.name, dev=True
        )
        print(variant)
    except Exception as e:
        write_json(exercise, saved)
        print("Wrote to saved.json")
        traceback.print_exc()
        if isinstance(e, subprocess.CalledProcessError):
            print(e.stdout)
            print(e.stderr)
        return 1
    return 0
