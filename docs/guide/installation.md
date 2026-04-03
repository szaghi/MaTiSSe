# Installation

## Requirements

- Python **3.9** or newer
- pip

## Install from PyPI

```bash
pip install MaTiSSe.py
```

Verify the installation:

```bash
MaTiSSe.py --help
```

## Install from source

```bash
git clone https://github.com/szaghi/MaTiSSe.git
cd MaTiSSe
pip install -e ".[dev]"
```

The `.[dev]` extras install `pytest`, `pytest-cov`, and `ruff` for local development.

## Runtime dependencies

MaTiSSe.py depends on three Python packages, all installed automatically:

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
