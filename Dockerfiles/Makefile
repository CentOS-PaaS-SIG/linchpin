PARENT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/../)

TARGETS := fedora27 centos7 fedora26 fedora25 centos6
DRIVERS := dummy duffy libvirt

.PHONY: all
all: pip_install.sh
	set -e; for i in $(TARGETS); do \
		docker build -f $$i/Dockerfile -t lp_$$i .; \
	done

test: all
	set -e; for i in $(TARGETS); do \
		./run_tests.sh lp_$$i $(PARENT_DIR) $(DRIVERS); \
	done

pip_install.sh: ../requirements.txt
	./gen_pip_install.sh

