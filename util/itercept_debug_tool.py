import logging
import os
import re
import uuid
from collections import Iterator
from enum import Enum
from typing import List

from framework.context import Context
from framework.exceptions import NotFoundException


class ResponseOption(Enum):
    SKIP = 'SKIP'
    REDO = 'REDO'
    END = 'END'


def cut_args(line: str) -> tuple[str, List[str]]:
    args = list(cut_args0(line))
    size = len(args)
    if size == 0:
        return None, []
    return args[0], args[1:]


def cut_args0(line: str) -> Iterator[str]:
    matcher = re.match('([^{}]*){([^}]*)}(.*)', line)
    is_not_empty = lambda x: x != ''
    if matcher:
        result = []
        result.extend(cut_args0(matcher.group(1)))
        result.append(matcher.group(2).strip())
        result.extend(cut_args0(matcher.group(3)))
        return filter(is_not_empty, result)
    else:
        return filter(is_not_empty, line.split(' '))


class WithUselessTraceException(BaseException):
    def __init__(self, message: str = ''):
        self.message = message


def executeMatchCommand(method, params: List[str]):
    try:
        required_args_count = method.__code__.co_argcount - 1
        give_args_count = len(params)
        message = "require {} arguments when {} was given".format(required_args_count, give_args_count)
        if required_args_count > give_args_count:
            raise WithUselessTraceException(message)
        elif required_args_count < give_args_count:
            logging.warning(message)
            method(*tuple(params[0:required_args_count]))
        else:
            method(*tuple(params))
    except BaseException as e:
        logging.exception(e)


class CacheElement:
    def __init__(self, id: str, text: str):
        self.id = id
        self.text = text


class ConsoleColor(Enum):
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    GREY = 37
    BLACK = 38


def color(text: str, color: ConsoleColor) -> str:
    return '\u001b[{};4m{}\u001b[0m'.format(color.value, text)


class InterceptDebugTool:
    def __init__(self):
        self.cache_elements = []
        self.response = None
        try:
            self.driver = Context.getDriver()
            self.device = Context.getDevice()
        except NotFoundException:
            pass

    def run(self, e: BaseException = None) -> ResponseOption:
        if e is None:
            logging.exception(e)
        print('Intercept by {}'.format(e))
        while True:
            commands = input()
            keyword, params = cut_args(commands)
            if keyword is None:
                continue
            print('match command: {} {}'.format(keyword, params))
            if not hasattr(self, keyword):
                self.help()
                print("Unable to find command: {}".format(keyword))
                continue
            method = getattr(self, keyword)
            try:
                executeMatchCommand(method, params)
            except WithUselessTraceException as e:
                print(e.message)
            except BaseException as e:
                logging.exception(e)
            if self.response is not None:
                return self.response

    def ss(self):
        self.screenshot()

    def screenshot(self):
        random_name = uuid.uuid4().__str__()[0: 8] + '.png'
        self.driver.get_web_driver().get_screenshot_as_file(random_name)
        print('screenshot created: {}'.format(random_name))
        os.system('open {}'.format(random_name))

    def ls(self):
        web_elements = self.driver.get_web_driver().find_elements('xpath', "//*[@id or @text]")
        to_cache_element = lambda ele: CacheElement(ele.get_attribute('id'), ele.get_attribute('text'))
        self.cache_elements = map(to_cache_element, web_elements)
        self.cache()

    def cache(self):
        for idx, ele in enumerate(self.cache_elements):
            idx_ = 'idx: {}'.format(idx)
            id_ = color('id: {}'.format(ele.id), ConsoleColor.BLUE)
            text_ = color('text: {}'.format(ele.text), ConsoleColor.PURPLE)
            print('%s %s %s' % (idx_, id_, text_))

    def redo(self):
        self.response = ResponseOption.REDO

    def end(self):
        self.response = ResponseOption.END

    def skip(self):
        self.response = ResponseOption.SKIP

    def help(self):
        print(color("Commands are listed in intercept_debug_tool as method names:", ConsoleColor.BLUE))
        print("{}\t\tredo the last failed step".format(color("redo", ConsoleColor.GREEN)))
        print("{}\t\tskip the last failed step".format(color("skip", ConsoleColor.GREEN)))
        print("{}\t\tend the test by rethrow the caught exception".format(color("end", ConsoleColor.GREEN)))
        print("{}\t\tprint all element with ID or with Text in current page".format(color("ls, list", ConsoleColor.GREEN)))
        print("{}\t\ttake a screenshot of current page, and open it".format(color("ss, screenshot", ConsoleColor.GREEN)))
        print("{}\t\tprint all elements in previous searches".format(color("cache", ConsoleColor.GREEN)))
        pass
