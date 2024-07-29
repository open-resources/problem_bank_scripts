__all__ = [
    "INPUT_TYPE_PROCESSORS",
    "OPB_INPUT_TYPES",
    "BasicInputConverter",
    "MCInputConverter",
    "InputType",
    "replace_tags",
    "process_custom_input",
    "process_file_upload",
    "process_matching",
    "process_workspace",
]


from .basic import BasicInputConverter
from .inputs import process_custom_input, process_file_upload, process_matching, process_workspace
from .multiple_choice import MCInputConverter
from .utils import InputType, replace_tags


_SUPPORTED_INPUTS: dict[str, tuple[InputType, str]] = {
    "number-input":           (BasicInputConverter("number-input"), "pl-number-input"),
    "integer-input":          (BasicInputConverter("integer-input"), "pl-integer-input"),
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
    "custom-input":           (process_custom_input, "custom-input"),
}

INPUT_TYPE_PROCESSORS = {opb_name: func for opb_name, (func, _) in _SUPPORTED_INPUTS.items()}
OPB_INPUT_TYPES = {tag: opb_name for opb_name, (_, tag) in _SUPPORTED_INPUTS.items()}
