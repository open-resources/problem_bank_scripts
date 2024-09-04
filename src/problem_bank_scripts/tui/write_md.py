import importlib.resources
import itertools
import json
import os
import pathlib
import shutil
import string
import tempfile
import textwrap

import pandas as pd
from pdf2image import convert_from_path

from .similarity import text_similarity
from .utils import apply_indent, apply_params_to_str, count_decimal_places, string_is_numeric


WRITE_PATH = "./questions"
MY_NAME = None
MY_INITIALS = None
CUSTOM_KEYS = ["type", "choices", "code", "options", "statements"]
TAB = " " * 2
TOPICS = {
    "1": "Introduction to Data",
    "2": "Summarizing Data",
    "3": "Probability",
    "4": "Distributions of random variables",
    "5": "Foundations for inference",
    "6": "Inference for categorical data",
    "7": "Inference for numerical data",
    "8": "Foundations for inference",  # for openstax
    "9": "Multiple and logistic regression",
}
TEMPLATE = string.Template(
    importlib.resources.files("problem_bank_scripts.tui")
    .joinpath("question.md.template")
    .read_text(encoding="utf-8")
)


def _update_globals():
    global MY_NAME, MY_INITIALS

    if MY_NAME is None:
        MY_NAME = os.environ.get("MY_NAME")

    if MY_INITIALS is None:
        MY_INITIALS = os.environ.get("MY_INITIALS")


def md_part_lines(part, i, params=None, solution: str | None = None):
    q_type = part["info"]["type"]
    answer_section = ""
    if q_type == "number-input" or q_type == "integer-input":
        answer_section = "Please enter a numeric value in.\n"
    elif q_type == "multiple-choice" or q_type == "dropdown":
        choices = part["info"]["choices"]
        answer_section = "\n".join(
            [f"- {{{{ params.part{i+1}.ans{j+1}.value }}}}" for j in range(len(choices))]
        )
    elif q_type == "file-upload":
        answer_section = "File upload box will be shown here.\n"
    # answer_section2 = '### pl-answer-panel\n\nEverything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.\nPlease remove this section if it is not application for this question.'
    # if part['type'] == 'multiple-choice':

    result = [f"## Part {i+1}", "", part["question"], ""]

    result += ["### Answer Section\n", answer_section, ""]

    if solution:
        if params:
            formatted_soln = apply_params_to_str(solution, params)
            result += ["### pl-answer-panel", "", f"{formatted_soln}", ""]
        else:
            result += ["### pl-answer-panel", "", f"{solution}", ""]

    return [*result, ""]


def get_pl_customizations(info: dict, index: int = 0):
    pl_indent = " " * 4

    decdig_defaults = {
        "comparison": "decdig",
        "digits": 2,
        "weight": 1,
        "allow-blank": "false",
        "label": "$d= $",
    }
    match info["type"]:
        case "multiple-choice":
            customizations: dict[str, str | int] = {"weight": 1}
        case "number-input":
            # # TODO: need to know if integer or not
            # if 'sigfigs' in info and info['sigfigs'] == 'integer':
            #     customizations["weight"] = 1
            #     customizations["allow-blank"] = "true"
            # else:
            customizations = decdig_defaults
        case "matrix-component-input":
            customizations = {"allow-fractions": "true", **decdig_defaults}
        case "dropdown":
            customizations = {"weight": 1, "blank": "true"}
        case "checkbox":
            customizations = {
                "weight": 1,
                "partial-credit": "true",
                "partial-credit-method": '"EDC"',
            }
        case "symbolic-input":
            customizations = {
                "label": "$F_r = $",
                "variables": '"m, v, r"',
                "weight": 1,
                "allow-blank": "false",
            }
        case "longtext":
            customizations = {
                "placeholder": '"Type your answer here..."',
                "file-name": f'"answer{index+1}.html"',
                "quill-theme": '"snow"',
                "directory": '"clientFilesQuestion"',
                "source-file-name": '"sample.html"',
            }
        case "file-upload":
            customizations = {"file-names": '"file.png, file.jpg, file.pdf, filename space.png"'}
        case "matching":
            customizations = {"weight": 1, "blank": "true"}
        case "integer-input":
            customizations = {"allow-blank": "false"}
        case _:
            customizations = {}

    customizations |= info
    lines = [f"{key}: {val}" for key, val in customizations.items() if key not in CUSTOM_KEYS]

    return ["  pl-customizations:", *apply_indent(lines=lines, indent=pl_indent)]


def format_type_info(info: dict):
    indent = TAB
    info_type = info["type"]
    entries = [f'type: {info["type"]}']

    if info_type == "longtext":
        entries.append("gradingMethod: Manual")

    if info_type == "number-input" and "sigfigs" in info and info["sigfigs"] == "integer":
        entries.append("label: $p=$")

    if info_type == "matching":
        entries.append("showCorrectAnswer: true")

    return apply_indent(entries, indent)


def move_figure(asset: str, exercise_path: str):
    _update_globals()
    dir_path = pathlib.Path(WRITE_PATH) / pathlib.Path(exercise_path).stem.lower()
    figure_no_extension_name, ext = asset.rsplit(".", maxsplit=1)
    if ext == "pdf":
        images = None
        with tempfile.TemporaryDirectory() as tmp_path:
            images = convert_from_path(asset, output_folder=tmp_path, use_cropbox=True)
            figure_name = f"{figure_no_extension_name}.jpg"
            if len(images) > 0:
                images[0].save(dir_path / figure_name, "JPEG")
    else:
        figure_name = pathlib.Path(asset).name
        shutil.copyfile(asset, f"{dir_path}/{figure_name}")
    return figure_name


def num_variable_to_line_value(num: float):
    randomized_str = ""
    if num.is_integer():
        if abs(num) > 15:
            range_value = abs(num) // 10
            add = 0
        else:
            range_value = abs(num)
            add = 2 if num >= 3 else 0
        randomized_str = f"random.randint({int(num - range_value + add)}, {int(num + range_value)})"
        num = int(num)
        if 1900 < num < 2090:
            randomized_str = num
    else:
        count_after_decimal = count_decimal_places(num)
        if (num := abs(num)) <= 0.5:
            range_value = round(num * 2, count_after_decimal)
        else:
            range_value = round(num / 10, count_after_decimal)
        randomized_str = f"round(random.uniform({round(num - range_value, count_after_decimal)}, {round(num + range_value, count_after_decimal)}), {count_after_decimal})"
    return f"{randomized_str}  # {num}"


def write_code(exercise: dict):
    indent = " " * 8
    lines = [
        "data2 = pbh.create_data2()",
        "",
        f'data2["params"]["vars"]["title"] = "{exercise["title"]}"',
    ]

    num_variables = exercise["num_variables"]
    variables = exercise["variables"]

    # Randomize Variables
    # v = random.randint(2,7)
    # t = random.randint(5,10)

    # region Handle variables
    used_by = {}
    for var_name, value in variables.items():
        if string_is_numeric(value):
            value = float(value)  # noqa: PLW2901
        if isinstance(value, float):
            num = value
            used = used_by.get(num, "")
            if not used:
                used_by[num] = var_name
            line = (
                f"{var_name} = {num_variable_to_line_value(num)}"
                if not used
                else f"{var_name} = {used}"
            )
            lines.append(line)
        else:
            lines.append(f"{var_name} = {value}")
            used_by[value] = var_name
    lines.append("")
    for var_name, value in variables.items():
        # values = var_name.split('_') # WARNING: THIS PART WAS IN OLD
        values = [var_name]
        cur_var_line = "data2['params']"
        for val in values:
            cur_var_line += f"['{val}']"
        cur_var_line += f" = {var_name}"
        lines.append(cur_var_line)
    lines.append("")

    lines.append("# Randomize Variables")
    for key, values in num_variables.items():
        for i, num in enumerate(values):
            cur_var_name = f"{key}_num{i+1}"
            used = used_by.get(num, "")
            if not used:
                used_by[num] = cur_var_name

            line = (
                f"{cur_var_name} = {num_variable_to_line_value(num)}"
                if not used
                else f"{key}_num{i+1} = {used}"
            )
            lines.append(line)

    if "tables" in exercise:
        for i, table in enumerate(exercise["tables"], start=1):
            lines.append(f"table{i} = {table['matrix']}")
            lines.append(
                f'data2["params"]["table{i}"] = pbh.create_html_table(table{i}, width="550px", '
                f'first_row_is_header={table.get("first_row_is_header", True)}, first_col_is_header={table.get("first_col_is_header", False)},)'
            )

    if "matrices" in exercise:
        for i, matrix in enumerate(exercise["matrices"], start=1):
            lines.append(f"matrix_ans{i} = {matrix['matrix']}")
            lines.append(f'data2["params"]["matrix{i}"] = pl.to_json(np.array([matrix_ans{i}]))')

    lines.append("")
    lines.append('# store the variables in the dictionary "params"')
    for key, values in num_variables.items():
        for i, num in enumerate(values, start=1):
            lines.append(f'data2["params"]["{key}"]["num{i}"] = {key}_num{i}')
    lines.append("")

    # endregion handle variables

    if len(exercise["parts"]) != len(exercise["solutions"]):
        print(f"MISMATCH: parts {len(exercise['parts'])}, solns {len(exercise['solutions'])}")
        print("parts:")

        print(json.dumps([x["question"] for x in exercise["parts"]], indent=2))
        print("solns:")
        print(json.dumps(exercise["solutions"], indent=2))

    for part_num, part in enumerate(exercise["parts"]):
        lines.append(f"# Part {part_num+1} is a {part['info']['type']} question.")
        if "code" in part["info"]:
            lines.append("# GPT generated solution")
            lines.extend(part["info"]["code"].splitlines())

        if part["info"]["type"] == "multiple-choice" or part["info"]["type"] == "dropdown":
            for choice_num, choice in enumerate(part["info"]["choices"], start=1):
                lines += [
                    f'data2["params"]["part{part_num+1}"]["ans{choice_num}"]["{key}"] = {val}'
                    for key, val in choice.items()
                ]
                lines.append("")
            lines.append("")
        if part["info"]["type"] == "matching":
            lines += [
                f'data2["params"]["part{part_num+1}"]["option{i}"]["value"] = "{value}"'
                for i, value in enumerate(part["info"]["options"])
            ]
            lines.append("")
            lines.extend(
                itertools.chain.from_iterable(
                    [
                        f'data2["params"]["part{part_num+1}"]["statement{s_num}"]["value"] = "{statement_info["value"]}"',
                        f'data2["params"]["part{part_num+1}"]["statement{s_num}"]["matches"] = "{statement_info["matches"]}"',
                    ]
                    for s_num, statement_info in enumerate(part["info"]["statements"], start=1)
                )
            )
            lines.append("")
        if part["info"]["type"] in {"number-input", "integer-input"}:
            numeric_answer = None
            words = exercise["solutions"][part_num].strip().split(" ")
            if len(words) == 1 and string_is_numeric(
                ans := exercise["solutions"][part_num].replace(",", "").strip().strip("%")
            ):
                numeric_answer = float(ans)
                # exercise['solutions'][part_num] = f'{{{{ correct_answers.part{part_num+1}_ans }}}}' # WARNING: THIS PART WAS IN OLD
            if (
                len(list(filter(None, exercise["solutions"][part_num].split("\n")))) == 1
                and "\\rightarrow" in exercise["solutions"][part_num]
            ):
                numeric_answer = 1
                answer_section: str = (
                    exercise["solutions"][part_num].split("\\rightarrow")[-1].strip()
                )
                while not answer_section[-1].isdigit():
                    answer_section = answer_section[:-1]
                while not answer_section[0].isdigit() and answer_section[0] != "-":
                    answer_section = answer_section[1:]
                numeric_answer = float(answer_section.strip())
                split: list[str] = exercise["solutions"][part_num].split("\\rightarrow")
                split[-1] = split[-1].replace(
                    answer_section, f"{{{{ correct_answers.part{part_num+1}_ans }}}}"
                )
                exercise["solutions"][part_num] = "\\rightarrow".join(split)
            if len(words) > 0 and string_is_numeric(words[-1].replace(",", "").strip()):
                numeric_answer = float(words[-1].replace(",", "").strip())
                exercise["solutions"][part_num] = exercise["solutions"][part_num].replace(
                    words[-1], f"{{{{ correct_answers.part{part_num+1}_ans }}}}"
                )
            if numeric_answer is not None:
                end_note = ""
                decimals = count_decimal_places(numeric_answer)
            else:
                end_note = "# TODO: insert correct answer here"
                decimals = 2
            lines += [
                f"correct_part{part_num+1}_ans = {numeric_answer or ' '.join(words)}  {end_note}",
                f"data2['correct_answers']['part{part_num+1}_ans'] = pbh.roundp(correct_part{part_num+1}_ans, decimals={decimals})",
                "",
            ]
        if part["info"]["type"] == "matrix-component-input":
            lines += [
                f"correct_part{part_num+1}_ans = np.array([{exercise['solutions'][part_num]}])",
                f"data2['correct_answers']['part{part_num+1}_ans'] = pl.to_json(matrix_ans{part_num+1})",
            ]
        if part["info"]["type"] == "symbolic-input" and "custom_functions" in part["info"]:
            for func in part["info"]["custom_functions"]:
                lines += [
                    f'{func} = sp.Function("{func}")',
                    "with sp.evaluate(False):",
                    f"{TAB}part{part_num+1}_ans = {func}(...)",
                ]
            lines.append(
                f'data2["correct_answers"]["part{part_num+1}_ans"] = pl.to_json(part{part_num+1}_ans)'
            )

    lines += ["# Update the data object with a new dict", "data.update(data2)"]
    return apply_indent(lines, indent), used_by


def assign_graph_variables(graph: dict, i: int, num_graphs: int):
    variables = graph["variables"]
    lines = [""]
    for var in variables:
        if num_graphs == 1:
            lines.append(f"{var} = {variables[var]}")
        else:
            lines.append(f"{var}_{i+1} = {variables[var]}")
    lines.append("")
    return lines


def write_graph(exercise: dict):
    indent = " " * 8
    outer_lines = ['if data["filename"] == "figure 1.png":', ""]
    lines = []

    graphs = exercise["graphs"]
    axis_str = ", ".join([f"ax{i+1}" for i in range(len(graphs))])

    lines.append(
        f"fig, ({axis_str}) = plt.subplots({1}, {len(graphs)}, figsize=(10, 6))"
    )  # Create n subplots

    for i, graph in enumerate(graphs):
        graph_type: str = graph["type"]
        variables = graph["variables"]
        lines.append("")
        lines.append(f"# {graph_type}")
        ax = f"ax{i+1}"

        lines += assign_graph_variables(graph, i, len(graphs))
        suffix = f"_{i+1}" if len(graphs) > 1 else ""
        if graph_type == "other":
            lines.append("# graph code here...")
        elif graph_type == "scatter":
            msg = "Scatter plots not supported yet"
            raise NotImplementedError(msg)
        elif graph_type == "histogram":
            lines.append(
                f"data{suffix} = np.random.uniform(low=min_val{suffix}, high=max_val{suffix}, size=sample_size{suffix})"
            )
            if "median" in graph["variables"]:
                lines.append(
                    f"data{suffix} = data{suffix} * (median{suffix} / (max_val{suffix} - min_val{suffix})) + min_val{suffix}"
                )
            lines.append(f"{ax}.hist(data{suffix}, bins=num_bins{suffix}, edgecolor='black')")
            lines.append(f"{ax}.grid(True)")
        elif graph_type == "bar":
            print("Bar plots not supported yet")
        elif graph_type == "line":
            print("Line plots not supported yet")
        elif graph_type == "box plot":
            data = graph["data"]
            if not isinstance(data[0], list):
                data = [data]
            lines.append(f"iqr{suffix} = q3{suffix} - q1{suffix}")

            if "min_val" not in variables:
                lines.append(
                    f"min_val{suffix} = q1{suffix} - 1.5 * iqr{suffix} - iqr{suffix} * 0.1"
                )
            if "max_val" not in variables:
                lines.append(
                    f"max_val{suffix} = q3{suffix} + 1.5 * iqr{suffix} + iqr{suffix} * 0.1"
                )

            lines.append("")
            is_bxp = False
            for j, box in enumerate(data):
                # case for box is None
                if (
                    "median" in variables
                    and "q1" in variables
                    and "q3" in variables
                    and "whislow" in variables
                    and "whishigh" in variables
                ):
                    lines.append(
                        f"box_data_{j+1} = dict(med=median{suffix}, q1=q1{suffix}, q3=q3{suffix}, whislo=whislow{suffix}, whishi=whishigh{suffix}, fliers=[])"
                    )  # [min_val{suffix}, q1{suffix}, median{suffix}, q3{suffix}, max_val{suffix}]
                    is_bxp = True
                else:
                    if "median" in variables:
                        if "std" in variables:
                            lines.append(
                                f"# suggestion, change iqr to control std, calculate std with std=np.std(box_data{i+1})"
                            )
                        create_data = f"box_data_{j+1} = np.random.uniform(low=min_val{suffix}, high=median{suffix}, size=(sample_size{suffix}-1)//2) + [median] + np.random.uniform(low=median, high=max_val{suffix}, size=(sample_size{suffix}-1)//2)"
                        lines.append(create_data)
                    else:
                        lines.append(
                            f"box_data_{j+1} = np.random.normal(loc=mean{suffix}, scale=std{suffix}, size=sample_size{suffix})"
                        )
                lines.append("")

            data_array = "[" + ", ".join([f"box_data_{j+1}" for j in range(len(data))]) + "]"
            lines.append("")
            show_means = "mean" in variables
            labels = (
                f', labels={graph["labels"]}'
                if "labels" in graph and len(graph["labels"]) > 0
                else ""
            )
            plot_name = "bxp" if is_bxp else "boxplot"
            lines.append(
                f"bp{suffix} = {ax}.{plot_name}({data_array}{labels}, showmeans={show_means}, meanline={show_means}, vert={graph['is_vertical']})"
            )
            lines.append("")
            # lines.append('# Annotate the new means on the plot')
            # lines.append('for i, mean in enumerate(new_means):')
            # lines.append(f"{TAB}{ax}.text(i + 1, mean, f'{{mean:.2f}}', color='black', fontsize=9, ha='center', va='bottom')")
        else:
            print(f"Graph type {graph_type} not supported")
        if "title" in graph:
            lines.append(f"{ax}.set_title('{variables['title']}')")
        if "x_label" in variables:
            lines.append(f"{ax}.set_xlabel('{variables['x_label']}')")
        if "y_label" in variables:
            lines.append(f"{ax}.set_ylabel('{variables['y_label']}')")
    lines += ["", "plt.tight_layout()", ""]
    outer_lines += apply_indent(lines, TAB)
    outer_lines += ["buf = io.BytesIO()", 'plt.savefig(buf, format="png")', "return buf"]
    return apply_indent(outer_lines, indent)


def suggested_outcomes(exercise):
    chapter = exercise["chapter"]
    df = pd.read_csv(
        "https://raw.githubusercontent.com/open-resources/learning_outcomes/main/outputs_csv/LO_stats.csv"
    )
    df = df.loc[df["Topic"] == TOPICS[chapter]]

    question_text = "\n".join([x["question"] for x in exercise["parts"]])
    question_text += f"\n{exercise['description']}\n'{exercise['title']}\n" + "\n".join(
        exercise["solutions"]
    )
    df["Similarity"] = df.apply(
        lambda row: text_similarity(row["Learning Outcome"], question_text), axis=1
    )

    min_value = 1
    while len(df.index) > 5:
        df = df.loc[df["Similarity"] > min_value]
        min_value += 0.5

    return "".join([f"- {row['Code']}  # {row['Learning Outcome']}\n" for _, row in df.iterrows()])


def display_assets(exercise):
    asset_lines1 = []
    asset_to_filename = {}
    # Do all the moving here
    for asset in exercise["assets"]:
        if asset.endswith(".html"):
            asset_lines1.append(f"- {asset}")
            continue
        figure_name = move_figure(asset, exercise["path"])
        asset_to_filename[asset] = figure_name
        asset_lines1.append(f"- {figure_name}")

    asset_lines2 = []
    for asset in exercise["assets"]:
        filename = asset_to_filename.get(asset, asset)
        if filename.rsplit(".", maxsplit=1)[-1] in {"jpg", "jpeg", "png"}:
            asset_lines2.append(f'<img src="{filename}" width=400>')

    if len(exercise["assets"]) > 0:
        asset_lines2.append("")
    return asset_lines1, asset_lines2


def display_extras(exercise):
    lines_to_write = []
    for extra in exercise["extras"]:
        if extra == "table":
            tables = exercise["tables"]
            for t, _ in enumerate(tables, start=1):
                lines_to_write.append(f"{{{{{{ params.table{t}}}}}}}")
            # lines_to_write.append(f"data2['params']['table'] = {table}")
        elif extra == "image":
            pass  # handled in assets
        elif extra == "graph":
            lines_to_write.append(
                '<pl-figure file-name="figure 1.png" type="dynamic" width="500px"></pl-figure>'
            )
        elif extra == "matrix":
            matrices = exercise["matrices"]
            for t, matrix in enumerate(matrices):
                lines_to_write.append(
                    f'<pl-matrix-latex params-name="matrix{t+1}"></pl-matrix-latex>'
                )
    if len(lines_to_write) > 0:
        lines_to_write.append("")
    return lines_to_write


def write_md(exercise: dict):
    _update_globals()

    solutions = exercise["solutions"]
    chapter = exercise["chapter"]

    dir_end = pathlib.Path(exercise["path"]).stem
    dir_path = pathlib.Path(WRITE_PATH) / dir_end
    path = dir_path / exercise["path"]
    dir_path.mkdir(parents=True, exist_ok=True)

    DEFAULT_CODE = " " * 8 + "pass"

    template_items = {
        "title": exercise["title"],
        "topic": TOPICS[chapter],
        "author": MY_NAME,
        "attribution": exercise["attribution"],
        "outcomes": suggested_outcomes(exercise),
        "tags": f"- {MY_INITIALS}",
        "file": DEFAULT_CODE,
        "prepare": DEFAULT_CODE,
        "parse": DEFAULT_CODE,
        "grade": DEFAULT_CODE,
    }

    asset_lines1, asset_lines2 = display_assets(exercise)
    template_items["assets"] = "\n" + "\n".join(asset_lines1)

    all_imports = {
        "import random",
        "import problem_bank_helpers as pbh",
    }
    all_imports.update(set(exercise["imports"]))
    if "graphs" in exercise:
        all_imports.add("import matplotlib.pyplot as plt")
        all_imports.add("import io")
        all_imports.add("import numpy as np")
        all_imports.add("from matplotlib import cbook")
    if "matrices" in exercise:
        all_imports.add("import prairielearn as pl")

    template_items["imports"] = textwrap.indent("\n".join(list(all_imports)), " " * 8)

    code_lines, params_dict = write_code(exercise)
    template_items["generate"] = "\n".join(code_lines)

    if "graphs" in exercise:
        template_items["file"] = "\n".join(write_graph(exercise))

    question_part_lines = []
    for i, part in enumerate(exercise["parts"]):
        question_lines = [
            f"part{i + 1}:",
            *format_type_info(part["info"]),
            *get_pl_customizations(part["info"], i),
        ]
        question_part_lines += question_lines
    template_items["parts_yaml"] = "\n".join(question_part_lines)

    question_body = [exercise["description"], ""]

    # TODO: ADD ASSETS HERE, how should assets be formatted?, since parts assets + main assets
    question_body += asset_lines2

    question_body += display_extras(exercise)

    has_long_text = False
    if len(exercise["parts"]) != len(solutions):
        print(
            f"ERROR: PARTS AND SOLUTIONS LENGTHS DON'T MATCH, parts {len(exercise['parts'])}, solutions {len(solutions)}"
        )
        print(
            "PARTS",
            len(exercise["parts"]),
            json.dumps([x["question"] for x in exercise["parts"]], indent=2),
        )
        print("SOLUTIONS", len(solutions), json.dumps(solutions, indent=2))
        # print(json.dumps(exercise, indent=2))

        print("\nPATH", path)
        print()

        if len(solutions) > len(exercise["parts"]):
            while len(solutions) > len(exercise["parts"]):
                solutions[1] = solutions[0] + "\n" + solutions[1]
                solutions = solutions[1:]
        else:
            msg = "PARTS AND SOLUTIONS LENGTHS DON'T MATCH"
            raise AssertionError(msg)
    for i, part in enumerate(exercise["parts"]):
        question_body += md_part_lines(part, i=i, params=params_dict, solution=solutions[i])
        if part["info"]["type"] == "longtext":
            has_long_text = True
            if "sample.html" not in template_items["assets"]:
                template_items["assets"] = template_items["assets"].rstrip() + "\n- sample.html"

    template_items["question"] = "\n".join(question_body)

    filled = TEMPLATE.safe_substitute({k: v.rstrip() for k, v in template_items.items()})

    print("WRITING TO", path)

    path.write_text(filled, encoding="utf-8")

    if has_long_text:
        dir_path.joinpath("sample.html").touch()
    return path
