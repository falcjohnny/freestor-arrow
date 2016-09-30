# Author                                : Johnny Wu
# Created                               : 2016/05/09
# Last Modified                         : 
# Version                               : 1.0

import json
import time

from oslo_log import log as logging
from six.moves.urllib import parse as urllib
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from arrow.common import selenium_client

LOG = logging.getLogger(__name__)

class BaseAdminClientJSON(selenium_client.SeleniumClient):
    """
    Base client class to send CRUD vdev requests to a web UI
    """
    def __init__(self, selenium_provider, credential_provider, fss_provider):
        selenium_client.SeleniumClient.__init__(self,selenium_provider,credential_provider)
        #todo: Need to move add_server function to other place,but no in init
    
    def login_server(self, size=None, vname=None):
        #login FMS web GUI
        self.driver.get(self.base_url + "/#/login")
        for i in range(60):
            try:
                if self.driver.find_element_by_xpath("//span[contains(.,'Log in to your account')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        self.driver.find_element_by_xpath("//input[@type='text']").clear()
        self.driver.find_element_by_xpath("//input[@type='text']").send_keys(self.credential_provider[1])
        self.driver.find_element_by_xpath("//input[@type='password']").clear()
        self.driver.find_element_by_xpath("//input[@type='password']").send_keys(self.credential_provider[2])
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
    
    def add_server(self, server_ip=None, server_user=None, server_passwd=None):
        #Add server (Todo: FDR server?)
        self.driver.find_element_by_xpath("//li[5]/a/span").click()
        self.driver.find_element_by_link_text("Servers").click()
        for i in range(60):
            try:
                if self.driver.find_element_by_xpath("//button[@type='button']").is_displayed(): break
            except: pass
            time.sleep(1)
        self.driver.find_element_by_xpath("//button[@type='button']").click()
        self.driver.find_element_by_name("ipAddress").clear()
        self.driver.find_element_by_name("ipAddress").send_keys(server_ip)
        self.driver.find_element_by_name("userName").clear()
        self.driver.find_element_by_name("userName").send_keys(server_user)
        self.driver.find_element_by_name("passwd").clear()
        self.driver.find_element_by_name("passwd").send_keys(server_passwd)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        self.wait_for_return_message("The server has been added.")
  
    def remove_server(self, fss_server=None):
        #Remove server
        driver = self.driver
        time.sleep(2)
        #You need to click Dashboard first, then you can click Administration without problem.
        driver.find_element_by_xpath("//span[contains(.,'Dashboard')]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//span[contains(.,'Administration')]").click()
        driver.find_element_by_link_text("Servers").click()
        driver.find_element_by_xpath(".//*[contains(text(), '"+ fss_server +"')]").click()
        driver.find_element_by_xpath("//button[@ng-click='deleteServer()']").click()
        driver.find_element_by_xpath("//input[@ng-model='deleteItem.force']").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.wait_for_return_message("The server has been deleted.")

    def create_customer(self, customer_name, domain, admin_pass, retype_pass):
        self.driver.find_element_by_xpath("//li[5]/a/span").click()
        self.driver.find_element_by_link_text("Customers").click()
        #Create customer
        self.driver.find_element_by_xpath("//button[@ng-click='showAddCustomerDialog()']").click()
        self.driver.find_element_by_xpath("(//input[@type='text'])[2]").clear()
        self.driver.find_element_by_xpath("(//input[@type='text'])[2]").send_keys(customer_name)
        self.driver.find_element_by_xpath("(//input[@type='text'])[3]").clear()
        self.driver.find_element_by_xpath("(//input[@type='text'])[3]").send_keys(domain)
        self.driver.find_element_by_xpath("//input[@name='password']").clear()
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(admin_pass)
        self.driver.find_element_by_xpath("//input[@name='retypePassword']").clear()
        self.driver.find_element_by_xpath("//input[@name='retypePassword']").send_keys(retype_pass)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        for i in range(60):
            try:
                if self.driver.find_element_by_xpath("//strong[contains(.,'The customer has been added.')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")

    def delete_customer(self, customer_name):
        self.driver.find_element_by_xpath("//li[5]/a/span").click()
        self.driver.find_element_by_link_text("Customers").click()
        self.driver.find_element_by_xpath(".//*[contains(text(), '"+ customer_name +"')]").click()
        self.driver.find_element_by_xpath("//button[@ng-click='deleteCustomer(customerGrid.selectedRows[0])']").click()
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        self.wait_for_return_message("The customer has been deleted.")

    def wait_for_return_message(self, message):
        for i in range(5):
            try:
                if self.driver.find_element_by_xpath("//strong[contains(.,'"+ message +"')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: assert False, "Time Out, the message didn't show up." 
        #Cannot use self.fail("time out"), because 

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

