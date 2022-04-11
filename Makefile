all: init format-check lint-check type-check test

init:
	pipenv install --dev
	npm install

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
	pipenv run pylint src --recursive=y

type-check:
	pipenv run mypy .

test:
	pipenv run pytest

deploy:
	sls deploy
