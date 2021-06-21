
from framework.device.device import Chrome
from framework.test_plan import TestPlan


# class Executor:
#     def execute(self):
if __name__ == '__main__':
    TestPlan(Chrome(), "@all").execute()

