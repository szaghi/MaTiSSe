#!/usr/bin/env python3
"""
matisse_config.py, module definition of MatisseConfig class.
"""
from __future__ import annotations
import os
from shutil import copyfile, copytree, rmtree
import sys


class MatisseConfig(object):
  """
  MaTiSSe.py configuration.

  Attributes
  ----------
  __highlight_styles : list
    list of available highlight.js styles
  __themes : list
    list of builtin themes
  """
  __highlight_styles = []
  __themes = []

  def __init__(self, cliargs=None):
    """
    Parameters
    ----------
    cliargs : argparse parsed object
      command line arguments parsed

    Attributes
    ----------
    verbose : bool
      more verbose printing messages (default no)
    offline : bool
      use local bundled copies of impress.js, MathJax and highlight.js instead
      of CDN versions; default False (CDN is used)
    highlight : bool
      use highlight.js for syntax highlighting of code blocks
    highlight_style : str
      css style file for highlight.js; the list of available styles can be printed
      by 'str_highlight_styles' method
    theme : str
      builtin theme chosen
    toc_at_chap_beginning : bool
      insert a slide with TOC at the beginning of each chapter (default false)
    toc_at_sec_beginning : bool
      insert a slide with TOC at the beginning of each section (default false)
    toc_at_subsec_beginning : bool
      insert a slide with TOC at the beginning of each subsection (default false)
    """
    self.verbose = False
    self.offline = False
    self.highlight = True
    self.highlight_style = 'github.css'
    self.theme = None
    self.toc_at_chap_beginning = None
    self.toc_at_sec_beginning = None
    self.toc_at_subsec_beginning = None
    self.pdf = False
    self.print_parsed_source = False
    self.__get_highlight_styles()
    self.__check_highlight_style()
    self.__get_themes()
    self.__check_theme()
    if cliargs:
      self.update(cliargs=cliargs)
    if self.verbose:
      print(self)

  def __str__(self):
    string = ['MaTiSSe.py configuration']
    string.append(f'\n  Verbose mode: {self.verbose}')
    if self.offline:
      string.append('\n  Asset mode: offline (local bundles)')
    else:
      string.append('\n  Asset mode: online (CDN — impress.js 2, MathJax 3, highlight.js 11)')
    if self.highlight:
      string.append(f'\n  Highlight.js style: {self.highlight_style}')
    string.append(f'\n  Insert TOC at chapters beginning: {self.toc_at_chap_beginning}')
    string.append(f'\n  Insert TOC at sections beginning: {self.toc_at_sec_beginning}')
    string.append(f'\n  Insert TOC at subsections beginning: {self.toc_at_subsec_beginning}')
    return ''.join(string)

  @staticmethod
  def __get_highlight_styles():
    """Get the available highlight.js styles."""
    MatisseConfig.__highlight_styles = []
    hilite_styles = os.path.join(os.path.dirname(__file__), 'utils/js/highlight/styles')
    for css in os.listdir(hilite_styles):
      if css.endswith(".css"):
        MatisseConfig.__highlight_styles.append(css)

  @staticmethod
  def __get_themes():
    """Get the builtin themes."""
    MatisseConfig.__themes = []
    themes = os.path.join(os.path.dirname(__file__), 'utils/builtin_themes')
    for theme in os.listdir(themes):
      MatisseConfig.__themes.append(theme)

  def __check_highlight_style(self):
    """Check if the selected highlight.js style is available."""
    if self.highlight_style != 'disable':
      avail = (self.highlight_style in MatisseConfig.__highlight_styles)
      if not avail:
        sys.stderr.write(f"Error: the selected highlight.js style '{self.highlight_style}' is not available")
        sys.stderr.write("\nRestore the default value 'github.css'\n")
        self.highlight_style = 'github.css'
        sys.stderr.write(self.str_highlight_styles())
    else:
      avail = False
      self.highlight = False
    return avail

  def __check_theme(self):
    """Check if the selected builtin theme is available."""
    avail = False
    if self.theme:
      avail = (self.theme in MatisseConfig.__themes)
      if not avail:
        self.theme = None
        sys.stderr.write(f"Error: the selected builtin theme '{self.theme}' is not available")
        sys.stderr.write(self.str_themes())
    return avail

  def set_highlight_style(self, style: str) -> None:
    """Set highlight.js style performing availability check.

    Parameters
    ----------
    style : str
      style file name
    """
    self.highlight_style = style
    self.__check_highlight_style()

  def set_theme(self, theme: str) -> None:
    """Set builtin theme performing availability check.

    Parameters
    ----------
    theme : str
      theme file name
    """
    self.theme = theme
    self.__check_theme()

  def put_theme(self, source, output):
    """Put builtin theme into the source.

    Must be called after the output tree has been made.

    Parameters
    ----------
    source : str
      source of presentation
    output: str
      output path

    Returns
    -------
    str
      source of presentation with theme included
    """
    source_themed = source
    if self.theme:
      themes = os.path.join(os.path.dirname(__file__), 'utils/builtin_themes')
      for theme in os.listdir(themes):
        if theme == self.theme:
          theme_path = os.path.join(os.path.join(themes, theme), 'theme.yaml')
          if os.path.exists(theme_path):
            copytree(os.path.join(themes, theme), 'theme-' + theme, dirs_exist_ok=True)
            source_themed = r'$include(' + os.path.join('theme-' + theme, 'theme.yaml') + ')\n' + source_themed
            metadata_path = os.path.join(os.path.join(themes, theme), 'metadata.yaml')
            if os.path.exists(metadata_path):
              source_themed = r'$include(' + os.path.join('theme-' + theme, 'metadata.yaml') + ')\n' + source_themed
            titlepage_path = os.path.join(os.path.join(themes, theme), 'titlepage.md')
            if os.path.exists(titlepage_path):
              source_themed = r'$include(' + os.path.join('theme-' + theme, 'titlepage.md') + ')\n' + source_themed
    return source_themed

  def str_highlight_styles(self):
    """Stringify the available highlight.js styles.

    Returns
    -------
    str
      string containing the list of available styles
    """
    string = ['Available highlight.js styles']
    for style in sorted(self.__highlight_styles):
      string.append(style)
    return '\n  '.join(string) + '\n'

  def str_themes(self):
    """Stringify the builtin themes.

    Returns
    -------
    str
      string containing the list of builtin themes
    """
    string = ['Builtin themes']
    for theme in sorted(self.__themes):
      string.append(theme)
    return '\n  '.join(string) + '\n'

  def update(self, cliargs):
    """Update config state from command line arguments.

    Parameters
    ----------
    cliargs : argparse parsed object
      command line arguments parsed
    """
    self.verbose = cliargs.verbose
    self.offline = getattr(cliargs, 'offline', False)
    self.set_highlight_style(style=cliargs.highlight_style)
    self.set_theme(theme=cliargs.theme)
    self.toc_at_chap_beginning = cliargs.toc_at_chap_beginning
    self.toc_at_sec_beginning = cliargs.toc_at_sec_beginning
    self.toc_at_subsec_beginning = cliargs.toc_at_subsec_beginning
    self.pdf = cliargs.pdf
    self.print_parsed_source = cliargs.print_parsed_source

  def printf(self):
    """Print config data with verbosity check."""
    if self.verbose:
      print(self)

  def make_output_tree(self, output: str) -> None:
    """
    Create output tree and copy MaTiSSe.py assets.

    In online mode (default) only countDown.js is copied; impress.js, MathJax
    and highlight.js are loaded from CDN.  In offline mode all local bundles
    are copied so the presentation works without a network connection.

    Parameters
    ----------
    output: str
      output path
    """
    # checking output directory
    if not os.path.exists(output):
      os.makedirs(output)
    # creating css directory
    if not os.path.exists(os.path.join(output, 'css')):
      os.makedirs(os.path.join(output, 'css'))
    # normalize.css
    css = os.path.join(os.path.dirname(__file__), 'utils/css/normalize.css')
    copyfile(css, os.path.join(output, 'css/normalize.css'))
    css = os.path.join(os.path.dirname(__file__), 'utils/css/matisse_defaults.css')
    copyfile(css, os.path.join(output, 'css/matisse_defaults.css'))
    css = os.path.join(os.path.dirname(__file__), 'utils/css/matisse_defaults_printing.css')
    copyfile(css, os.path.join(output, 'css/matisse_defaults_printing.css'))
    # creating jscript directory
    if not os.path.exists(os.path.join(output, 'js')):
      os.makedirs(os.path.join(output, 'js'))
    if self.offline:
      # MathJax engine (local bundle — MathJax 2.x)
      if os.path.exists(os.path.join(output, 'js/MathJax')):
        rmtree(os.path.join(output, 'js/MathJax'))
      jscript = os.path.join(os.path.dirname(__file__), 'utils/js/MathJax')
      copytree(jscript, os.path.join(output, 'js/MathJax'))
      # highlight.js (local bundle)
      if self.highlight:
        if os.path.exists(os.path.join(output, 'js/highlight')):
          rmtree(os.path.join(output, 'js/highlight'))
        jscript = os.path.join(os.path.dirname(__file__), 'utils/js/highlight')
        copytree(jscript, os.path.join(output, 'js/highlight'))
      # impress.js (local bundle)
      jscript = os.path.join(os.path.dirname(__file__), 'utils/js/impress/impress.js')
      copyfile(jscript, os.path.join(output, 'js/impress.js'))
    # countDown.js is always local
    jscript = os.path.join(os.path.dirname(__file__), 'utils/js/countDown.js')
    copyfile(jscript, os.path.join(output, 'js/countDown.js'))
