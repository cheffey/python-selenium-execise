from abc import abstractmethod
from typing import List

from framework.executable import Executable
from framework.operation.operation_factory import ActionFactory


class UseCase(ActionFactory):
    @abstractmethod
    def executables(self) -> List[Executable]:
        pass

    def desc(self) -> str:
        return '[{}]'.format(self.__class__.__name__)
