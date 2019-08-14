#!/bin/bash -xe

buildah --storage-driver vfs info | grep metacopy
IMAGE=docker.io/${DOCKER_HUB_USERNAME}/${DOCKER_HUB_IMAGE}
TAG=$1
TAGGED_IMAGE=${IMAGE}:${TAG}

buildah --storage-driver vfs bud -t ${IMAGE} config/Dockerfiles/linchpin
buildah --storage-driver vfs push --authfile ${DOCKER_CREDS} ${IMAGE}
buildah --storage-driver vfs tag ${IMAGE} ${TAGGED_IMAGE}
buildah --storage-driver vfs push --authfile ${DOCKER_CREDS} ${IMAGE}
