# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sphinx_rtd_theme

project = 'py-qgis-server2'
copyright = '2023, David Marteau - 3liz'
author = 'David Marteau'
release = '${PIN_VERSION}'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_rtd_theme",
    "sphinxcontrib.httpdomain",
    "swagger_plugin_for_sphinx", 
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
html_static_path = [
    "specs/openapi-managment.yml",
]

# Fix for read the doc
# See https://github.com/readthedocs/readthedocs.org/issues/2569
master_doc = 'index'

# -- Swagger ---
# Note: for reading swagger doc one must use http server:
# ex  'python -m http.server doc/build'
swagger = [
    {
        "name": "Managment API",
        "page": "managment-api",
        "options": {"url": "_static/openapi-managment.yml"},
    },
]

