from __future__ import absolute_import
from abc import ABCMeta, abstractmethod
import six

# action manager abstract class to be implemented by all
# action managers


class ActionManager(six.with_metaclass(ABCMeta, object)):

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def execute(self):
        pass
