import logging
from abc import abstractmethod, ABCMeta

from framework.reporter.step import StepHandler, StepHandlerImpl


class Reporter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def beforeAll(self):
        pass

    @abstractmethod
    def startCase(self, case):
        pass

    @abstractmethod
    def passCase(self, case):
        pass

    @abstractmethod
    def failCase(self, case, e: BaseException):
        pass

    @abstractmethod
    def afterAll(self):
        pass

    @abstractmethod
    def stepHandler(self) -> StepHandler:
        pass

class ReporterImpl(Reporter):
    def beforeAll(self):
        logging.info('test begin')

    def startCase(self, case):
        logging.info('case: {}, started'.format(case.desc()))

    def passCase(self, case):
        logging.info('case: {}, pass'.format(case.desc()))

    def failCase(self, case, e: BaseException):
        logging.error("case: {}, failed".format(case.desc()))
        logging.exception(e)

    def afterAll(self):
        logging.info('test end')

    def stepHandler(self) -> StepHandler:
        return StepHandlerImpl()