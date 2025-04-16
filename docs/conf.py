# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sphinx_autosummary_accessors

try:
    import geotech_pandas
except ModuleNotFoundError:
    import os
    import sys

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

    import geotech_pandas  # noqa: F401 registers accessor for autosummary

project = "geotech-pandas"
copyright = "2023-2025, Fraser Dominic David"
author = "Fraser Dominic David"
version = "0.3.0"
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_design",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "numpydoc",
    "sphinx_autosummary_accessors",
    "sphinx.ext.extlinks",
]

autosummary_generate = True
autodoc_typehints = "none"

templates_path = ["_templates", sphinx_autosummary_accessors.templates_path]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}

intersphinx_disabled_reftypes = ["*"]

# extlinks alias
extlinks = {
    "pull": ("https://github.com/fraserdominicdavid/geotech-pandas/pull/%s", "#%s"),
}

# numpydoc
numpydoc_show_class_members = False
numpydoc_show_inherited_class_members = False
numpydoc_attributes_as_param_list = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
# html_static_path = ["_static"]

html_title = project
html_theme_options = {
    "navbar_align": "left",
    "github_url": "https://github.com/fraserdominicdavid/geotech-pandas",
    "show_nav_level": 4,
    "secondary_sidebar_items": ["page-toc"],
}
html_sidebars = {
    "**": ["sidebar-nav-bs", "sidebar-ethical-ads"],
    "index": [],
    "changelog/index": [],
    "column-reference/index": [],
}
