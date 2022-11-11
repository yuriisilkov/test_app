import unittest
from libs.my_logs import MyLogs
from libs.my_ui import MyBrowserUI
from libs.my_api import MyAPI


logger = MyLogs().initial_logs(name="My_logs")


class GlobalInitClass(unittest.TestCase):

    @classmethod
    def setupClass(cls):
        cls.ui = MyBrowserUI()
        cls.ui.open_browser(url="https://www.saucedemo.com/")

    @classmethod
    def tearDownClass(cls):
        if cls.ui:
            cls.ui.driver.quit()

    def setUp(self):
        logger.info("--------------------------------------------------------------------------------------------")
        logger.info(f"START TEST: {self._testMethodName}")

    def tearDown(self):
        error = self._outcome.errors
        skip = self._outcome.skipped
        if skip:
            logger.warning(f"SKIPPED: {self._testMethodName}")
        else:
            getattr(logger, 'error' if error else 'info')(f"TEST {'FAILED' if error else 'PASSED'}: {self._testMethodName}")


class GlobalApiInitClass(unittest.TestCase):

    @classmethod
    def setupClass(cls):
        cls.api = MyAPI()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        logger.info("--------------------------------------------------------------------------------------------")
        logger.info(f"START TEST: {self._testMethodName}")

    def tearDown(self):
        error = self._outcome.errors
        skip = self._outcome.skipped
        if skip:
            logger.warning(f"SKIPPED: {self._testMethodName}")
        else:
            getattr(logger, 'error' if error else 'info')(f"TEST {'FAILED' if error else 'PASSED'}: {self._testMethodName}")
