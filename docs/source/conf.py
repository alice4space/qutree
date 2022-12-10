"""
Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# -- Path setup ----------------------------------------------------------------
from datetime import datetime

from src import __author__, __version__

# -- Project information -------------------------------------------------------

project = "template"
copyright = f"2022-{datetime.now().year}, {__author__}"
author = __author__
release = __version__

# -- General configuration -----------------------------------------------------

extensions = []

templates_path = ["_templates"]

# when working in a Jupyter env.
exclude_patterns = ["**.ipynb_checkpoints"]


# -- Options for HTML output ---------------------------------------------------

html_theme = "pydata-sphinx-theme"

html_static_path = ["_static"]

# -- Options of the HTML theme -------------------------------------------------
