# Delete all compiled Python files
.PHONY: clean
clean:
	poetry run python -m pyclean -v src/ tests/

# Lint using ruff (use `make format` to do formatting)
.PHONY: lint
lint:
	poetry run python -m ruff check src/

# Format source code with ruff
.PHONY: format
format:
	poetry run python -m ruff format src/ tests/

# Fixing import problems
.PHONY: fix-imports
fix-imports:
	poetry run ruff check --select I --fix  

# Run project tests.
.PHONY: test
test:
	poetry run pytest -v --cov=src --cov-report=term-missing --cov-fail-under=80 tests/

# Create .env file with variables.
.PHONY: env
env:
	@cp config/.env.example .env

# Create and launch service containers.
.PHONY: up
up:
	docker compose up -d
