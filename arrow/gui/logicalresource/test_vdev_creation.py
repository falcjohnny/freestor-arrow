# -*- coding: utf-8 -*-
# Author                                : Johnny Wu
# Created                               : 2016/05/09
# Last Modified                         : 
# Version                               : 1.0

from oslo_log import log as logging
from arrow.gui.logicalresource import base
from selenium.webdriver.common.by import By
from arrow import config
from arrow import test
import unittest
import random

LOG = logging.getLogger("VdevCreationTest")

class VdevCreationTest(base.BaseLogicalResourceTest):
    @classmethod
    def setUpClass(cls):
        super(VdevCreationTest, cls).setUpClass()
        cls.admin = cls.admin_client
        cls.client = cls.vdev_client
        #cls.snapshot = cls.snapshot_client
        cls.admin.login_server()
        cls.admin.add_server(cls.os.fss_provider[0], cls.os.fss_provider[1], cls.os.fss_provider[2])
        cls.vdevs = []
        cls.vdev_name = 'SANDisk-' + str(random.randrange(1, 1024))
        cls.new_vdev_name = "new-name"
        cls.new_vdev_size = 2
        cls.vdevs.append(cls.vdev_name)

    def setUp(self):
        LOG.info('===Start running test "%s".===', self._testMethodName)

    def test_01_create_vdev(self):
        """Best practice, we shouln't use number(01,02...) for the order of tests, we should do it with "unit test" concept. """ 
        params = {'vdev_name': self.vdev_name,'vdev_type': 'Thick'}
        self.client.create_vdev(None,**params)
        self.assertTrue(self.client.is_element_present(By.XPATH, ".//*[contains(text(), '" + self.vdev_name + "')]"))
       # self.snapshot.create_snapshot(None,self.vdev_name)
        
    def test_02_update_vdev(self):
        self.client.update_vdev(self.vdev_name, self.new_vdev_name, self.new_vdev_size)

    def test_03_delete_vdev(self):
        force = True
        self.client.delete_vdev(self.new_vdev_name, force)
        #self.client.delete_all_vdevs(force)
    
    @classmethod
    def tearDownClass(cls):
        super(VdevCreationTest, cls).tearDownClass()
        #self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
    #import xmlrunner
    #unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
