from abc import ABCMeta, abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from framework.action.action_impl import ClickAction, SendAction
from util.logistic import ConditionWait


class Element:
    __metaclass__ = ABCMeta

    @abstractmethod
    def desc(self) -> str:
        return self.__str__()

    @abstractmethod
    def fetch(self, web_driver: WebDriver) -> WebElement:
        pass

    def fetchWithRetry(self, web_driver: WebDriver, timeout_in_sec: int = 10) -> WebElement:
        message = 'Unable to find element: {} within {} seconds'.format(self.desc(), timeout_in_sec)
        return ConditionWait(timeout_in_sec).untilOrThrow(lambda: self.fetch(web_driver), message)

    def clickAction(self) -> ClickAction:
        return ClickAction(self)

    def sendAction(self, text: str) -> SendAction:
        return SendAction(self, text)


class ElementImpl(Element):
    def desc(self) -> str:
        return '[by: {} value: {}]'.format(self.by, self.value)

    def __init__(self, by: str, value: str):
        self.by = by
        self.value = value

    def fetch(self, web_driver: WebDriver) -> WebElement:
        return web_driver.find_element(self.by, self.value)
