from selenium.webdriver.chrome.options import Options as Options_chrom
from selenium.webdriver.firefox.options import Options as Options_firefox
import os


# Chrom Webdriver configuration
chrome_options = Options_chrom()

chrome_options.headless = os.environ.__contains__('CHROME_HEADLESS')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-impl-side-painting")
chrome_options.add_argument("--disable-accelerated-2d-canvas")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disk-cache-size=0")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--use-fake-ui-for-media-stream')
chrome_options.add_argument('--use-fake-device-for-media-stream')


# Firefox Webdriver configuration
firefox_options = Options_firefox()

firefox_options.headless = os.environ.__contains__('CHROME_HEADLESS')
firefox_options.add_argument("--window-size=1920,1080")

