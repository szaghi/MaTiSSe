#!/usr/bin/env python3
"""
matisse_config.py, module definition of MatisseConfig class.
"""

from __future__ import annotations

import os
import sys
from shutil import copyfile, copytree, rmtree

from pygments.styles import get_all_styles


class MatisseConfig(object):
    """
    MaTiSSe.py configuration.

    Attributes
    ----------
    __themes : list
      list of builtin themes
    """

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
          use local bundled copies of impress.js and MathJax instead of CDN
          versions; default False (CDN is used)
        code_highlight : bool
          use Pygments for server-side syntax highlighting of code blocks
        code_style : str
          Pygments style name; the list of available styles can be obtained
          via str_code_styles() or MaTiSSe.py --print-code-styles
        theme : str
          builtin theme chosen
        toc_at_chap_beginning : bool
          insert a slide with TOC at the beginning of each chapter (default false)
        toc_at_sec_beginning : bool
          insert a slide with TOC at the beginning of each section (default false)
        toc_at_subsec_beginning : bool
          insert a slide with TOC at the beginning of each subsection (default false)
        """
        self.backend = "impress"
        self.verbose = False
        self.offline = False
        self.code_highlight = True
        self.code_style = "default"
        self.theme = None
        self.toc_at_chap_beginning = None
        self.toc_at_sec_beginning = None
        self.toc_at_subsec_beginning = None
        self.pdf = False
        self.print_parsed_source = False
        self.__check_code_style()
        self.__get_themes()
        self.__check_theme()
        if cliargs:
            self.update(cliargs=cliargs)
        if self.verbose:
            print(self)

    def __str__(self):
        string = ["MaTiSSe.py configuration"]
        string.append(f"\n  Verbose mode: {self.verbose}")
        if self.offline:
            string.append("\n  Asset mode: offline (local bundles)")
        else:
            string.append("\n  Asset mode: online (CDN — impress.js 2, MathJax 3)")
        if self.code_highlight:
            string.append(f"\n  Code highlight style (Pygments): {self.code_style}")
        string.append(f"\n  Insert TOC at chapters beginning: {self.toc_at_chap_beginning}")
        string.append(f"\n  Insert TOC at sections beginning: {self.toc_at_sec_beginning}")
        string.append(f"\n  Insert TOC at subsections beginning: {self.toc_at_subsec_beginning}")
        return "".join(string)

    @staticmethod
    def __get_themes():
        """Get the builtin themes."""
        MatisseConfig.__themes = []
        themes = os.path.join(os.path.dirname(__file__), "utils/builtin_themes")
        for theme in os.listdir(themes):
            MatisseConfig.__themes.append(theme)

    _VALID_BACKENDS = frozenset({"impress", "reveal"})

    def __check_backend(self):
        """Validate the selected rendering backend."""
        if self.backend not in self._VALID_BACKENDS:
            sys.stderr.write(f"Error: unknown backend '{self.backend}'. Valid values: {sorted(self._VALID_BACKENDS)}\n")
            sys.stderr.write("Falling back to 'impress'.\n")
            self.backend = "impress"

    def __check_code_style(self):
        """Check if the selected Pygments style is available."""
        if self.code_style == "disable":
            self.code_highlight = False
            return
        available = sorted(get_all_styles())
        if self.code_style not in available:
            sys.stderr.write(f"Error: the selected Pygments style '{self.code_style}' is not available\n")
            sys.stderr.write("Restoring the default value 'default'\n")
            self.code_style = "default"

    def __check_theme(self):
        """Check if the selected builtin theme is available."""
        avail = False
        if self.theme:
            avail = self.theme in MatisseConfig.__themes
            if not avail:
                self.theme = None
                sys.stderr.write(f"Error: the selected builtin theme '{self.theme}' is not available")
                sys.stderr.write(self.str_themes())
        return avail

    def set_code_style(self, style: str) -> None:
        """Set Pygments code style performing availability check.

        Parameters
        ----------
        style : str
          Pygments style name, or 'disable' to turn off highlighting
        """
        self.code_style = style
        self.__check_code_style()

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
            themes = os.path.join(os.path.dirname(__file__), "utils/builtin_themes")
            for theme in os.listdir(themes):
                if theme == self.theme:
                    theme_path = os.path.join(os.path.join(themes, theme), "theme.yaml")
                    if os.path.exists(theme_path):
                        copytree(os.path.join(themes, theme), "theme-" + theme, dirs_exist_ok=True)
                        source_themed = (
                            r"$include(" + os.path.join("theme-" + theme, "theme.yaml") + ")\n" + source_themed
                        )
                        metadata_path = os.path.join(os.path.join(themes, theme), "metadata.yaml")
                        if os.path.exists(metadata_path):
                            source_themed = (
                                r"$include(" + os.path.join("theme-" + theme, "metadata.yaml") + ")\n" + source_themed
                            )
                        titlepage_path = os.path.join(os.path.join(themes, theme), "titlepage.md")
                        if os.path.exists(titlepage_path):
                            source_themed = (
                                r"$include(" + os.path.join("theme-" + theme, "titlepage.md") + ")\n" + source_themed
                            )
        return source_themed

    def str_code_styles(self):
        """Stringify the available Pygments code styles.

        Returns
        -------
        str
          string containing the list of available styles
        """
        string = ["Available Pygments code styles"]
        for style in sorted(get_all_styles()):
            string.append(style)
        return "\n  ".join(string) + "\n"

    # reveal.js built-in theme names (CDN — reveal.js 5)
    _REVEAL_THEMES = (
        "beige",
        "black",
        "blood",
        "dracula",
        "league",
        "moon",
        "night",
        "serif",
        "simple",
        "sky",
        "solarized",
        "white",
    )

    def str_themes(self):
        """Stringify the available themes for the current backend.

        For the impress backend, lists built-in theme directories from
        ``utils/builtin_themes/``.  For the reveal backend, lists the
        reveal.js built-in theme names (CDN-delivered).

        Returns
        -------
        str
          string containing the list of themes
        """
        if self.backend == "reveal":
            string = ["reveal.js built-in themes"]
            for theme in self._REVEAL_THEMES:
                string.append(theme)
            return "\n  ".join(string) + "\n"
        string = ["Builtin themes (impress backend)"]
        for theme in sorted(self.__themes):
            string.append(theme)
        return "\n  ".join(string) + "\n"

    def update(self, cliargs):
        """Update config state from command line arguments.

        Parameters
        ----------
        cliargs : argparse parsed object
          command line arguments parsed
        """
        self.backend = getattr(cliargs, "backend", "impress")
        self.__check_backend()
        self.verbose = cliargs.verbose
        self.offline = getattr(cliargs, "offline", False)
        self.set_code_style(style=getattr(cliargs, "code_style", self.code_style))
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
        Create output tree and copy MaTiSSe assets.

        **impress backend (default)**

        In online mode only ``countDown.js`` is copied; impress.js and MathJax
        are loaded from CDN.  In offline mode all local bundles are copied so
        the presentation works without a network connection.  Pygments CSS is
        always generated at build time — no CDN dependency, no extra bundle.

        **reveal backend**

        The reveal.js presentation is entirely CDN-based (reveal.js 5, MathJax 3).
        Only the output directory skeleton (``css/``, ``js/``) is created; no
        local asset bundles are copied.  ``--offline`` is not yet supported for
        the reveal backend and will emit a warning.

        Parameters
        ----------
        output: str
          output path
        """
        # ensure output directory exists
        if not os.path.exists(output):
            os.makedirs(output)
        # always create css/ and js/ subdirectories
        if not os.path.exists(os.path.join(output, "css")):
            os.makedirs(os.path.join(output, "css"))
        if not os.path.exists(os.path.join(output, "js")):
            os.makedirs(os.path.join(output, "js"))

        # always write pygments.css (build-time, no CDN, works offline automatically)
        if self.code_highlight:
            from .markdown_utils import get_pygments_css

            css_path = os.path.join(output, "css", "pygments.css")
            with open(css_path, "w") as fh:
                fh.write(get_pygments_css(style=self.code_style))

        if self.backend == "reveal":
            if self.offline:
                sys.stderr.write(
                    "Warning: --offline is not yet supported for --backend reveal. Assets will be loaded from CDN.\n"
                )
            # No local bundles for reveal — all CSS/JS comes from CDN
            return

        # --- impress backend assets ---
        css = os.path.join(os.path.dirname(__file__), "utils/css/normalize.css")
        copyfile(css, os.path.join(output, "css/normalize.css"))
        css = os.path.join(os.path.dirname(__file__), "utils/css/matisse_defaults.css")
        copyfile(css, os.path.join(output, "css/matisse_defaults.css"))
        css = os.path.join(os.path.dirname(__file__), "utils/css/matisse_defaults_printing.css")
        copyfile(css, os.path.join(output, "css/matisse_defaults_printing.css"))
        if self.offline:
            # MathJax engine (local bundle — MathJax 2.x)
            if os.path.exists(os.path.join(output, "js/MathJax")):
                rmtree(os.path.join(output, "js/MathJax"))
            jscript = os.path.join(os.path.dirname(__file__), "utils/js/MathJax")
            copytree(jscript, os.path.join(output, "js/MathJax"))
            # impress.js (local bundle)
            jscript = os.path.join(os.path.dirname(__file__), "utils/js/impress/impress.js")
            copyfile(jscript, os.path.join(output, "js/impress.js"))
        # countDown.js is always local (impress backend only)
        jscript = os.path.join(os.path.dirname(__file__), "utils/js/countDown.js")
        copyfile(jscript, os.path.join(output, "js/countDown.js"))
