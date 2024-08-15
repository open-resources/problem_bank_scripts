# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = "Problem Bank Scripts"
copyright = "2021-Present, Open Problem Bank Team"
author = "Open Problem Bank Team"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_nb",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "matplotlib.sphinxext.plot_directive",
]
nbsphinx_execute = "always"
autodoc_member_order = "bysource"

# Napoleon settings
napoleon_numpy_docstring = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True

plot_pre_code = """
import numpy as np
import matplotlib.pyplot as plt
import problem_bank_helpers as pbh
"""
plot_formats = ["png"]
plot_include_source = True
plot_html_show_source_link = False
plot_html_show_formats = False

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Links used for cross-referencing stuff in other documentation
intersphinx_mapping = {
    "py": ("https://docs.python.org/3", None),
    "mpl": ("https://matplotlib.org/stable", None),
}

show_warning_types = True
suppress_warnings = ["docutils"]

nitpick_ignore = [
    ("py:class", "optional"),
    ("py:class", "number"),
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
