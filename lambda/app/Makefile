.PHONY: all
all: init format-check lint-check type-check test

.PHONY: init
init:
	pipenv install --dev

.PHONY: format
format:
	pipenv run black ./
	pipenv run isort ./
	prettier --write .

.PHONY: format-check
format-check:
	pipenv run black --check ./
	pipenv run isort ./ --check
	prettier --check ./

.PHONY: lint-check
lint-check:
	pipenv run pylint app.py
	pipenv run pylint bee_slack_app

.PHONY: type-check
type-check:
	pipenv run mypy . --disallow-untyped-calls --disallow-any-generics --disallow-untyped-decorators --warn-unused-ignores --no-implicit-optional --warn-unused-configs --disallow-subclassing-any

.PHONY: test
test: export AWS_DEFAULT_REGION := us-east-1
test: export DYNAMODB_TABLE := dummy-table-name
test:
	pipenv run pytest --verbose
