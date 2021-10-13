##Intro

This is a rewrite of another java test framework in python with selenium as practice. **NOT** all functions are implemented yet.
The framework use page object design to manager the code. And case is forced to be composed with **Actions, Route(Action combo)** which have description that could give a better report using allure(NOT implemented yet).

Also, this framework included the debug tool which is similar to **Cucumber Appium Debug Tool** https://github.com/cheffey/cadt

framework structure:
**framework-structure.png**

case sample:
**baidu_search.py**

page object sample:
**baidu_pages.py**

##Get started
1. Check local chrome version
2. Download matching driver in https://chromedriver.chromium.org/downloads
3. Modify constant CHROME_WEB_DRIVER_PATH in constant.py
4. Start the test in entrance: executor.py
5. Wait the case to be failed which will trigger the debug tool in python console