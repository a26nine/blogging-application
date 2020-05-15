# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Path setup
import os
import sys

sys.path.insert(0, os.path.abspath("_extensions"))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath("."))))

import kivymd
import autoapi_kivymd  # from _extensions


# Project information
project = "KivyMD"
copyright = "2020, Andrés Rodríguez, Ivanov Yuri, Artem S. Bulgakov and KivyMD contributors"
author = (
    "Andrés Rodríguez, Ivanov Yuri, Artem S. Bulgakov and KivyMD contributors"
)
version = kivymd.__version__
reelase = kivymd.__version__


# General configuration
master_doc = "index"
exclude_patterns = []
templates_path = ["_templates"]
locale_dirs = ["_locales"]
language = "Python"


# HTML Theme
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_favicon = "_static/logo-kivymd.png"
html_logo = "_static/logo-kivymd.png"
html_theme_options = {
    "canonical_url": "https://kivymd.readthedocs.io/en/latest/",
    "navigation_depth": 2,
    "collapse_navigation": False,
}


# Extensions
extensions = [
    "sphinx.ext.autodoc",
    "autoapi_kivymd",
    "sphinx.ext.intersphinx",
    "kivy_lexer",
    "toctree_with_sort",
]

# AutoAPI configuration
autoapi_dirs = ["../../kivymd"]
autoapi_template_dir = os.path.abspath("_templates")
autoapi_ignore = []
autoapi_type = "python"
autoapi_file_patterns = ["*.py"]
autoapi_generate_api_docs = True
autoapi_options = ["members", "undoc-members"]
autoapi_root = "api"
autoapi_add_toctree_entry = False
autoapi_include_inheritance_graphs = False
autoapi_include_summaries = True
autoapi_python_class_content = "class"
autoapi_python_use_implicit_namespaces = False
autoapi_keep_files = False  # True for debugging

# InterSphinx configuration
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "kivy": ("https://kivy.org/doc/stable/", None),
}
