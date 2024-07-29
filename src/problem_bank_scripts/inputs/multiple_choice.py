from .utils import replace_tags


__all__ = ["MCInputConverter"]

class MCInputConverter:
    """Creates a input type converter for a given multiple choice style tag, such as ``pl-multiple-choice`` or ``pl-dropdown``.
    
    Basic is determined by the fact that the processor just needs to set the appropriate tag,
    group the pl-customizations, and return the HTML including the markdown content for the question.

    More complex processors will need to be created manually, or with a different factory function.

    Arguments
    ---------
        pl_tag (str):
            The tag to be used for the input type, such as ``multiple-choice`` (for ``pl-multiple-choice``)
            or ``dropdown`` (for ``pl-dropdown``).
    """

    def __init__(self, pl_tag: str):
        self._pl_tag = pl_tag
        self.__doc__ = self.__call__.__doc__.format(pl_tag=pl_tag)  # pyright: ignore[reportOptionalMemberAccess]
    
    def __call__(self, part_name: str, parsed_question: dict, data_dict: dict) -> str:
        """Processes markdown format of {pl_tag} questions and returns PL HTML

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
        html = f"<pl-question-panel>\n<markdown>{parsed_question['body_parts_split'][part_name]['content']}</markdown>\n</pl-question-panel>\n\n"

        pl_customizations = " ".join(
            [
                f'{k} = "{v}"'
                for k, v in parsed_question["header"][part_name][
                    "pl-customizations"
                ].items()
            ]
        )  # PL-customizations
        html += f'<pl-{self._pl_tag} answers-name="{part_name}_ans" {pl_customizations} >\n'

        ###### LOOKHERE
        if (data_dict["params"]["vars"]["units"]) and (
            "units" in parsed_question["body_parts_split"][part_name]["answer"]
        ):
            units = "|@ params.vars.units @|"
        else:
            units = ""

        ## Note: `|@`` gets converted into `{{` and `@|`` gets converted to `}}` by `replace_tags()`
        for a in data_dict["params"][f"{part_name}"]:
            if "ans" in a:
                if data_dict["params"][f"{part_name}"][f"{a}"]["feedback"]:
                    feedback = f"|@ params.{part_name}.{a}.feedback @|"
                else:
                    feedback = "Feedback for this choice is not available yet."

                correctness = f"|@ params.{part_name}.{a}.correct @|"
                value = f"|@|@ params.{part_name}.{a}.value @|@|"

                ## Hack to remove feedback for Dropdown questions
                if self._pl_tag == "dropdown":
                    html += f"\t<pl-answer correct= {correctness} > {value} {units} </pl-answer>\n"
                else:
                    html += f"\t<pl-answer correct= {correctness} feedback = '{feedback}' > {value} {units} </pl-answer>\n"

        return replace_tags(f"{html}</pl-{self._pl_tag}>\n")
