from abc import abstractmethod, ABCMeta

from framework.context import Context


class Condition:
    __metaclass__ = ABCMeta

    @abstractmethod
    def verify(self) -> bool:
        pass

    @abstractmethod
    def desc(self) -> str:
        pass


class TitleIs(Condition):
    def __init__(self, title: str):
        self.title = title

    def verify(self) -> bool:
        return Context.getDriver().getTitle() == self.title

    def desc(self) -> str:
        return 'title is {}'.format(self.title)
