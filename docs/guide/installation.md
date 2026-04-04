# Installation

## Requirements

- Python **3.9** or newer
- pip

## Install from PyPI

```bash
pip install MaTiSSe.py
```

With [pipx](https://pypa.github.io/pipx/) (recommended for isolated installs):

```bash
pipx install MaTiSSe.py
```

Verify the installation:

```bash
matisse --version
```

## Install from source

```bash
git clone https://github.com/szaghi/MaTiSSe.git
cd MaTiSSe
pip install -e ".[dev]"
```

The `.[dev]` extras install `pytest`, `pytest-cov`, and `ruff` for local development.

## Runtime dependencies

MaTiSSe depends on three Python packages, all installed automatically:

| Package | Purpose |
|---|---|
| `markdown` | Markdown → HTML conversion |
| `yattag` | HTML generation |
| `pyyaml` | YAML theme and metadata parsing |

Frontend assets (impress.js, MathJax, highlight.js) are loaded from CDN at runtime by default and require no local installation. Use `--offline` to copy them into the output directory instead.

## Upgrading

```bash
pip install --upgrade MaTiSSe.py
```

## Platform notes

| Platform | Notes |
|---|---|
| Linux | Works on any modern distribution |
| macOS | Works with the standard Python installation |
| Windows | Use WSL (Windows Subsystem for Linux) or PowerShell with Python 3.9+ |

## Troubleshooting

**`matisse: command not found`**

If you installed with `pip install --user`, ensure `~/.local/bin` is on your `PATH`. `pipx` wires up the binary automatically.

**Module import errors**

Check Python version (`python --version` — must be 3.9+). If using a virtual environment, make sure it is activated before running `pip install`.

**Reinstall from source**

```bash
git clone https://github.com/szaghi/MaTiSSe.git
cd MaTiSSe
pip install -e ".[dev]"
```
