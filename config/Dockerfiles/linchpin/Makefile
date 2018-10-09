IMAGE_NAME = linchpin
CONTAINER_NAME = $(IMAGE_NAME)-z
REPO_URL ?= https://github.com/herlo/linchpin
REPO_REF ?= automate_lp

.PHONY: buildcontainer
buildcontainer:
	buildah bud -t ${IMAGE_NAME} .

.PHONY: testcontainer
testcontainer:
	buildah bud -t $(IMAGE_NAME)-candidate --build-arg "install_location=." \
	   --build-arg "git_project=$(REPO_URL)" --build-arg "git_branch=$(REPO_REF)" .
	IMAGE_NAME=$(IMAGE_NAME)-candidate CONTAINER_NAME=$(CONTAINER_NAME) ./test/run

