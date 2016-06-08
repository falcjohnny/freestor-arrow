# -*- coding: utf-8 -*-
# Author                                : Johnny Wu
# Created                               : 2016/05/09
# Last Modified                         : 
# Version                               : 1.0

from oslo_log import log as logging
from arrow.gui.administration import base
from selenium.webdriver.common.by import By
from arrow import config
from arrow import test
import unittest
import random

LOG = logging.getLogger("CustomerActionsTest")

class CustomerActionsTest(base.BaseAdministrationTest):
    @classmethod
    def setUpClass(cls):
        super(CustomerActionsTest, cls).setUpClass()
        cls.admin = cls.admin_client
        #cls.client = cls.vdev_client
        cls.admin.login_server()
        cls.admin.add_server(cls.os.fss_provider[0], cls.os.fss_provider[1], cls.os.fss_provider[2])
        cls.customer_name = "test"
        cls.domain = "test.com"

    def setUp(self):
        LOG.info('===Start running test "%s".===', self._testMethodName)

    def test_create_customer(self):
        #params = {self.name_field: vol_name,'volume_type': 'FSS'}
        #params = {}
        self.create_customer(self.customer_name, self.domain)
        #self.assertTrue(self.client.is_element_present(By.XPATH, ".//*[contains(text(), '" + self.vdev_name + "')]"))
    def test_delete_customer(self):
        self.remove_customer(self.customer_name)

    @classmethod
    def tearDownClass(cls):
        super(CustomerActionsTest, cls).tearDownClass()

if __name__ == "__main__":
    unittest.main()
    #import xmlrunner
    #unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
