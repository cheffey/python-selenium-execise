from abc import ABCMeta, abstractmethod

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

import constant
from framework.element.element import Element


class Driver:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_web_driver(self) -> WebDriver:
        pass

    @abstractmethod
    def click(self, ele: Element):
        pass

    @abstractmethod
    def open(self, url: str):
        pass

    @abstractmethod
    def send(self, ele: Element, text: str):
        pass

    @abstractmethod
    def getTitle(self):
        pass


class DriverImpl(Driver):
    def __init__(self, __web_driver: WebDriver):
        self.__web_driver = __web_driver

    def get_web_driver(self) -> WebDriver:
        return self.__web_driver

    def open(self, url: str):
        self.__web_driver.get(url)

    def click(self, ele: Element):
        ele.fetchWithRetry(self.__web_driver).click()

    def send(self, ele: Element, text: str):
        web_ele = ele.fetchWithRetry(self.__web_driver)
        web_ele.send_keys(text)

    def getTitle(self):
        return self.__web_driver.title


class Device:
    def __init__(self, driver: Driver):
        self.driver = driver


class DeviceConfig:
    __metaclass__ = ABCMeta

    @abstractmethod
    def connect(self) -> tuple[Device, Driver]:
        pass


class Chrome(DeviceConfig):
    def connect(self) -> tuple[Device, Driver]:
        web_driver = webdriver.Chrome(constant.CHROME_WEB_DRIVER_PATH)
        driver = DriverImpl(web_driver)
        device = Device(driver)
        return device, driver
