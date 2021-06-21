from abc import abstractmethod, ABCMeta
from typing import List, Iterator

from framework.reporter.step import Step


class Executable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self): pass


class Action(Executable, Step):
    __metaclass__ = ABCMeta


class Route(Executable, Step):
    __metaclass__ = ABCMeta

    @abstractmethod
    def getExecutables(self) -> List[Executable]:
        pass


class ComboRoute(Route):
    def __init__(self, name: str, executables: Iterator[Executable]):
        self.name = name
        self.executables = list(executables)

    def stepName(self) -> str:
        return self.name

    def getExecutables(self) -> List[Executable]:
        return self.executables
