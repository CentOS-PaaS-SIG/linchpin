IMAGE_NAME = linchpin
CONTAINER_NAME = $(IMAGE_NAME)-z
INSTALL_LOCATION ?= .
REPO_URL ?= https://github.com/CentOS-PaaS-SIG/linchpin
REPO_REF ?= develop

.PHONY: buildcontainer
buildcontainer:
	buildah bud -t $(IMAGE_NAME) --build-arg "install_location=$(INSTALL_LOCATION)" \
	   --build-arg "git_project=$(REPO_URL)" --build-arg "git_branch=$(REPO_REF)" .

.PHONY: testcontainer
testcontainer:
	buildah bud -t $(IMAGE_NAME)-candidate --build-arg "install_location=$(INSTALL_LOCATION)" \
	   --build-arg "git_project=$(REPO_URL)" --build-arg "git_branch=$(REPO_REF)" .
	IMAGE_NAME=$(IMAGE_NAME)-candidate CONTAINER_NAME=$(CONTAINER_NAME) ./test/run

