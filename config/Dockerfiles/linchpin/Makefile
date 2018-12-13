IMAGE_NAME = linchpin
CONTAINER_NAME = $(IMAGE_NAME)-z
INSTALL_LOCATION ?= .
REPO_URL ?= https://github.com/CentOS-PaaS-SIG/linchpin
REPO_REF ?= develop

USERNAME ?= dummy_username
PASSWORD ?= dummy_password
VERSION ?= dummy_version
CONTAINER_REGISTRY ?= docker://docker.io
CONTAINER_NAMESPACE ?= contrainfra


.PHONY: build
build:
	buildah bud -t $(IMAGE_NAME) --build-arg "install_location=$(INSTALL_LOCATION)" \
	   --build-arg "git_project=$(REPO_URL)" --build-arg "git_branch=$(REPO_REF)" .

.PHONY: test
test:
	buildah bud -t $(IMAGE_NAME)-candidate --build-arg "install_location=$(INSTALL_LOCATION)" \
	   --build-arg "git_project=$(REPO_URL)" --build-arg "git_branch=$(REPO_REF)" .
	IMAGE_NAME=$(IMAGE_NAME)-candidate CONTAINER_NAME=$(CONTAINER_NAME) ./test/run

.PHONY: push
push:
	buildah tag localhost/$(IMAGE_NAME)-candidate:latest localhost/$(IMAGE_NAME)-candidate:$(VERSION)
	buildah push --creds $(USERNAME)\:$(PASSWORD) localhost/$(IMAGE_NAME)-candidate\:$(VERSION) \
    $(CONTAINER_REGISTRY)/$(CONTAINER_NAMESPACE)/$(IMAGE_NAME)\:$(VERSION)

