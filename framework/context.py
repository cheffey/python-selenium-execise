from typing import List

from framework.exceptions import NotFoundException
from framework.reporter.reporter import Reporter
from util.threadlocal import ThreadLocal


class Context:
    THREAD_LOCAL_CONTEXT = None

    def __init__(self):
        self.driver = None
        self.device = None
        self.reporters = []

    @classmethod
    def getDriver(cls):
        context = Context.THREAD_LOCAL_CONTEXT.get()
        if context.driver is None:
            raise NotFoundException("Unable to find driver")
        return context.driver

    @classmethod
    def setDriver(cls, driver):
        Context.THREAD_LOCAL_CONTEXT.get().driver = driver

    @classmethod
    def getDevice(cls):
        context = Context.THREAD_LOCAL_CONTEXT.get()
        if context.device is None:
            raise NotFoundException("Unable to find device")
        return context.device

    @classmethod
    def setDevice(cls, device):
        Context.THREAD_LOCAL_CONTEXT.get().device = device

    @classmethod
    def reporters(cls) -> List[Reporter]:
        return Context.THREAD_LOCAL_CONTEXT.get().reporters


Context.THREAD_LOCAL_CONTEXT = ThreadLocal.withInitial(lambda: Context())
