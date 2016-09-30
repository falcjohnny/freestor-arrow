# -*- coding: utf-8 -*-
# Author                                : Johnny Wu
# Created                               : 2016/05/09
# Last Modified                         : 
# Version                               : 1.0

from oslo_log import log as logging
from arrow.gui.clientagents import base
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from arrow import config
from arrow import test
import unittest
import random, time

LOG = logging.getLogger("DiskProtectionTest")

class DiskProtectionTest(base.BaseClientAgentsTest):
    @classmethod
    def setUpClass(cls):
        super(DiskProtectionTest, cls).setUpClass()
        #cls.client = cls.vdev_client
        cls.admin = cls.admin_client
        cls.cagent = cls.cagent_client
        cls.admin.login_server()
        cls.admin.add_server(cls.os.fss_provider[0], cls.os.fss_provider[1], cls.os.fss_provider[2])
        cls.client = "JOHNNY-WIN2012"
        cls.disk = "Disk 1"
        cls.protocol = 'iSCSI'
        cls.params = {'existed':None, 'interval_num': 2,'schedule_type': 'Hour(s)','trigger_sync': False, 'watermark_value': 1, 'watermark_unit': 'GB'}

    def setUp(self):
        LOG.info('===Start running test "%s".===', self._testMethodName)

    def test_01_protect_disk(self):
        self.protect_disk(self.client, self.disk, self.protocol, **self.params)
        # Check if protected disk activity show "Wait for next sync"
        self.cagent.wait_for_sync_finished(self.client)
    
    def test_02_update_protection_policy(self):
        self.cagent.update_protection(self.client, self.disk, **self.params)

    def test_03_suspend_protection(self):
        action = "suspend"
        self.cagent.suspend_resume_protection(self.client, self.disk, action)
        #Verify if the mirror disk is suspended 
        self.cagent.driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
        time.sleep(1)
        self.cagent.driver.find_element_by_xpath(".//*[contains(text(), '" + self.client + "')]").click()
        time.sleep(1)
        self.assertTrue(self.cagent.is_element_present(By.XPATH, ".//*[contains(text(), 'Synchronization suspended')]"))
    
    def test_04_resume_protection(self):
        action = "resume"
        self.cagent.suspend_resume_protection(self.client, self.disk, action)        
        #self.assertTrue(self.client.is_element_present(By.XPATH, ".//*[contains(text(), 'Protection suspended')]"))

    def test_05_remove_protected_disk(self):
        self.cagent.remove_protected_disk(self.client, self.disk)
    
    @classmethod
    def tearDownClass(cls):
        cls.remove_protected_disk(cls.client, cls.disk)
        cls.sanclient_client.unassign_all_from_sanclient(cls.client)
        force = True
        cls.vdev_client.delete_vdev(cls.client, force)
        super(DiskProtectionTest, cls).tearDownClass()

if __name__ == "__main__":
    unittest.main()
    #import xmlrunner
    #unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
