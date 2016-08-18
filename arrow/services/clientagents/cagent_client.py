# Author                                : Johnny Wu
# Created                               : 2016/05/09
# Last Modified                         : 
# Version                               : 1.0

import json
import time

from oslo_log import log as logging
from six.moves.urllib import parse as urllib
from arrow.services.administration.admin_client import BaseAdminClientJSON
#from arrow.services.logicalresource.vdev_client import BaseVdevClientJSON
#from tempest import exceptions

LOG = logging.getLogger(__name__)

class CagentClientJSON(BaseAdminClientJSON):
    """
    Base client class to send CRUD snapshot requests to a web UI
    """
    def __init__(self, AdminClient_driver):
        #VdevClient_driver => self.vdev_client.driver in BaseVdevClientJSON
        self.driver = AdminClient_driver

    def protect_disk(self, client=None, disk=None, protocol=None):
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        driver.find_element_by_xpath("//a[contains(.,'Client Agents')]").click()
        driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
        #Select the Client
        driver.find_element_by_xpath(".//*[contains(text(), '" + client + "')]").click()
        #LOG.info('===The Actual_Category is "%s".===', Actual_Category)      
        #Create protection 
        driver.find_element_by_xpath("//button[contains(@ng-click,'createProtection(gridOptions.selectedRows[0], false)')]").click()
        #Select disk
        driver.find_element_by_xpath("//fieldset/div/div/div/div/span/span").click()
        driver.find_element_by_xpath("//span[contains(.,'" + disk + "')]").click()
        #driver.find_element_by_xpath(".//*[contains(text(), '" + server + "')]").click()       
        #Select Protocol
        driver.find_element_by_xpath("//span[@class='ui-select-placeholder text-muted ng-binding']").click()
        driver.find_element_by_xpath("//span[contains(.,'" + protocol + "')]").click()
#        driver.find_element_by_xpath("//a[contains(.,'" + protocol + "')]").click()
        #driver.find_element_by_xpath("//select[@name='category']/option[text()='" + disk + "']").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.wait_for_return_message("The protection policy has been created.")
        for i in range(30):
            try:
                driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
                time.sleep(1)
                driver.find_element_by_xpath(".//*[contains(text(), '" + client + "')]").click()
                time.sleep(1)
                if driver.find_element_by_xpath("//span[contains(.,'Online')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")

    def update_protection(self, client=None, disk=None, **kwargs):
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        driver.find_element_by_xpath("//a[contains(.,'Client Agents')]").click()
        driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
        driver.find_element_by_xpath(".//*[contains(text(), '" + client + "')]").click()
        #LOG.info('===The Actual_Category is "%s".===', Actual_Category)       
        #Select disk
        driver.find_element_by_xpath(".//*[contains(text(), '" + disk + "')]").click()
        #Update policy
        driver.find_element_by_xpath("//button[contains(@ng-click,'updateProtection(gridOptions.selectedRows[0], gridProtectedOptions.selectedRows, true)')]").click()
        stype = None 
        if kwargs['schedule_type'] == 'Days':
            stype = 'day'
        elif kwargs['schedule_type'] == 'Hour':
            stype = 'typeHo'
        else:
            stype = 'typeMn' 
        driver.find_element_by_xpath("//input[@ng-model='protectionForm." + stype + "']").clear()
        driver.find_element_by_xpath("//input[@ng-model='protectionForm." + stype + "']").send_keys(kwargs['interval_num'])
        driver.find_element_by_xpath("//select[@ng-model='protectionForm.type']").click()
        driver.find_element_by_xpath("//option[@label='" + kwargs['schedule_type'] + "']")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        for i in range(60):
            try:
                if driver.find_element_by_xpath("//strong[contains(.,'The protection policy has been created.')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
 
    def remove_protected_disk(self, client=None, disk=None):
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        driver.find_element_by_xpath("//a[contains(.,'Client Agents')]").click()
        driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
        time.sleep(1)
        #Select the Client
        driver.find_element_by_xpath(".//*[contains(text(), '" + client + "')]").click()
        #LOG.info('===The Actual_Category is "%s".===', Actual_Category)       
        #Select disk
        driver.find_element_by_xpath(".//*[contains(text(), '" + disk + "')]").click()
        #Remove protection
        driver.find_element_by_xpath("(//button[@type='button'])[10]").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.wait_for_return_message("The protection policy has been deleted.")
   
    def wait_for_return_message(self, message):
        for i in range(5):
            try:
                if self.driver.find_element_by_xpath("//strong[contains(.,'"+ message +"')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: assert False, "Time Out, the expected message didn't show up."

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
