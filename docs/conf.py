# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sphinx_autosummary_accessors

import geotech_pandas  # noqa: F401 registers accessor for autosummary

project = "geotech-pandas"
copyright = "2023, Fraser Dominic David"
author = "Fraser Dominic David"
version = "0.0.0"
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
}
