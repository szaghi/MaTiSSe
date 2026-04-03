.PHONY: dev test lint fmt clean

dev:
	pip install -e ".[dev]"

test:
	python -m pytest --cov=matisse --cov-report=term-missing

lint:
	ruff check matisse/ tests/

fmt:
	ruff check --fix matisse/ tests/
	ruff format matisse/ tests/

clean:
	rm -rf dist/ build/ *.egg-info .pytest_cache .coverage coverage.xml
