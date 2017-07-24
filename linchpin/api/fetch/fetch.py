from abc import ABCMeta, abstractmethod

class Fetch(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def fetch_files(self):
        pass

    def copy_files(self):
        pass

