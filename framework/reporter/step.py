import logging
from abc import ABCMeta, abstractmethod

from framework.reporter.allure import Status


class Step:
    __metaclass__ = ABCMeta

    @abstractmethod
    def stepName(self) -> str:
        pass


class StepHandler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def startStep(self, step: Step):
        pass

    @abstractmethod
    def endStep(self, step: Step, status: Status):
        pass


class StepHandlerImpl(StepHandler):
    def startStep(self, step: Step):
        logging.info('step start: {}'.format(step.stepName()))

    def endStep(self, step: Step, status: Status):
        logging.info('step end: {} with result: {}'.format(step.stepName(), status))
