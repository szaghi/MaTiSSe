# Contributing

Contributions are welcome — bug reports, feature requests, documentation improvements, and pull requests.

## Reporting issues

Open an issue on [GitHub](https://github.com/szaghi/MaTiSSe/issues). Include:

- MaTiSSe.py version (`MaTiSSe.py --version`)
- Python version (`python --version`)
- A minimal reproducer (source `.md` file or snippet)
- The error message or unexpected output

## Development setup

```bash
git clone https://github.com/szaghi/MaTiSSe.git
cd MaTiSSe
git checkout develop
pip install -e ".[dev]"
```

Work on the `develop` branch. The `master` branch is release-only.

## Running tests

```bash
make test          # pytest + coverage
make lint          # ruff check
make fmt           # ruff check --fix + ruff format
```

## Submitting a pull request

1. Fork the repository and create a branch from `develop`
2. Make your changes
3. Ensure `make test` and `make lint` pass
4. Open a pull request targeting `develop`

## Commit style

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(theme): add support for background images
fix(parser): handle nested fenced code blocks correctly
docs(guide): add offline mode page
```

Types used in the changelog: `feat`, `fix`, `perf`, `refactor`, `docs`.
