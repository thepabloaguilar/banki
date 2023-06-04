.PHONY: fix-imports
fix-imports:
	poetry run isort .

# TESTS

.PHONY: unit-test
unit-test:
	poetry run pytest -m "not integration"

.PHONY: integration-test
integration-test:
	poetry run pytest -m integration

.PHONY: typing-test
typing-test:
	# We're not type checking `gateways/db` because some errors regarding the SQLAlchemy plugin.
	poetry run mypy banki/api
	poetry run mypy banki/entities
	poetry run mypy banki/extensions
	poetry run mypy banki/use_cases
	poetry run mypy banki/vo
	poetry run mypy banki/gateways/email
	poetry run mypy tests

.PHONY: style-test
style-test:
	poetry run flake8 .

.PHONY: test
test: style-test typing-test unit-test

.PHONY: test-full
test-full: style-test typing-test
	poetry run pytest .
	poetry run poetry check
	poetry run safety check --full-report

# MIGRATION

.PHONY: migration-up
migration-up:
	poetry run alembic upgrade head

.PHONY: migration-down
migration-down:
	poetry run alembic downgrade base

# APP

.PHONY: run-app
run-app:
	poetry run uvicorn banki.main:app --port 6000 --reload

# UTILS

.PHONY: export-requirements
export-requirements:
	poetry export -f requirements.txt --output requirements.txt
