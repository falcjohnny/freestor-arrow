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

class HotzoneClientJSON(BaseAdminClientJSON):
    """
    Base client class to send CRUD hotzone requests to a web UI
    """
    def __init__(self, AdminClient_driver):
        #VdevClient_driver = self.vdev_client.driver in BaseVdevClientJSON
        self.driver = AdminClient_driver

    def create_hotzone(self, vname=None):
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        #Create Hotzone Resource
        driver.find_element_by_xpath(".//*[contains(text(), '" + vname + "')]").click()
        driver.find_element_by_xpath("//button[contains(@data-template-url,'views/manage/hotzone-menu.tpl.html')]").click()
        time.sleep(2)
        #driver.find_element_by_xpath("//a[contains(.,'Create HotZone')]").click()
        driver.find_element_by_link_text("Create HotZone").click()
        for i in range(60):
            try:
                if driver.find_element_by_xpath("//h5[contains(.,'Create HotZone')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: assert False, "Time Out, the message didn't show up."
	time.sleep(1)
        driver.find_element_by_xpath("//input[@ng-model='sizeInput.value']").clear()
        driver.find_element_by_xpath("//input[@ng-model='sizeInput.value']").send_keys("1024")
	driver.find_element_by_xpath("//span[@ng-show='$select.isEmpty()']").click()
        driver.find_element_by_xpath("//span[contains(.,'StoragePool-1')]").click()
	driver.find_element_by_xpath("//button[@type='submit']").click()
        self.wait_for_return_message("The HotZone has been created.")
    
    def delete_hotzone(self, vdev_name):
        """Deletes the Specified Hotzone resource by vdev name only."""
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        time.sleep(2)
        #Find the element with text is vdev name. This method is very useful.
        driver.find_element_by_xpath(".//*[contains(text(), '" + vdev_name + "')]").click()
        driver.find_element_by_xpath("//button[contains(@data-template-url,'views/manage/hotzone-menu.tpl.html')]").click()
	for i in range(60):
            try:
                if driver.find_element_by_xpath("//a[contains(.,'Delete HotZone')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: assert False, "Time Out, the message didn't show up."
	driver.find_element_by_xpath("//a[contains(.,'Delete HotZone')]").click()
        driver.find_element_by_xpath("//button[contains(.,'Delete')]").click()
        self.wait_for_return_message("The HotZone has been deleted.")

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

