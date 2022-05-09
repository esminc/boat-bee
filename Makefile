all: init format-check lint-check type-check test

init:
	pipenv install --dev
	npm install
	sls dynamodb install

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
test: export DYNAMODB_TABLE := bee-dev
test:
	pipenv run pytest bee_slack_app/service/test_review.py -vv

train:
	cd ml && pipenv run python train.py

deploy:
	sls deploy

start-dev: export AWS_DEFAULT_REGION := us-east-1
start-dev: export DYNAMODB_TABLE := bee-dev
start-dev: export DYNAMODB_ENDPOINT := http://localhost:8000
start-dev: export AWS_ACCESS_KEY_ID := local
start-dev: export AWS_SECRET_ACCESS_KEY := local
start-dev:
	pipenv run gunicorn --bind :3000 --workers 1 --threads 2 --timeout 0 --reload bee_slack_app.flask_app:flask_app

start-dynamodb:
	sls dynamodb start --migrate

start-admin:
	npm start
