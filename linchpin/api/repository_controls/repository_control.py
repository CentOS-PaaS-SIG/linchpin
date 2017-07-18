from abc import ABCMeta, abstractmethod

class RepositoryControl(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def fetch_files(self):
        pass
