import logging
from typing import List

from constant import ITERCEPT_LOCAL_DEBUG_ON
from framework.context import Context
from framework.reporter.allure import Status
from framework.base.base_case import UseCase
from framework.executable import Action, Route, Executable
from util.itercept_debug_tool import InterceptDebugTool, ResponseOption


def reportersDo(reporter_action):
    for reporter in Context.reporters():
        reporter_action(reporter)


def execute(executable: Executable):
    if executable is None: return
    reportersDo(lambda reporter: reporter.stepHandler().startStep(executable))
    if isinstance(executable, Action):
        execute_action(executable)
    elif isinstance(executable, Route):
        try:
            for step in executable.getExecutables():
                execute(step)
        except BaseException as e:
            reportersDo(lambda reporter: reporter.stepHandler().endStep(executable, Status.FAILED))
            raise e
        else:
            reportersDo(lambda reporter: reporter.stepHandler().endStep(executable, Status.PASSED))


def execute_action(executable):
    while True:
        try:
            executable.run()
            break
        except BaseException as e:
            if ITERCEPT_LOCAL_DEBUG_ON:
                response = InterceptDebugTool().run(e)
                if response is ResponseOption.REDO:
                    continue
                elif response is ResponseOption.SKIP:
                    break
                elif response is ResponseOption.END:
                    pass
            reportersDo(lambda reporter: reporter.stepHandler().endStep(executable, Status.FAILED))
            raise e
    reportersDo(lambda reporter: reporter.stepHandler().endStep(executable, Status.PASSED))


class TestFlow:
    def __init__(self, cases: List[UseCase]):
        self.cases = cases

    def run(self):
        reportersDo(lambda reporter: reporter.beforeAll())
        for case in self.cases:
            try:
                for step in case.executables():
                    execute(step)
            except BaseException as e:
                reportersDo(lambda report: report.failCase(case, e))
            else:
                reportersDo(lambda report: report.passCase(case))
