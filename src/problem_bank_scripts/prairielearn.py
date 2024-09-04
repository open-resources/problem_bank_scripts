import sympy

from ._vendored import python_helper_sympy as phs

__all__ = ["to_json"]

# at question conversion time, the only needed metadata is via sympy_to_json
def to_json(v, *args, **kwargs):
    if isinstance(v, sympy.Expr):
        return phs.sympy_to_json(v)
    return None


# See PEP 562: https://peps.python.org/pep-0562/ for how the below works
# But it basically it makes sure that any other functions that normally exist
#  are available in case someone wants them


def __getattr__(name: str):
    if name == "to_json":
        return globals()[name]

    def fake_function(*args, **kwargs):
        return None

    return fake_function


def __dir__():
    return ["to_json"]
