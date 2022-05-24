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
	pipenv run pylint app.py app_local.py
	pipenv run pylint bee_slack_app

type-check:
	pipenv run mypy .

test: export AWS_DEFAULT_REGION := us-east-1
test: export DYNAMODB_TABLE := bee-dev
test:
	pipenv run pytest

train:
	cd ml && pipenv run python train.py

deploy: deploy-dev
deploy-dev:
	sls deploy --stage dev

deploy-prod:
	sls deploy --stage prod

start-dev: export AWS_DEFAULT_REGION := us-east-1
start-dev: export DYNAMODB_TABLE := bee-dev
start-dev: export DYNAMODB_ENDPOINT := http://localhost:8000
start-dev: export AWS_ACCESS_KEY_ID := local
start-dev: export AWS_SECRET_ACCESS_KEY := local
start-dev: export NOTIFY_POST_REVIEW_CHANNEL := C03AXBQNFPV
start-dev: export ASSETS_PATH := ./assets/
start-dev:
	pipenv run gunicorn --bind :3000 --workers 1 --threads 2 --timeout 0 --reload app_local:flask_app

start-dynamodb:
	sls dynamodb start --migrate

start-admin:
	npm start
