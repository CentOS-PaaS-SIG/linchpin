PARENT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/../../)

DISTROS := fedora27 centos7 fedora26

.PHONY: all
all:
	set -e; for i in $(DISTROS); do \
		docker build -f $$i/Dockerfile -t lp_$$i .; \
	done

test: all
	./run_tests.sh $(PARENT_DIR) "$(DISTROS)"

pip_install.sh: ../../requirements.txt
	./gen_pip_install.sh

