all: init format-check lint-check type-check test

init:
	pipenv install --dev

format:
	pipenv run black ./
	pipenv run isort ./
	prettier --write .

format-check:
	pipenv run black --check ./
	pipenv run isort ./ --check
	prettier --check ./

lint-check:
	pipenv run pylint app.py
	pipenv run pylint bee_slack_app

type-check:
	pipenv run mypy .

test: export AWS_DEFAULT_REGION := us-east-1
test: export DYNAMODB_TABLE := dummy-table-name
test:
	pipenv run pytest --verbose
