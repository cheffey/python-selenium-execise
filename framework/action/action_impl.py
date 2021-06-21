from framework.context import Context
from framework.executable import Action
from framework.logistic.condition import Condition


class ClickAction(Action):
    def stepName(self) -> str:
        return 'click {}'.format(self.ele.desc())

    def __init__(self, ele):
        self.ele = ele

    def run(self):
        Context.getDriver().click(self.ele)


class SendAction(Action):
    def stepName(self) -> str:
        return 'send {} with text: {}'.format(self.ele.desc(), self.text)

    def __init__(self, ele, text: str):
        self.text = text
        self.ele = ele

    def run(self):
        Context.getDriver().send(self.ele, self.text)


class OpenAction(Action):
    def stepName(self) -> str:
        return 'open {}'.format(self.url)

    def __init__(self, url: str):
        self.url = url

    def run(self):
        Context.getDriver().open(self.url)


class AssertAction(Action):
    def stepName(self) -> str:
        return 'assert {}'.format(self.condition.desc())

    def __init__(self, condition: Condition):
        self.condition = condition

    def run(self):
        assert self.condition.verify()
