# Delete all compiled Python files
.PHONY: clean
clean:
	poetry run python -m pyclean -v src

# Lint using ruff (use `make format` to do formatting)
.PHONY: lint
lint:
	poetry run python -m ruff check src

# Format source code with ruff
.PHONY: format
format:
	poetry run python -m ruff format src
