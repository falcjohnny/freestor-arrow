# -*- coding: utf-8 -*-
# Author                                : Johnny Wu
# Created                               : 2016/05/09
# Last Modified                         : 
# Version                               : 1.0

from oslo_log import log as logging
from arrow.gui.clientagents import base
from selenium.webdriver.common.by import By
from arrow import config
from arrow import test
import unittest
import random

LOG = logging.getLogger("ExistedDiskProtectionTest")

class ExistedDiskProtectionTest(base.BaseClientAgentsTest):
    @classmethod
    def setUpClass(cls):
        super(ExistedDiskProtectionTest, cls).setUpClass()
        #cls.client = cls.vdev_client
        cls.admin = cls.admin_client
        cls.cagent = cls.cagent_client
        cls.admin.login_server()
        cls.admin.add_server(cls.os.fss_provider[0], cls.os.fss_provider[1], cls.os.fss_provider[2])
        cls.client = "JOHNNY-WIN2012[admin_johnny_local]"
        cls.disk = "Disk 0"
        cls.exist_dsk = "Disk 1"
        cls.protocol = 'iSCSI'
        cls.params = {'interval_num': 2,'schedule_type': 'Days'}
        cls.cagent.protect_disk(cls.client, cls.disk, cls.protocol)
        cls.cagent.remove_protected_disk(cls.client, cls.disk)

    def setUp(self):
        LOG.info('===Start running test "%s".===', self._testMethodName)

    def test_protect_existed_disk(self):
        self.cagent.protect_disk(self.client, self.disk, self.protocol, self.exist_dsk)
        #self.assertTrue(self.client.is_element_present(By.XPATH, ".//*[contains(text(), '" + ? + "')]"))
    
    @classmethod
    def tearDownClass(cls):
        super(ExistedDiskProtectionTest, cls).tearDownClass()
        #self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
    #import xmlrunner
    #unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
