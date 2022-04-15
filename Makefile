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
	pipenv run pylint bee_slack_app

type-check:
	pipenv run mypy .

test:
	pipenv run pytest

train:
	cd ml && pipenv run python train.py

deploy:
	sls deploy

start-dev:
	pipenv run gunicorn --bind :3000 --workers 1 --threads 2 --timeout 0 --reload bee_slack_app.flask_app:flask_app

start-dynamodb:
	java -Djava.library.path=./dynamodb/DynamoDBLocal_lib -jar dynamodb/DynamoDBLocal.jar -sharedDb
