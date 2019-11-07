
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ChromeHeadlessDriver(webdriver.Chrome):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1920x1080')
        super().__init__(options=chrome_options)
