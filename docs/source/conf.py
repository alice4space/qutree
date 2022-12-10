"""
Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import os
import sys

# -- Path setup ----------------------------------------------------------------
from datetime import datetime

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../.."))

from src import __author__, __version__  # noqa

# -- Project information -------------------------------------------------------
project = "template"
copyright = f"2022-{datetime.now().year}, {__author__}"
author = __author__
release = __version__

# -- General configuration -----------------------------------------------------
extensions = [
    "sphinx.ext.autosummary",
    "numpydoc",
]
templates_path = ["_templates"]
exclude_patterns = ["**.ipynb_checkpoints"]  # when working in a Jupyter env.


# -- Options for HTML output ---------------------------------------------------
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]

# -- Options for autosummary/autodoc output ------------------------------------
autosummary_generate = True
autoclass_content = "class"

# -- Options of the HTML theme -------------------------------------------------
