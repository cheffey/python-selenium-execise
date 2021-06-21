from framework.base.base_page import BasePage
from framework.executable import Route


class BaiduHomePage(BasePage):
    def __init__(self):
        self.search_box = self.withIdElement('kw')
        self.search_btn = self.withIdElement('su')

    def search(self, keyword: str) -> Route:
        return self.routesOf(
            'search ' + keyword,
            self.search_box.sendAction(keyword),
            self.search_btn.clickAction()
        )
