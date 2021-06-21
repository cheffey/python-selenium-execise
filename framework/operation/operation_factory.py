from typing import List

from framework.action.action_impl import OpenAction, ClickAction, SendAction, AssertAction
from framework.element.element import Element, ElementImpl
from framework.executable import Executable, Route, ComboRoute
from framework.logistic.condition import TitleIs


class OperationFactory:
    def withIdElement(self, id: str) -> Element:
        return ElementImpl("id", id)

    def element(self, by: str, value: str) -> Element:
        return ElementImpl(by, value)

    def executablesOf(self, *executables: Executable) -> List[Executable]:
        return list(executables)

    def routesOf(self, name: str, *args: Executable) -> Route:
        return ComboRoute(name, args)


class ActionFactory(OperationFactory):
    def open(self, url: str) -> OpenAction:
        return OpenAction(url)

    def assertTitle(self, title: str) -> AssertAction:
        return AssertAction(TitleIs(title))
