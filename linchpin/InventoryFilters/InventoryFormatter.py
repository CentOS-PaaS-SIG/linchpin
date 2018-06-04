#!/usr/bin/env python

import abc


class InventoryFormatter:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def add_sections(self, section_list):
        pass

    @abc.abstractmethod
    def set_children(self, inv):
        pass

    @abc.abstractmethod
    def set_vars(self, inv):
        pass

    @abc.abstractmethod
    def add_ips_to_groups(self, inven_hosts, layout):
        pass

    @abc.abstractmethod
    def add_common_vars(self, host_groups, layout):
        pass

    @abc.abstractmethod
    def generate_inventory(self):
        pass
