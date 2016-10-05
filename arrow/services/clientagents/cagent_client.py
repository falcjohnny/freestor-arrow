# Author                                : Johnny Wu
# Created                               : 2016/05/09
# Last Modified                         : 
# Version                               : 1.0

import json
import time, re

from oslo_log import log as logging
from six.moves.urllib import parse as urllib
from arrow.services.administration.admin_client import BaseAdminClientJSON
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
#from arrow.services.logicalresource.vdev_client import BaseVdevClientJSON
#from tempest import exceptions

LOG = logging.getLogger(__name__)

class CagentClientJSON(BaseAdminClientJSON):
    """
    Base client class to send CRUD snapshot requests to a web UI
    """
    def __init__(self, AdminClient_driver):
        #VdevClient_driver => self.vdev_client.driver in BaseVdevClientJSON
        self.driver = AdminClient_driver.driver
        self.wait = AdminClient_driver.wait

    def protect_disk(self, client=None, disk=None, protocol=None, **kwargs):
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        driver.find_element_by_xpath("//a[contains(.,'Client Agents')]").click()
        driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
        time.sleep(1)
        #Select the Client
        driver.find_element_by_xpath(".//*[contains(text(), '" + client + "')]").click()
        #LOG.info('===The Actual_Category is "%s".===', Actual_Category)      
        #Create protection 
        driver.find_element_by_xpath("//button[@data-template-url='views/client/create-protection-menu.tpl.html']").click()
        driver.find_element_by_xpath("//a[contains(.,'Single Client')]").click()
        time.sleep(1)
        #Select disk
        driver.find_element_by_xpath("//fieldset/div/div/div/div/span/span").click()
        driver.find_element_by_xpath("//span[contains(.,'" + disk + "')]").click()
        if kwargs['existed'] is not None:
            driver.find_element_by_xpath("//label[contains(.,'Use Existing')]").click()
            driver.find_element_by_xpath("//span[@class='ui-select-placeholder text-muted ng-binding']").click()
            driver.find_element_by_xpath("//span[contains(.,'" + kwargs['existed'] + "')]").click()
        else:
            #Select Protocol
            driver.find_element_by_xpath("//span[@class='ui-select-placeholder text-muted ng-binding']").click()
            driver.find_element_by_xpath("//span[contains(.,'" + protocol + "')]").click()
        #set parameter
        stype = None
        if kwargs['schedule_type'] == 'Day(s)':
            stype = 'day'
        elif kwargs['schedule_type'] == 'Hour(s)':
            stype = 'typeHo'
        else:
            stype = 'typeMn'
        driver.find_element_by_xpath("//select[@ng-model='protectionForm.type']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//option[@label='" + kwargs['schedule_type'] + "']").click()
        driver.find_element_by_xpath("//input[@ng-model='protectionForm." + stype + "']").clear()
        driver.find_element_by_xpath("//input[@ng-model='protectionForm." + stype + "']").send_keys(kwargs['interval_num'])
        if kwargs['trigger_sync'] == False:
            driver.find_element_by_xpath("//button[@class='btn btn-default btn-toggle blue ng-pristine ng-untouched ng-valid active']").click()
        else:
            driver.find_element_by_xpath("//select[@ng-model='sizeInput.unit']").click()
            driver.find_element_by_xpath("//option[@label='"+ kwargs['watermark_unit'] +"']").click()
            driver.find_element_by_xpath("//input[@ng-model='sizeInput.value']").clear()
            driver.find_element_by_xpath("//input[@ng-model='sizeInput.value']").send_keys(kwargs['watermark_value'])
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.wait_for_return_message("The request to create a protection policy has been submitted. Check back later.")
        # Check if protected disk status show "Online"
        for i in range(30):
            try:
                driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
                time.sleep(1)
                driver.find_element_by_xpath(".//*[contains(text(), '" + client + "')]").click()
                time.sleep(1)
                if driver.find_element_by_xpath("//span[contains(.,'Online')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: assert False, "Time Out, the expected message didn't show up."

    def protect_multi_disks(self, client=None, disk=None, protocol=None, nums=None):
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        driver.find_element_by_xpath("//a[contains(.,'Client Agents')]").click()
        driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//button[@data-template-url='views/client/create-protection-menu.tpl.html']").click()
        driver.find_element_by_xpath("//a[contains(.,'Multiple Clients')]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//input[@ng-model='selectAllChecked']").click()
        #Select disk
        driver.find_element_by_css_selector("span.ui-select-match-text.pull-left").click()
        time.sleep(1)
        driver.find_element_by_xpath("//span[contains(.,'" + disk + "')]").click()
        #Select protocol
        driver.find_element_by_xpath("//span[@class='ui-select-placeholder text-muted ng-binding']").click()
        driver.find_element_by_xpath("//span[contains(.,'" + protocol + "')]").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.wait_for_return_message("The protection policy for " + nums + " clients has been created.")
        # Check if protected disk status show "Online"
        for i in range(30):
            try:
                driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
                time.sleep(1)
                driver.find_element_by_xpath(".//*[contains(text(), '" + client + "')]").click()
                time.sleep(1)
                if driver.find_element_by_xpath("//span[contains(.,'Online')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: assert False, "Time Out, the expected message didn't show up."

    def update_protection(self, client=None, disk=None, **kwargs):
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        driver.find_element_by_xpath("//a[contains(.,'Client Agents')]").click()
        driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
        time.sleep(1)
        driver.find_element_by_xpath(".//*[contains(text(), '" + client + "')]").click()
        #LOG.info('===The Actual_Category is "%s".===', Actual_Category)       
        #Select disk
        driver.find_element_by_xpath(".//*[contains(text(), '" + disk + "')]").click()
#        driver.find_element_by_xpath(".//*[contains(text(), 'Disk 0')]").click()
        #Update policy
        driver.find_element_by_xpath("//button[contains(@ng-click,'updateProtection(gridOptions.selectedRows[0], gridProtectedOptions.selectedRows, true)')]").click()
        stype = None 
        if kwargs['schedule_type'] == 'Day(s)':
            stype = 'day'
        elif kwargs['schedule_type'] == 'Hour(s)':
            stype = 'typeHo'
        else:
            stype = 'typeMn' 
        driver.find_element_by_xpath("//select[@ng-model='protectionForm.type']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//option[@label='" + kwargs['schedule_type'] + "']").click()
        driver.find_element_by_xpath("//input[@ng-model='protectionForm." + stype + "']").clear()
        driver.find_element_by_xpath("//input[@ng-model='protectionForm." + stype + "']").send_keys(kwargs['interval_num'])
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.wait_for_return_message("The request to update the protection policy has been submitted. Check back later.")

    def suspend_resume_protection(self, client=None, disk=None, action=None):
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        driver.find_element_by_xpath("//a[contains(.,'Client Agents')]").click()
        driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
        time.sleep(1)
        #Select the Client
        driver.find_element_by_xpath(".//*[contains(text(), '" + client + "')]").click()
        #Select disk
        driver.find_element_by_xpath(".//*[contains(text(), '" + disk + "')]").click()
#        driver.find_element_by_xpath(".//*[contains(text(), 'Disk 0')]").click()
        #Suspend sync
        driver.find_element_by_xpath("//button[@data-template-url='views/client-agent/protection-menu.tpl.html']").click()
        time.sleep(1)
        if action == "suspend":
           driver.find_element_by_xpath("//a[contains(.,'Suspend Synchronization')]").click()
           driver.find_element_by_xpath("//button[@type='submit']").click()
           self.wait_for_return_message("The request to suspend synchronization has been submitted.")
        else:
           driver.find_element_by_xpath("//a[contains(.,'Resume Synchronization')]").click()
           driver.find_element_by_xpath("//button[@type='submit']").click()
           self.wait_for_return_message("The request to resume synchronization has been submitted.")
        
        time.sleep(2)
        driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
        time.sleep(2)

    def remove_protected_disk(self, client=None, disk=None):
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        driver.find_element_by_xpath("//a[contains(.,'Client Agents')]").click()
        driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
        time.sleep(1)
        #Select the Client
        driver.find_element_by_xpath(".//*[contains(text(), '" + client + "')]").click()
        #Select disk
        driver.find_element_by_xpath(".//*[contains(text(), '" + disk + "')]").click()
        #Remove protection
        driver.find_element_by_xpath("(//button[@type='button'])[9]").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.wait_for_return_message("The request to delete the protection policy has been submitted.")
        # Check if protected disk is removed
        for i in range(30):
            try:
                driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
                time.sleep(1)
                driver.find_element_by_xpath(".//*[contains(text(), '" + client + "')]").click()
                time.sleep(1)
                if not re.search(r"^[\s\S]*//span\[contains\(\.,'Online'\)\][\s\S]*$", driver.find_element_by_css_selector("BODY").text): break
            except: pass
            time.sleep(1)
        else: assert False, "Time Out, the expected message didn't show up."   

    def sync_mirror(self, client=None, disk=None):
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        driver.find_element_by_xpath("//a[contains(.,'Client Agents')]").click()
        driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
        time.sleep(1)
        #Select the Client
        driver.find_element_by_xpath(".//*[contains(text(), '" + client + "')]").click()
        #Select disk
        driver.find_element_by_xpath(".//*[contains(text(), '" + disk + "')]").click()
        #Start Sync mirror
        driver.find_element_by_xpath("//button[@data-template-url='views/client-agent/protection-menu.tpl.html']").click()
        driver.find_element_by_xpath("//a[contains(.,'Start Synchronization')]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='submit']").click()      
        self.wait_for_return_message("The request to start synchronization has been submitted.")
        time.sleep(2)
        driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
        time.sleep(1)

    def take_snapshot(self, client=None, disk=None):
        driver = self.driver
        driver.find_element_by_xpath("//span[contains(.,'Manage')]").click()
        driver.find_element_by_xpath("//a[contains(.,'Client Agents')]").click()
        driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
        time.sleep(1)
        #Select the Client
        driver.find_element_by_xpath(".//*[contains(text(), '" + client + "')]").click()
        #Select disk
        driver.find_element_by_xpath(".//*[contains(text(), '" + disk + "')]").click()
        #Take snapshot
        driver.find_element_by_xpath("//button[@data-template-url='views/client-agent/protection-menu.tpl.html']").click()
        driver.find_element_by_xpath("//a[contains(.,'Create TimeMark')]").click()
        #Check if the refresh button is clickable first
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='submit']")))
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.wait_for_return_message("The request to create a TimeMark has been submitted")
    
    def wait_for_sync_finished(self, client):
        # Check if protected disk activity show "Wait for next sync"
        for i in range(30):
            try:
                self.driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
                time.sleep(1)
                self.driver.find_element_by_xpath(".//*[contains(text(), '" + client + "')]").click()
                time.sleep(1)
                if self.driver.find_element_by_xpath(".//*[contains(text(), 'Waiting for next sync')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: assert False, "Time Out, the expected message didn't show up."

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

