from abc import ABCMeta, abstractmethod

class ActionManager(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def execute(self):
        pass
