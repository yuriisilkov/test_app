from tests import GlobalInitClass


class MyTests(GlobalInitClass):

    def test_01_verify_that_we_are_on_login_page(self):
        self.ui.verify_login_page_is_present()

    def test_02_verify_login_with_empty_credentials(self):
        self.ui.login(username="", password="", negative=True)

    def test_03_verify_login_with_incorrect_credentials(self):
        self.ui.login(username="Test", password="Test", negative=True)

    def test_04_verify_login_with_correct_credentials(self):
        self.ui.login(username="standard_user", password="secret_sauce")

    def test_05_verify_content(self):
        self.ui.content_verification()

    def test_06_verify_logout(self):
        self.ui.logout()

