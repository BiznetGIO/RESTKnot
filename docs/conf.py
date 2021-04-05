import os
import sys

sys.path.insert(0, os.path.abspath("../"))

project = "RESTKnot"
copyright = "2019, BiznetGio"
author = "BiznetGio"
version = "0.7.0"
templates_path = ["_templates"]

extensions = ["sphinx.ext.autodoc", "sphinx.ext.doctest", "sphinx.ext.autosectionlabel"]
autosectionlabel_prefix_document = True

source_suffix = ".rst"
master_doc = "index"
pygments_style = "sphinx"
html_theme = "alabaster"
pygments_style = "sphinx"
html_logo = "img/restknot-logo.svg"
html_static_path = ["_static"]
