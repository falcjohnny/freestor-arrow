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

class TimemarkClientJSON(BaseAdminClientJSON):
    """
    Base client class to send CRUD timemark requests to a web UI
    """
    def __init__(self, AdminClient_driver):
        #VdevClient_driver = self.vdev_client.driver in BaseVdevClientJSON
        self.driver = AdminClient_driver

    def create_timemark(self, vname=None, **kwargs):
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        #Create Timemark Resource
        driver.find_element_by_xpath(".//*[contains(text(), '" + vname + "')]").click()
        driver.find_element_by_xpath("//button[contains(@data-template-url,'views/manage/snapshot-menu.tpl.html')]").click()
        driver.find_element_by_xpath("//span[contains(.,'Create TimeMark/CDP Policy')]").click()
	time.sleep(2)
        driver.find_element_by_xpath("//button[@ng-model='snapPolicy.schedule']").click()
	#driver.find_element_by_xpath("(//input[@type='text'])[3]").clear()
        #driver.find_element_by_xpath("(//input[@type='text'])[3]").send_keys("00:00")
        #driver.find_element_by_xpath("(//button[@type='button'])[18]").click()
        driver.find_element_by_name("snapFreq").clear()
        driver.find_element_by_name("snapFreq").send_keys("2")
        driver.find_element_by_xpath("//button[@ng-model='snapPolicy.notifctn']").click()
        driver.find_element_by_name("snapNotifyDur").clear()
        driver.find_element_by_name("snapNotifyDur").send_keys("12")
        driver.find_element_by_name("maxShots").clear()
        driver.find_element_by_name("maxShots").send_keys("1000")
        if kwargs['automatic']['enabled'] is False:
            driver.find_element_by_xpath("//button[@type='submit']").click()
        self.wait_for_return_message("The TimeMark policy has been created.")
    
    def delete_timemark(self, vdev_name):
        """Deletes the Specified Timemark resource by vdev name only."""
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        time.sleep(2)
        #Find the element with text is vdev name. This method is very useful.
        driver.find_element_by_xpath(".//*[contains(text(), '" + vdev_name + "')]").click()
        driver.find_element_by_xpath("//button[@data-template-url='views/manage/timemark-menu.tpl.html']").click()
        for i in range(60):
            try:
                if driver.find_element_by_xpath("//a[contains(.,'Virtual Device Timemark ')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: assert False, "Time Out, the message didn't show up."
	driver.find_element_by_xpath("//a[contains(.,'Virtual Device Timemark ')]").click()
	driver.find_element_by_xpath("//a[contains(.,'Delete Timemark')]").click()
        driver.find_element_by_xpath("//button[contains(.,'Delete')]").click()
        self.wait_for_return_message("The timemark for virtual has been deleted.")

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

