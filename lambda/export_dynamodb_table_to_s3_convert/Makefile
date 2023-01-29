.PHONY: all
all: init format-check

.PHONY: init
init:
	pipenv install --dev

.PHONY: format
format:
	pipenv run black ./
	pipenv run isort ./

.PHONY: format-check
format-check:
	pipenv run black --check ./
	pipenv run isort ./ --check
