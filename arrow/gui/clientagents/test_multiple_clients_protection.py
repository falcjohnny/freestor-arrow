# -*- coding: utf-8 -*-
# Author                                : Johnny Wu
# Created                               : 2016/08/25
# Last Modified                         : 
# Version                               : 1.0

from oslo_log import log as logging
from arrow.gui.clientagents import base
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from arrow import config
from arrow import test
import unittest
import random

LOG = logging.getLogger("MultiClientsProtectionTest")

class MultiClientsProtectionTest(base.BaseClientAgentsTest):
    @classmethod
    def setUpClass(cls):
        super(MultiClientsProtectionTest, cls).setUpClass()
        #cls.client = cls.vdev_client
        cls.admin = cls.admin_client
        cls.cagent = cls.cagent_client
        cls.vdev = cls.vdev_client
        cls.sanclient = cls.sanclient_client
        cls.admin.login_server()
        cls.admin.add_server(cls.os.fss_provider[0], cls.os.fss_provider[1], cls.os.fss_provider[2])
        cls.client = ["JOHNNY-WIN2012[admin_johnny_local]","J-WIN2012-1[admin_johnny_local]"]
        cls.disk = "Disk 1"
        cls.nums_client = '2'
        cls.protocol = 'iSCSI'
        cls.params = {'interval_num': 2,'schedule_type': 'Hour(s)'}
        #cls.vdev_name = 'SANDisk-' + str(random.randrange(1, 1024))
        #cls.vdevs.append(cls.vdev_name)

    def setUp(self):
        LOG.info('===Start running test "%s".===', self._testMethodName)

    def test_01_protect_windows_disks(self):
        #params = {self.name_field: vol_name,'volume_type': 'FSS'}
        #params = {}
        self.protect_multiple_disks(self.client[0], self.disk, self.protocol, self.nums_client)
        #self.assertTrue(self.client.is_element_present(By.XPATH, ".//*[contains(text(), '" + ? + "')]"))
    
 #   def test_05_remove_protected_disk(self):
 #       self.cagent.remove_protected_disk(self.client, self.disk)
    
    @classmethod
    def tearDownClass(cls):
        cls.remove_protected_disk(cls.client[0], cls.disk)
        cls.remove_protected_disk(cls.client[1], cls.disk)
        cls.sanclient_client.unassign_all_from_sanclient(cls.client[0])
        cls.sanclient_client.unassign_all_from_sanclient(cls.client[1])
        force = True
        cls.vdev_client.delete_all_vdevs(force)
        super(MultiClientsProtectionTest, cls).tearDownClass()
        #self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
    #import xmlrunner
    #unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
