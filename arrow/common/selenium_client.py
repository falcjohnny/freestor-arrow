# Author                                : Johnny Wu
# Created                               : 2016/05/09
# Last Modified                         : 
# Version                               : 1.0

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

class SeleniumClient:

    def __init__(self,selenium_provider=None,credential_provider=None):
        #selenium_provider[0] is saved with hub_ip;selenium_provider[1] is broswer
        self.driver = webdriver.Remote(command_executor='http://'+selenium_provider[0]+':4444/wd/hub',desired_capabilities=getattr(DesiredCapabilities,selenium_provider[1])) 
        #This is for remote webdriver use
        self.driver.implicitly_wait(30)
        self.base_url = "http://"+credential_provider[0]+"/"
        self.driver.maximize_window()
        self.verificationErrors = []
        self.accept_next_alert = True
        self.credential_provider = credential_provider
        self.wait = WebDriverWait(self.driver, 5)

