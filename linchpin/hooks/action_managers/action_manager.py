from abc import ABCMeta, abstractmethod
#action manager abstract class to be implemented by all 
# action mangers
class ActionManager(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def execute(self):
        pass
