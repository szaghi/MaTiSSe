#!/usr/bin/env python3
"""
markdown_utils.py, module definition of markdown utils functions.
"""

import markdown
from pygments.formatters import HtmlFormatter

from .mdx_custom_span_class import CustomSpanClassExtension
from .mdx_mathjax import MathJaxExtension

try:
    from markdown_checklist.extension import ChecklistExtension

    __mdx_checklist__ = True
except ImportError:
    __mdx_checklist__ = False


def get_pygments_css(style: str = "default", css_class: str = "highlight") -> str:
    """Return the Pygments CSS stylesheet for the given style name."""
    return HtmlFormatter(style=style, cssclass=css_class).get_style_defs(f".{css_class}")


def markdown2html(source, no_p=False, code_style="default"):
    """Convert markdown source to html.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    no_p : bool, optional
      if True the converted contents is not inserted into the <p></p> tags
    code_style : str, optional
      Pygments style name used by the codehilite extension (default: 'default')

    Returns
    -------
    str
      converted source
    """
    extensions = [
        "smarty",
        "fenced_code",
        CustomSpanClassExtension(),
        MathJaxExtension(),
        "codehilite",
    ]
    if __mdx_checklist__:
        extensions.append(ChecklistExtension())

    extension_configs = {
        "codehilite": {
            "css_class": "highlight",
            "pygments_style": code_style,
            "guess_lang": False,
            "noclasses": False,
        }
    }

    mkd = markdown.Markdown(
        output_format="html5",
        extensions=extensions,
        extension_configs=extension_configs,
    )
    markup = mkd.reset().convert(source)
    if no_p:
        p_start = "<p>"
        p_end = "</p>"
        if markup.startswith(p_start) and markup.endswith(p_end):
            markup = markup[len(p_start) : -len(p_end)]
    return markup
