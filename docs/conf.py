# pylint: skip-file
import sys
from os.path import abspath, dirname

sys.setrecursionlimit(2000)
sys.path.insert(1, dirname(dirname(abspath(__file__))))

project = "restcountries_cli"
copyright = "2023, Martín Galdeano Cañizares"
author = "Martín Galdeano Cañizares"
version = release = "0.0.0"

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.extlinks",
    "sphinx_copybutton",
    "sphinx.ext.autosectionlabel",
]
autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 2
source_suffix = ".rst"
master_doc = "index"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
templates_path = []
html_theme = "furo"
epub_show_urls = "footnote"
