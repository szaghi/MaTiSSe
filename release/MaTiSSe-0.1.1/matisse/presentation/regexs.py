#!/usr/bin/env python
"""
regexs.py, module definition of main regular expressions.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import re
# MaTiSSe.py modules
from ..utils.utils import __expr__
# regular expressions
__section_pre__ = r"([^#]#|^#)\s+"
__subsection_pre__ = r"([^#]##|^##)\s+"
__slide_pre__ = r"([^#]###|^###)\s+"
__regex_section__    = re.compile(__section_pre__+__expr__)
__regex_subsection__ = re.compile(__subsection_pre__+__expr__)
__regex_slide__ = re.compile(__slide_pre__+__expr__)
__regex_titlepage__ = re.compile(r"([^#]#|^#)titlepage(\[(?P<plain>plain)\])*")
__regex_endtitlepage__ = re.compile(r"(?P<sec>"+__section_pre__+r".*)|(?P<subsec>"+__subsection_pre__+r".*)|(?P<slide>"+__slide_pre__+r".*)")
