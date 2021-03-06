# -*- coding: utf-8 -*-
# Author				: Johnny Wu
# Created				: 2016/05/09
# Last Modified		                : 
# Version				: 1.0
from oslo_log import log as logging
from arrow.gui.logicalresource import base
from selenium.webdriver.common.by import By
from arrow import config
from arrow import test
import unittest
import random

LOG = logging.getLogger("CacheCreationTest")

class CacheCreationTest(base.BaseLogicalResourceTest):
    @classmethod
    def setUpClass(cls):
        super(CacheCreationTest, cls).setUpClass()
        cls.admin = cls.admin_client
        cls.client = cls.vdev_client
        cls.cache = cls.cache_client
        cls.admin.login_server()
        cls.admin.add_server(cls.os.fss_provider[0], cls.os.fss_provider[1], cls.os.fss_provider[2])
        cls.vdevs = []
        cls.vdev_name = 'SANDisk-' + str(random.randrange(1, 1024))
        cls.vdevs.append(cls.vdev_name)
    
    def setUp(self):
        LOG.info('===Start running test "%s".===', self._testMethodName)

    def test_create_cache(self):
        #params = {self.name_field: vol_name,'volume_type': 'FSS'}
        #params = {}
        self.client.create_vdev(None,self.vdev_name)
        self.assertTrue(self.client.is_element_present(By.XPATH, ".//*[contains(text(), '" + self.vdev_name + "')]"))
        self.cache.create_cache(self.vdev_name)

    def test_delete_cache(self):
        self.cache.delete_cache(self.vdev_name)
    
    @classmethod
    def tearDownClass(cls):
        super(CacheCreationTest, cls).tearDownClass()

if __name__ == "__main__":
    unittest.main()
    #import xmlrunner
    #unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
