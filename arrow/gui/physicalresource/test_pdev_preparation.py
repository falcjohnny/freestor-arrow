# -*- coding: utf-8 -*-
# Author                                : Johnny Wu
# Created                               : 2016/05/09
# Last Modified                         : 
# Version                               : 1.0

from oslo_log import log as logging
from arrow.gui.physicalresource import base
from selenium.webdriver.common.by import By
from arrow import config
from arrow import test
import unittest
import random

LOG = logging.getLogger("PdevPreparationTest")

class PdevPreparationTest(base.BasePhysicalResourceTest):
    @classmethod
    def setUpClass(cls):
        super(PdevPreparationTest, cls).setUpClass()
        cls.client = cls.vdev_client
        cls.pdev = cls.pdev_client
        cls.client.login_server()
        cls.client.add_server(cls.os.fss_provider[0], cls.os.fss_provider[1], cls.os.fss_provider[2])
        #cls.vdevs = []
        #cls.vdev_name = 'SANDisk-' + str(random.randrange(1, 1024))
        #cls.vdevs.append(cls.vdev_name)

    def setUp(self):
        LOG.info('===Start running test "%s".===', self._testMethodName)

    def test_prepare_pdev(self):
        #params = {self.name_field: vol_name,'volume_type': 'FSS'}
        #params = {}
        acsl = "0:0:3:0"
        category = "Virtual" #"Unassigned"
        self.pdev.prepare_pdev(acsl,category)
        #self.assertTrue(self.client.is_element_present(By.XPATH, ".//*[contains(text(), '" + self.vdev_name + "')]"))
       # self.snapshot.create_snapshot(None,self.vdev_name)
    @classmethod
    def tearDownClass(cls):
        super(PdevPreparationTest, cls).tearDownClass()
        #self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
    #import xmlrunner
    #unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
