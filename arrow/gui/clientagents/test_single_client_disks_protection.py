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

LOG = logging.getLogger("SingleClientDisksProtectionTest")

class SingleClientDisksProtectionTest(base.BaseClientAgentsTest):
    @classmethod
    def setUpClass(cls):
        super(SingleClientDisksProtectionTest, cls).setUpClass()
        #cls.client = cls.vdev_client
        cls.admin = cls.admin_client
        cls.cagent = cls.cagent_client
        cls.admin.login_server()
        cls.admin.add_server(cls.os.fss_provider[0], cls.os.fss_provider[1], cls.os.fss_provider[2])
        cls.client = "RH15-123" #"JOHNNY-WIN2012"
        cls.numdisk = 3
        cls.protocol = 'iSCSI'
        cls.params = {'client_os': 'linux','existed':None, 'interval_num': 2,'schedule_type': 'Hour(s)','trigger_sync': None, 'watermark_value': 1, 'watermark_unit': 'GB'}
        # Note: "trigger_sync" has False,True and None; None for Linux client protection has no "trigger_sync" option 
    def setUp(self):
        LOG.info('===Start running test "%s".===', self._testMethodName)

    def test_protect_disks(self):
        self.protect_single_client_disks(self.client, self.numdisk, self.protocol, **self.params)
        # Check if protected disk activity show "Wait for next sync"
        #self.cagent.wait_for_sync_finished(self.client)
    
    @classmethod
    def tearDownClass(cls):
        cls.remove_all_single_client_disks(cls.client, cls.numdisk, **cls.params)
        cls.sanclient_client.unassign_all_from_sanclient(cls.client)
        force = True
        cls.vdev_client.delete_all_vdevs( force)
        super(SingleClientDisksProtectionTest, cls).tearDownClass()

if __name__ == "__main__":
    unittest.main()
    #import xmlrunner
    #unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
