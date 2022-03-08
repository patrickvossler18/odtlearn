# -*- coding: utf-8 -*-
#
# odtlearn documentation build configuration file, created by
# sphinx-quickstart on Mon Jan 18 14:44:12 2016.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os

import sphinx_gallery
import sphinx_rtd_theme

# Add to sys.path the top-level directory where the package is located.
sys.path.insert(0, os.path.abspath(".."))

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('.'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "myst_parser",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "numpydoc",
    "sphinx_gallery.gen_gallery",
    "sphinx_toggleprompt",
]

# this is needed for some reason...
# see https://github.com/numpy/numpydoc/issues/69
numpydoc_show_class_members = False

# pngmath / imgmath compatibility layer for different sphinx versions
import sphinx
from distutils.version import LooseVersion

if LooseVersion(sphinx.__version__) < LooseVersion("1.4"):
    extensions.append("sphinx.ext.pngmath")
else:
    extensions.append("sphinx.ext.imgmath")

autodoc_default_flags = ["members", "inherited-members"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# generate autosummary even if no references
autosummary_generate = True

# The suffix of source filenames.
source_suffix = ".rst"

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# Generate the plots for the gallery
plot_gallery = False

# The master toctree document.
master_doc = "index"

# General information about the project.
project = u"odtlearn"
# copyright = u'2022, Patrick Vossler'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
from odtlearn import _version

version = _version.__version__
# The full version, including alpha/beta/rc tags.
release = _version.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build", "_templates"]

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False


# Custom style


# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# html_theme = "sphinxawesome_theme"

# html_awesome_docsearch = False
# # Theme options are theme-specific and customize the look and feel of a theme
# # further.  For a list of options available for each theme, see the
# # documentation.
# html_theme_options = {
#     "show_scrolltop": True,
#     "extra_header_links": {
#         "Docs": "/index",
#         "About": "/about",
#         "repository on GitHub": {
#             "link": "https://github.com/patrickvossler18/decision_tree_estimators/",
#             "icon": (
#                 '<svg style="height: 26px; margin-top: -2px;" viewBox="0 0 45 44" '
#                 'fill="currentColor" xmlns="http://www.w3.org/2000/svg">'
#                 '<path fill-rule="evenodd" clip-rule="evenodd" '
#                 'd="M22.477.927C10.485.927.76 10.65.76 22.647c0 9.596 6.223 17.736 '
#                 "14.853 20.608 1.087.2 1.483-.47 1.483-1.047 "
#                 "0-.516-.019-1.881-.03-3.693-6.04 "
#                 "1.312-7.315-2.912-7.315-2.912-.988-2.51-2.412-3.178-2.412-3.178-1.972-1.346.149-1.32.149-1.32 "  # noqa
#                 "2.18.154 3.327 2.24 3.327 2.24 1.937 3.318 5.084 2.36 6.321 "
#                 "1.803.197-1.403.759-2.36 "
#                 "1.379-2.903-4.823-.548-9.894-2.412-9.894-10.734 "
#                 "0-2.37.847-4.31 2.236-5.828-.224-.55-.969-2.759.214-5.748 0 0 "
#                 "1.822-.584 5.972 2.226 "
#                 "1.732-.482 3.59-.722 5.437-.732 1.845.01 3.703.25 5.437.732 "
#                 "4.147-2.81 5.967-2.226 "
#                 "5.967-2.226 1.185 2.99.44 5.198.217 5.748 1.392 1.517 2.232 3.457 "
#                 "2.232 5.828 0 "
#                 "8.344-5.078 10.18-9.916 10.717.779.67 1.474 1.996 1.474 4.021 0 "
#                 "2.904-.027 5.247-.027 "
#                 "5.96 0 .58.392 1.256 1.493 1.044C37.981 40.375 44.2 32.24 44.2 "
#                 '22.647c0-11.996-9.726-21.72-21.722-21.72" '
#                 'fill="currentColor"/></svg>'
#             ),
#         },
#     },
# }

# Add any paths that contain custom themes here, relative to this directory.
# The name of the Pygments (syntax highlighting) style to use.

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = "sphinx"
# html_theme = "sphinx_rtd_theme"
# html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
# html_style = "css/odtlearn.css"
html_theme = "furo"
# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = False

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = "odtlearndoc"


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    ("index", "odtlearn.tex", u"odtlearn Documentation", u"Patrick Vossler", "manual"),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [("index", "odtlearn", u"odtlearn Documentation", [u"Patrick Vossler"], 1)]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        "index",
        "odtlearn",
        u"odtlearn Documentation",
        u"Patrick Vossler",
        "odtlearn",
        "One line description of project.",
        "Miscellaneous",
    ),
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False


# Example configuration for intersphinx: refer to the Python standard library.
# intersphinx configuration
intersphinx_mapping = {
    "python": ("https://docs.python.org/{.major}".format(sys.version_info), None),
    "numpy": ("https://docs.scipy.org/doc/numpy/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference", None),
    "matplotlib": ("https://matplotlib.org/", None),
    "sklearn": ("http://scikit-learn.org/stable", None),
}

# sphinx-gallery configuration
sphinx_gallery_conf = {
    "doc_module": "skltemplate",
    "backreferences_dir": os.path.join("generated"),
    "reference_url": {"skltemplate": None},
    "filename_pattern": r"fit_*",
}


# copybutton strip prompt text
copybutton_prompt_text = ">>> "

# toggle prompt
toggleprompt_offset_right = 30

# GH REPO URL
# rst_prolog = """
# .. |repo| replace:: https://github.com/D3M-Research-Group/decision_tree_estimators.git#egg=odtlearn
# """

# def setup(app):
# a copy button to copy snippet of code from the documentation
# app.add_js_file("js/copybutton.js")
