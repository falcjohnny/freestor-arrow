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

class PdevClientJSON(BaseAdminClientJSON):
    """
    Base client class to send CRUD snapshot requests to a web UI
    """
    def __init__(self, AdminClient_driver):
        #VdevClient_driver => self.vdev_client.driver in BaseVdevClientJSON
        self.driver = AdminClient_driver

    def prepare_pdev(self, acsl=None, category=None):
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        driver.find_element_by_xpath("//a[contains(.,'Physical Resources')]").click()
        driver.find_element_by_xpath("//label[contains(.,'Physical Devices')]").click()
        #Select the physical device
        driver.find_element_by_xpath(".//*[contains(text(), '" + acsl + "')]").click()
        #Actual_Category = driver.find_element_by_xpath("//div[@class='ag-cell cell-col-3 ag-cell-value ag-cell-focus']").getText()
        #LOG.info('===The Actual_Category is "%s".===', Actual_Category)       
        driver.find_element_by_xpath("//button[@data-template-url='views/manage/select.tpl.html']").click()
        driver.find_element_by_xpath("//a[contains(.,'Prepare Physical Device')]").click()
        #Select the element 'category' and click the option "Virtual" or "Unassign"
        driver.find_element_by_xpath("//select[@name='category']/option[text()='" + category + "']").click()
        driver.find_element_by_xpath("//div[@class='modal-footer']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        for i in range(60):
            try:
                if driver.find_element_by_xpath("//strong[contains(.,'The devices have been updated.')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
 
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

