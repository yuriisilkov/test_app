import logging
from libs.my_decorators import description
from libs.my_driver import WebDriver
from libs.my_ui_repository import LoginPage, MainPage
from libs.my_json_utils import MyJsonUtils


logger = logging.getLogger("My_logs")


class MyBrowserUI:
    def __init__(self):
        self.driver = WebDriver()
        self.xpath = self.driver.by.XPATH
        self.logged_in = False

    @description("Function name: 'Open browser'")
    def open_browser(self, url):
        if not self.driver.invoke_browser():
            logger.error("Unable to invoke browser")
            return False
        if not self.driver.go_to_url(url):
            logger.error(f"Unable to proceed to URL: {url}")
            return False
        return True

    @description("Function name: 'Verify login page is present'")
    def verify_login_page_is_present(self):
        if not self.driver.find(self.xpath, LoginPage.logo):
            logger.error("Unable to find logo")
            return False
        return True

    @description("Function name: 'Login'")
    def login(self, username, password, negative=False):
        logger.info(f"Set user credentials...")
        if not self.driver.send_text(self.xpath, LoginPage.username_input, username):
            logger.error("Unable to set value into username input")
            return False
        if not self.driver.send_text(self.xpath, LoginPage.password_input, password):
            logger.error("Unable to set value into password input")
            return False
        if not self.driver.click(self.xpath, LoginPage.login_button):
            logger.error("Unable to click on the Login button")
            return False
        if negative:
            if not self.driver.find(self.xpath, LoginPage.error_hint):
                logger.error("Unable to find error message with incorrect login")
                return False
            logger.info("User failed while login as expected")
            return True
        if not self.driver.not_exists(self.xpath, LoginPage.error_hint):
            logger.error("User failed while login")
            return False
        logger.info(f"Username/Password was set")
        if not self.logged_in_verification():
            return False
        return True

    @description("Function name: 'Logged in verification'")
    def logged_in_verification(self):
        logger.info(f"Verify that we are on the main page...")
        if not self.driver.find(self.xpath, MainPage.logo):
            logger.error("Unable to find main logo into the maine page")
            return False
        self.logged_in = True
        return True

    @description("Function name: 'Content verification'")
    def content_verification(self):
        if not self.logged_in:
            logger.warning("User already logged out")
            return 'test_skipped'
        logger.info(f"Verify content numbers on the main page...")
        actual_items_content = self.driver.driver.find_elements(self.xpath, MainPage.contents_of_items)
        if not actual_items_content:
            logger.error("Unable to get actual items content from UI")
            return False

        object_number = 1
        actual_content_data = {}
        for item in actual_items_content:
            title, description, price = item.text.split("\n")[0], item.text.split("\n")[1], item.text.split("\n")[2]
            actual_content_data.update({object_number: {'title': title, 'description': description, 'price': price}})
            object_number = object_number + 1

        db_content_storage = MyJsonUtils().content_data_store()
        if not actual_content_data == db_content_storage:
            logger.error(f"Expected items content: {db_content_storage}, not equal with actual: {actual_content_data}")
            return False
        logger.info(f"Expected items content equal with actual")
        return True

    @description("Function name: 'Logout'")
    def logout(self):
        if not self.logged_in:
            logger.warning("User already logged out")
            return 'test_skipped'
        if not self.driver.click(self.xpath, MainPage.menu_button):
            logger.error("Unable to click on the menu button")
            return False
        if not self.driver.click(self.xpath, MainPage.logout_button):
            logger.error("Unable to click on the Logout button")
            return False
        if not self.verify_login_page_is_present():
            logger.error("Unable to find Login page")
            return False
        logger.info("User successfully logged out")
        return True
