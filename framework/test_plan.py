import inspect
import importlib
import logging
from os import listdir
from typing import List, Iterator

from framework.context import Context
from framework.base.base_case import UseCase
from framework.device.device import DeviceConfig
from framework.flow import TestFlow
from framework.reporter.reporter import ReporterImpl
from util.exceptions import ignoreException

USECASE_FOLDER_NAME = 'usecases'


class TestPlan:
    def __init__(self, device_config: DeviceConfig, tag_regex: str):
        self.device_config = device_config
        self.tag_regex = tag_regex

    def execute(self):
        logging.getLogger().setLevel(logging.INFO)
        self.connect()
        Context.reporters().append(ReporterImpl())
        TestFlow(self.getCases()).run()
        self.disconnect()

    def connect(self):
        device, driver = self.device_config.connect()
        Context.setDriver(driver)
        Context.setDevice(device)

    def disconnect(self):
        ignoreException(lambda: Context.getDriver().get_web_driver().quit())
        Context.setDriver(None)
        Context.setDevice(None)

    @staticmethod
    def getCases() -> List[UseCase]:
        return list(map(lambda type: type(), TestPlan._getCaseClasses()))

    @staticmethod
    def _getCaseClasses() -> Iterator[type]:
        case_files = listdir(USECASE_FOLDER_NAME)
        case_file_names = map(lambda name: name.replace('.py', ''), case_files)
        classes = []
        for case_files in case_file_names:
            module = importlib.import_module('{}.{}'.format(USECASE_FOLDER_NAME, case_files))
            classes1 = inspect.getmembers(module, inspect.isclass)
            classes.extend(map(lambda name_and_type: name_and_type[1], classes1))
        return filter(TestPlan._isCase, classes)

    @staticmethod
    def _isCase(clazz: type) -> bool:
        return clazz is not UseCase and isinstance(clazz(), UseCase)


if __name__ == '__main__':
    cases = TestPlan.getCases()
    print(cases)
