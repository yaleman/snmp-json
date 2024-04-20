
.DEFAULT: help
.PHONY: help
help:
	@grep -E -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

REPO ?= snmp-json
IMAGE_NAME ?= yaleman/$(REPO):latest

.PHONY: container
container: ## Build the container
container:
	docker build -t $(IMAGE_NAME) .

.PHONY: mypy
mypy: ## Run mypy
mypy:
	poetry run mypy --strict snmp_json tests

.PHONY: ruff
ruff: ## Run ruff
ruff:
	poetry run ruff check snmp_json tests


.PHONY: pytest
pytest: ## Run pytest
pytest:
	poetry run pytest -s


.PHONY: checks
checks: ## Run all the tests
checks: pytest ruff mypy
	codespell

