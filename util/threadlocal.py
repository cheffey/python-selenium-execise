import threading


class ThreadLocal:

    def __init__(self, supplier):
        self.__supplier = supplier
        self.__values = {}

    @classmethod
    def withInitial(cls, supplier):
        return ThreadLocal(supplier)

    def get(self):
        current_thread = threading.currentThread()
        if current_thread not in self.__values:
            initiate_value = self.__supplier()
            self.__values.update({current_thread: initiate_value})
        return self.__values[current_thread]

    def set(self, value):
        current_thread = threading.currentThread()
        self.__values.update({current_thread: value})


if __name__ == '__main__':
    tl = ThreadLocal.withInitial(lambda: 4)
    value = tl.get()
    print(value)
    tl.set("xx")
    value = tl.get()
    print(value)
