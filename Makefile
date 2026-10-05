.PHONY: install dev test lint format clean build publish

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/

lint:
	ruff check src/ tests/
	mypy src/ --ignore-missing-imports

format:
	black src/ tests/
	ruff check --fix src/ tests/

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +

build:
	python -m build

publish: build
	twine upload dist/*
