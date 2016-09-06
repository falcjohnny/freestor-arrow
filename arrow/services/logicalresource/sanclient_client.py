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
from arrow.services.administration.admin_client import BaseAdminClientJSON

LOG = logging.getLogger(__name__)

class SANClientClientJSON(BaseAdminClientJSON):
    """
    Base client class to send CRUD sanclient requests to a web UI
    """
    def __init__(self, AdminClient_driver):
        #AdminClient_driver => self.admin_client.driver in BaseAdminClientJSON
        self.driver = AdminClient_driver
        #self.default_sanclient_size = default_sanclient_size
    
    def unassign_all_from_sanclient(self, sanclient_name):
        """Unassign the Specified Virtual Device from sanclient name."""
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        time.sleep(2)
        #Clients tab
        driver.find_element_by_xpath("//a[contains(.,'Clients')]").click()
        #Find the element with text is sanclient name. This method is very useful.
        driver.find_element_by_xpath(".//*[contains(text(), '" + sanclient_name + "')]").click()
        driver.find_element_by_xpath("//button[@ng-click='showUnassignDialog(currentDevice, gridResOptions.selectedRows[0])']").click()
        driver.find_element_by_xpath("//input[@ng-model='selectAllChecked']").click()
        driver.find_element_by_xpath("//button[contains(.,'Unassign')]").click()
        self.wait_for_return_message("The device has been unassigned from the client.")

    def wait_for_return_message(self, message):
        for i in range(5):
            try:
                if self.driver.find_element_by_xpath("//strong[contains(.,'"+ message +"')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: assert False, "Time Out, the expected message didn't show up." 
        #Cannot use self.fail("time out"), because self didn't inhert unittest

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

