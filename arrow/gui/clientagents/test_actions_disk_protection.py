# -*- coding: utf-8 -*-
# Author                                : Johnny Wu
# Created                               : 2016/08/24
# Last Modified                         : 
# Version                               : 1.0

from oslo_log import log as logging
from arrow.gui.clientagents import base
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from arrow import config
from arrow import test
import unittest, time
import random

LOG = logging.getLogger("ActionsDiskProtectionTest")

class ActionsDiskProtectionTest(base.BaseClientAgentsTest):
    @classmethod
    def setUpClass(cls):
        super(ActionsDiskProtectionTest, cls).setUpClass()
        #cls.client = cls.vdev_client
        cls.admin = cls.admin_client
        cls.cagent = cls.cagent_client
        cls.vdev = cls.vdev_client
        cls.sanclient = cls.sanclient_client
        cls.admin.login_server()
        cls.admin.add_server(cls.os.fss_provider[0], cls.os.fss_provider[1], cls.os.fss_provider[2])
        cls.client = "JOHNNY-WIN2012"
        cls.disk = "Disk 1"
        #cls.exist_dsk = ''
        cls.protocol = 'iSCSI'
        cls.params = {'existed':None, 'interval_num': 2,'schedule_type': 'Hour(s)','trigger_sync': False, 'watermark_value': 1, 'watermark_unit': 'GB'}
        cls.protect_disk(cls.client, cls.disk, cls.protocol, **cls.params)
        # Check if protected disk activity show "Wait for next sync"
        cls.cagent.wait_for_sync_finished(cls.client)
        """for i in range(30):
            try:
                cls.cagent.driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
                time.sleep(1)
                cls.cagent.driver.find_element_by_xpath(".//*[contains(text(), '" + cls.client + "')]").click()
                time.sleep(1)
                if cls.cagent.driver.find_element_by_xpath(".//*[contains(text(), 'Wait for next sync')]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: assert False, "Time Out, the expected message didn't show up."
        """
    def setUp(self):
        LOG.info('===Start running test "%s".===', self._testMethodName)

    def test_sync_mirror_disk(self):
        self.cagent.sync_mirror(self.client, self.disk)
        time.sleep(2)
        #self.assertTrue(self.client.is_element_present(By.XPATH, ".//*[contains(text(), '" + ? + "')]"))
    
    def test_take_snapshot(self):
        # Check if protected disk activity show "Wait for next sync" first.
        self.cagent.wait_for_sync_finished(self.client)
        self.cagent.take_snapshot(self.client, self.disk)
        time.sleep(2)
        #Verify if the snapshot has been taken or not
        self.cagent.driver.find_element_by_xpath("//span[contains(.,'Monitor')]").click()
        self.cagent.driver.find_element_by_xpath("//a[contains(.,'Client View')]").click()
        time.sleep(1)
        self.cagent.driver.find_element_by_xpath("//span[contains(.,'" + self.client + "')]").click()
        self.cagent.driver.find_element_by_xpath("//a[contains(.,'TimeMarks')]").click()
        element = self.cagent.wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(@ng-click,'loadSnapshot();')]")))
        #time.sleep(5)
        self.cagent.driver.find_element_by_xpath("//button[contains(@ng-click,'loadSnapshot();')]").click()
        time.sleep(1)
        self.assertTrue(self.cagent.is_element_present(By.XPATH, "//div[@id='center']/div/div[2]/div[2]/div/div/div[2]/div"))
   
    @classmethod
    def tearDownClass(cls):
        cls.remove_protected_disk(cls.client, cls.disk)
        cls.sanclient_client.unassign_all_from_sanclient(cls.client)
        force = True
        cls.vdev_client.delete_vdev(cls.client, force)
        super(ActionsDiskProtectionTest, cls).tearDownClass()

if __name__ == "__main__":
    unittest.main()
    #import xmlrunner
    #unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
