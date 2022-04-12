all: init format-check lint-check type-check test

init:
	pipenv install --dev
	cd app && npm install

format:
	pipenv run black ./
	pipenv run isort ./
	prettier --write .

format-check:
	pipenv run black --check ./
	pipenv run isort ./ --check
	prettier --check ./

lint-check:
	pipenv run pylint app/app.py
	pipenv run pylint app/bee_slack_app

type-check:
	pipenv run mypy .

test:
	pipenv run pytest

deploy:
	cd app && sls deploy
