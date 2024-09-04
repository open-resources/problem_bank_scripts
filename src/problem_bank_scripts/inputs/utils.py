from typing import Protocol


__all__ = ["InputType", "replace_tags"]


def replace_tags(string: str) -> str:
    """Takes in a string with tags: |@ and @| and returns {{ and }} respectively. This is because Python strings can't have double curly braces.

    Args:
        string (str): String to be processed, can be multi-line.

    Returns:
        string (str): returns string with tags replaced with curly braces.
    """
    return (string
        .replace("|@|@", r"{{{")
        .replace("@|@|", r"}}}")
        .replace("|@", r"{{")
        .replace("@|", r"}}")
    )


class InputType(Protocol):
    def __call__(self, part_name: str, parsed_question: dict, data_dict: dict) -> str:
        """Processes markdown format of a pl question and returns PL HTML

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
        ...