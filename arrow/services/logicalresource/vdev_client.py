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

class BaseVdevClientJSON(BaseAdminClientJSON):
    """
    Base client class to send CRUD vdev requests to a web UI
    """
    def __init__(self, AdminClient_driver,default_vdev_size=1):
        #AdminClient_driver => self.admin_client.driver in BaseAdminClientJSON
        self.driver = AdminClient_driver
        self.default_vdev_size = default_vdev_size
    
    def create_vdev(self, size=None, **kwargs):
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        # Create a Virtual Device
        # todo : 'vdev_type' -> thin & SED type
        driver.find_element_by_xpath("//button[contains(@ng-click,'showCreateVirtualDeviceDialog(currentDevice)')]").click()
        for i in range(60):
            try:
                if driver.find_element_by_xpath("//h5[contains(.,'Create Virtual Device')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        driver.find_element_by_xpath("//input[@ng-model='createItem.name']").clear()
        driver.find_element_by_xpath("//input[@ng-model='createItem.name']").send_keys(kwargs['vdev_name'])
        #Select storage pool
        driver.find_element_by_xpath("//div[9]/div[2]/div/div/div/span").click()
        driver.find_element_by_xpath("//span[contains(.,'StoragePool-1')]").click()
        driver.find_element_by_xpath("(//input[@type='number'])[3]").clear()
        if size is None:
            size = self.default_vdev_size
        driver.find_element_by_xpath("(//input[@type='number'])[3]").send_keys(size) #"1"
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.wait_for_return_message("The virtual device has been created.")
    
    def update_vdev(self, vdev_name, new_vname, new_size):
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        time.sleep(1)
        #Find the element with text is vdev name. This method is very useful.
        driver.find_element_by_xpath(".//*[contains(text(), '" + vdev_name + "')]").click()       
        driver.find_element_by_xpath("//button[@ng-click='showEditVirtualDeviceDialog(currentDevice, gridResOptions.selectedRows[0])']").click()
        if new_vname is not None:
            driver.find_element_by_xpath("//input[@ng-model='formItem.name']").clear()
            driver.find_element_by_xpath("//input[@ng-model='formItem.name']").send_keys(new_vname)
        if new_size is not None:
            driver.find_element_by_xpath("//input[@type='number']").clear()
            driver.find_element_by_xpath("//input[@type='number']").send_keys(new_size)
        driver.find_element_by_xpath("//button[contains(.,'Update')]").click()
        self.wait_for_return_message("The virtual device has been updated.")        

    def delete_vdev(self, vdev_name, force=False):
        #todo: force deletion 
        """Deletes the Specified Virtual Device by vdev name only."""
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        time.sleep(2)
        #Find the element with text is vdev name. This method is very useful.
        driver.find_element_by_xpath(".//*[contains(text(), '" + vdev_name + "')]").click()
        driver.find_element_by_xpath("//button[contains(@data-template-url,'views/manage/delete-device.tpl.html')]").click()
        driver.find_element_by_xpath("//a[@ng-click='showDeleteVirtualDeviceDialog(currentDevice, gridResOptions.selectedRows[0])']").click()
        for i in range(60):
            try:
                if driver.find_element_by_xpath("//h5[contains(.,'Delete Virtual Device')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        if force is True:
            driver.find_element_by_xpath("//button[@ng-model='deleteItem.force']").click()
        driver.find_element_by_xpath("//button[contains(.,'Delete')]").click()
    
    def delete_all_vdevs(self, force=False): 
        """Clear All Virtual Devices ."""
        driver = self.driver
        time.sleep(2)
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//a[contains(.,'Virtual Devices')]").click()
        driver.find_element_by_xpath("//input[@ng-model='selectAll']").click()
        driver.find_element_by_xpath("//button[@data-template-url='views/manage/delete-device.tpl.html']").click()
        #Count the number of virtual devices
        row_count = len(driver.find_elements_by_xpath("//div[@id='center']/div/div[2]/div/div/div/div[2]"))
        row_count = row_count - 1 # The correct num# of vdevs
        #If there are more than one vdevs existed.
        if row_count > 1:
            driver.find_element_by_xpath("//a[contains(.,'Delete Virtual Devices')]").click()
            for i in range(60):
                try:
                    if driver.find_element_by_xpath("//h5[contains(.,'Delete Multiple Virtual Devices')]").is_displayed(): break
                except: pass
                time.sleep(1)
            else: self.fail("time out")
            if force is True:
                driver.find_element_by_xpath("//button[@ng-model='deleteMultiple.force']").click()
            driver.find_element_by_xpath("//button[contains(@ng-click,'deleteMultipleDevices(gridMultipleDevice,$hide)')]").click()
            time.sleep(1)
            driver.find_element_by_xpath("//button[contains(@ng-click,'yesDeleteMultipleDevices(gridMultipleDevice,$hide)')]").click()
            self.wait_for_return_message("Devices have been deleted.")
        #If there is only one vdev existed.
        elif row_count is 1:
            driver.find_element_by_xpath("//a[contains(.,'Delete')]").click()
            for i in range(60):
                try:
                    if driver.find_element_by_xpath("//h5[contains(.,'Delete Virtual Device')]").is_displayed(): break
                except: pass
                time.sleep(1)
            else: self.fail("time out")
            if force is True:
                driver.find_element_by_xpath("//button[@ng-model='deleteItem.force']").click()
            driver.find_element_by_xpath("//button[contains(.,'Delete')]").click()
            self.wait_for_return_message("The virtual device has been deleted.")
        else:
            pass

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

