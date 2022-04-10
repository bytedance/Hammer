# python 3.7
"""Configuration file for the Sphinx documentation builder.

For more details, please refer to

https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import os
import sys

# Setup path to the codebase.
sys.path.insert(0, os.path.abspath('../..'))

# Setup project information.
project = 'Hammer'

# Setup extensions.
extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx_copybutton',
    'sphinxcontrib.mermaid',
    'myst_parser',
    'autodocsumm'
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
source_suffix = ['.rst', '.md']

# Setup theme.
html_theme = 'furo'

# Setup paths.

# Add any paths that contain templates here, relative to this directory.
templates_path = []

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []


def setup(app):
    """Sets up customized configurations."""

    def remove_automodule_docstring(app, what, name, obj, options, lines):  # pylint: disable=unused-argument
        """Remove the docstring of automodule.

        For more details, please refer to

        https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#event-autodoc-process-docstring
        """
        if what == 'module':
            del lines[:2]  # Omit short description of automodule.

    app.connect('autodoc-process-docstring', remove_automodule_docstring)
