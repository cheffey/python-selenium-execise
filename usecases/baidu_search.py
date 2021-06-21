from typing import List

from framework.base.base_case import UseCase
from framework.executable import Executable
from pageobject.baidu_pages import BaiduHomePage


class BaiduSearch(UseCase):
    def executables(self) -> List[Executable]:
        return self.executablesOf(
            self.open("https://baidu.com"),
            BaiduHomePage().search('python'),
            self.withIdElement("non-exist").clickAction(),
            self.assertTitle("python_百度搜索"),
        )
