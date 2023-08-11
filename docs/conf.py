# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import sys
from pathlib import Path

from pallets_sphinx_themes import ProjectLink

from click_option_group import __version__

sys.path.insert(0, str(Path().absolute()))

# -- Project information -----------------------------------------------------

project = "click-option-group"
copyright = "2019-2020, Eugene Prilepin"
author = "Eugene Prilepin"

# The full version, including alpha/beta/rc tags
release = __version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "pallets_sphinx_themes",
    "m2r2",
]

autodoc_member_order = "bysource"

intersphinx_mapping = {"Click": ("https://click.palletsprojects.com", None)}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "click"

html_context = {
    "project_links": [
        ProjectLink("PyPI releases", "https://pypi.org/project/click-option-group/"),
        ProjectLink("Source Code", "https://github.com/click-contrib/click-option-group/"),
        ProjectLink(
            "Issue Tracker",
            "https://github.com/click-contrib/click-option-group/issues/",
        ),
    ]
}

html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html"],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
