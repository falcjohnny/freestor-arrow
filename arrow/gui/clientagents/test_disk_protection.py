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
        cls.client = "JOHNNY-WIN2012[admin_johnny_local]"
        cls.disk = "disk0"
        cls.protocol = 'iSCSI'
        cls.params = {'interval_num': 2,'schedule_type': 'Days'}
        #cls.vdev_name = 'SANDisk-' + str(random.randrange(1, 1024))
        #cls.vdevs.append(cls.vdev_name)

    def setUp(self):
        LOG.info('===Start running test "%s".===', self._testMethodName)

    def test_01protect_disk(self):
        #params = {self.name_field: vol_name,'volume_type': 'FSS'}
        #params = {}
        self.cagent.protect_disk(self.client, self.disk, self.protocol)
    
    def test_02update_protection_policy(self):
        self.cagent.update_protection(self.client, self.disk, **self.params)
    
    def test_03remove_protected_disk(self):
        self.cagent.remove_protected_disk(self.client, self.disk)
    
    @classmethod
    def tearDownClass(cls):
        super(DiskProtectionTest, cls).tearDownClass()
        #self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
    #import xmlrunner
    #unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
