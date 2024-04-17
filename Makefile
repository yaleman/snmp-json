
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


