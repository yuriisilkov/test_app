import os
import threading
from datetime import datetime
from selenium.webdriver.support.wait import WebDriverWait
from libs.my_browser_options import chrome_options, firefox_options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException, \
    NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from pathlib import Path


logger = logging.getLogger("My_logs")


class WebDriver():

    def __init__(self):
        self.browser = os.environ.get("ENV_BROWSER_TYPE", "Chrome")
        self.driver = None
        self.by = By()
        self.time_to_wait = 60
        self.invoked = False

        self.chromedriver_path = os.path.dirname(os.path.realpath(__file__)).replace("libs", "chromedriver")

    def invoke_browser(self):
        logger.info("Invoke browser %s" % self.browser)
        try:
            if self.browser == "Chrome":
                self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=self.chromedriver_path)
            if self.browser == "Firefox":
                self.driver = webdriver.Firefox(options=firefox_options)
            self.driver.set_page_load_timeout(time_to_wait=self.time_to_wait)
        except Exception as e:
            logger.error("Invoke Browser False cause: '%s'" % e)
            return False
        logger.info("Browser successfully opened")
        self.invoked = True
        return True

    def go_to_url(self, url):
        try:
            logger.info("Trying to get URL: %s" % url)
            self.driver.get(url)
            return True
        except Exception as e:
            logger.error(f"Requested URL: {url}, exception: {e}")
            return False

    def quit(self):
        logger.info("Trying to close %s" % self.browser)
        try:
            self.driver.quit()
        finally:
            logger.info("Done closing %s" % self.browser)

    def find(self, kind, locator, timeout=20, skip_log=False, displayed=True):
        ec_method = EC.element_to_be_clickable if displayed else EC.presence_of_element_located
        try:
            return WebDriverWait(self.driver, timeout, ignored_exceptions=(StaleElementReferenceException,)).\
                until(ec_method((kind, locator)))
        except KeyError:
            logging.debug("find: unexpected kind of locator {}".format(kind))
            return None
        except TimeoutException:
            if not skip_log:
                logging.debug("find: Unable to find element (kind={}, locator={})".format(kind, locator))
            return None
        except WebDriverException as exc:
            if not skip_log:
                logging.debug("find: {}".format(exc.msg))
            return None
        except Exception as exc:
            if not skip_log:
                logging.debug("find: {}".format(str(exc)))
            return None

    def click(self, kind, locator, timeout=20, skip_log=False):
        end_time = time.time() + timeout
        exc_message = ''
        while time.time() < end_time:
            remaining_time = int(end_time - time.time())
            element = self.find(kind, locator, remaining_time, skip_log)
            if not element:
                exc_message += '\nElement was not found on page. Kind: %s, locator: %s' % (kind, locator)
                continue
            try:
                element.click()
                return True
            except WebDriverException as exc:
                exc_message += ('\n' + exc.msg)
                continue
        if not skip_log:
            logging.debug("click: unable to click on element (kind={}, locator={}). All exceptions: {}.".
                         format(kind, locator, exc_message))
        return False

    def send_text(self, kind, locator, text_to_send, timeout=20, do_clear=True, skip_log=False):
        end_time = time.time() + timeout
        exc_message = ''
        while time.time() < end_time:
            remaining_time = int(end_time - time.time())
            element = self.find(kind, locator, remaining_time)
            if not element:
                exc_message += '\nElement was not found on page. Kind: %s, locator: %s' % (kind, locator)
                continue
            try:
                if do_clear:
                    element.clear()
                    element.send_keys(text_to_send)
                    # Ignore non ascii symbols
                    if text_to_send.encode("ascii", errors="ignore").decode() \
                            == self.driver.execute_script('return arguments[0].value', element):
                        return True
                else:
                    element.send_keys(text_to_send)
                    return True
            except WebDriverException as exc:
                exc_message += ('\n' + exc.msg)

        if not skip_log:
            logging.debug("send_text: unable to send text {} into element (kind={}, locator={}). All exceptions: {}"
                         .format(text_to_send.encode("ascii", errors="ignore").decode(), kind, locator, exc_message))
        return False

    def refresh_page(self, timeout=30, action_on_alert='accept'):
        """
        :param action_on_alert: 'accept' or 'dismiss'
        :param timeout: maximum time to wait until page is refreshed
        """

        def refreshing():
            self.driver.refresh()
            time.sleep(2)
            # Here we need timeout a little bit more than argument 'timeout' is - in order to keep subprocess alive
            # in case page has not been refreshed. 'Alive' status of subprocess indicates that page was not refreshed.
            end_time = time.time() + timeout * 2
            while end_time > time.time():
                alert = EC.alert_is_present()(self)
                if alert:
                    getattr(alert, action_on_alert)()
                    logging.debug('Alert message appeared during refreshing. %sed.', action_on_alert.capitalize())
                if self.driver.execute_script('return document.readyState') == 'complete':
                    return

        subprocess = threading.Thread(target=refreshing)
        subprocess.setDaemon(True)
        subprocess.start()
        subprocess.join(timeout=timeout)
        if subprocess.is_alive():
            logging.error('refresh_page: The page is still refreshing but timeout (%s seconds) is over.', timeout)
            return False
        logging.debug('refresh_page: The page has been refreshed.')
        return True

    def hover(self, kind, locator, timeout=20):
        element = self.find(kind, locator, timeout)
        if not element:
            logging.error('Element with locator %s was not found on page' % locator)
            return False
        try:
            hov = ActionChains(self.driver).move_to_element(element)
            hov.perform()
        except WebDriverException as exc:
            logging.error('Failed to hover over web element with exception: %s' % exc)
            return False
        return True

    def exists(self, kind, locator, timeout=20, skip_log=False, check_count=5, only_enables=False):
        ec_method = EC.presence_of_element_located if only_enables else EC.element_to_be_clickable

        try:
            WebDriverWait(self.driver, timeout, ignored_exceptions=(StaleElementReferenceException,))\
                .until(ec_method((kind, locator)))
            return True
        except KeyError:
            logging.debug("exists: unexpected type {}".format(kind))
            return False
        except TimeoutException:
            if not skip_log:
                logging.debug("exists: element doesn't exist (kind={}, locator={})".format(kind, locator))
            return False
        except WebDriverException as exc:
            if not skip_log:
                logging.debug("exists: {}".format(exc.msg))
            return False

    def not_exists(self, kind, locator, timeout=20, skip_log=False):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.staleness_of(self.driver.find_element(kind, locator)))
        except KeyError:
            logging.debug("not_exists: unexpected type {}".format(kind))
            return False
        except NoSuchElementException:
            return True
        except TimeoutException:
            if not skip_log:
                logging.debug("not_exists: element still exists (kind={}, locator={})".format(kind, locator))
            return False
        except WebDriverException as exc:
            if not skip_log:
                logging.debug("not_exists: {}".format(exc.msg))
            return False

    def save_screen(self):
        try:
            test_name = globals.config.test_name
            root_dir = os.path.abspath(os.curdir)
            screen_path = Path(os.environ.get("LOG_FOLDER", f"{root_dir}/logs"))
            screen_path.mkdir(parents=True, exist_ok=True)
            screenshot_name = f"{test_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
            self.driver.save_screenshot(f'{screen_path}/{screenshot_name}')
            logging.debug(f"Screenshot {screenshot_name} was saved.")
        except Exception as exc:
            logging.error("Impossible to save Screenshot: {} (type={})".format(str(exc), type(exc)))
