"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""


# -- Path setup ----------------------------------------------------------------
from datetime import datetime

# -- Project information -------------------------------------------------------
project = "ipython-gpt"
copyright = f"2023-{datetime.now().year}, Santiago Basulto"
author = "Santiago Basulto"
release = "0.0.4"

# -- General configuration -----------------------------------------------------
extensions = [
    "sphinx_copybutton",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx_design",
    "sphinxcontrib.icon",
    "sphinxcontrib.btn",
]
templates_path = ["_template"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output ---------------------------------------------------
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_theme_options = {
    "logo": {
        "text": project,
    },
    "use_edit_page_button": True,
    "footer_end": ["theme-version"],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/santiagobasulto/ipython-gpt",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "Pypi",
            "url": "https://pypi.org/project/ipython-gpt/",
            "icon": "fa-brands fa-python",
        },
    ],
}
html_context = {
    "github_user": "santiagobasulto",
    "github_repo": "ipython-gpt",
    "github_version": "master",
    "doc_path": "docs",
}
html_css_files = ["custom.css"]

# -- Options for autosummary/autodoc output ------------------------------------
autosummary_generate = True
autoclass_content = "init"
autodoc_typehints = "description"
