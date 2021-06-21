import time


def isValid(value) -> bool:
    if value is bool:
        return value
    else:
        return value is not None


class ConditionWait:
    def __init__(self, timeout_in_sec: int = 10):
        self.timeout_in_sec = timeout_in_sec

    def untilOrNot(self, supplier) -> bool:
        return isValid(self.until(supplier))

    def untilOrThrow(self, supplier, message: str = ''):
        value = self.until(supplier)
        if not isValid(value):
            raise TimeoutError(message)
        return value

    def until(self, supplier) -> object:
        timeout_instant = time.time() + self.timeout_in_sec
        while True:
            try:
                value = supplier()
                if isValid(value):
                    return value
            except BaseException:
                pass
            if time.time() > timeout_instant:
                return None
