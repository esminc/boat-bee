all: init format-check

init:
	pipenv install --dev

format:
	pipenv run black ./
	pipenv run isort ./

format-check:
	pipenv run black --check ./
	pipenv run isort ./ --check
