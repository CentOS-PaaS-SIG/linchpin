# Beware: only meant for use with pkg2appimage-with-docker

FROM ubuntu:xenial

MAINTAINER "TheAssassin <theassassin@users.noreply.github.com>"

ENV DEBIAN_FRONTEND=noninteractive \
    DOCKER_BUILD=1

RUN sed -i 's/archive.ubuntu.com/ftp.fau.de/g' /etc/apt/sources.list ;\
    echo "deb http://ppa.launchpad.net/deadsnakes/ppa/ubuntu xenial main" >> /etc/apt/sources.list ;\
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F23C5A6CF475977595C89F51BA6932366A755776 ;\
    apt-get update
RUN apt-get install -y python3.7 python3.7-dev python3.7-venv python3.7-distutils ;\
    python3.7 -m ensurepip --default-pip ;\
    python3.7 -m pip install --upgrade pip setuptools wheel virtualenv
RUN apt-get install -y apt-transport-https libcurl3-gnutls libarchive13 wget desktop-file-utils aria2 gnupg2 build-essential file libglib2.0-bin git sudo
RUN apt-get install -y pkg-config libvirt-dev
RUN apt-get install -y fuse || true
RUN install -m 0777 -d /workspace

RUN adduser --system --uid 1000 test

WORKDIR /workspace
