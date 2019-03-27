IMAGE=docker.io/${DOCKER_HUB_USERNAME}/${DOCKER_HUB_IMAGE}
TAG=$1
TAGGED_IMAGE=${IMAGE}:${TAG}

buildah bud -t ${IMAGE} .
buildah push --authfile ${DOCKER_CREDS} ${IMAGE}
buildah tag ${IMAGE} ${TAGGED_IMAGE}
buildah push --authfile ${DOCKER_CREDS} ${IMAGE}
