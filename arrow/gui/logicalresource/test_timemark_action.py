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

LOG = logging.getLogger("TimemarkCreationTest")

class TimemarkCreationTest(base.BaseLogicalResourceTest):
    @classmethod
    def setUpClass(cls):
        super(TimemarkCreationTest, cls).setUpClass()
        cls.admin = cls.admin_client
        cls.client = cls.vdev_client
        cls.timemark = cls.timemark_client
        cls.admin.login_server()
        cls.admin.add_server(cls.os.fss_provider[0], cls.os.fss_provider[1], cls.os.fss_provider[2])
        cls.vdevs = []
        cls.vdev_name = 'SANDisk-' + str(random.randrange(1, 1024))
        cls.vdevs.append(cls.vdev_name)
    
    def setUp(self):
        LOG.info('===Start running test "%s".===', self._testMethodName)

    def test_create_timemark(self):
        vdev_params = {'vdev_name': self.vdev_name,'vdev_type': 'Thick'}
        self.client.create_vdev(None,**vdev_params)
        self.assertTrue(self.client.is_element_present(By.XPATH, ".//*[contains(text(), '" + self.vdev_name + "')]"))
        params = {'automatic':{'enabled':False}}
        #params = {'automatic':{'enabled':true,'initialtime':'2011-07-20 12:00','interval':'1H','snapshotnotification':{'enabled':true,'frequency':5}}

        self.timemark.create_timemark(self.vdev_name,**params)

    """def test_delete_timemark(self):
        self.timemark.delete_timemark(self.vdev_name)
    """
    @classmethod
    def tearDownClass(cls):
        super(TimemarkCreationTest, cls).tearDownClass()

if __name__ == "__main__":
    unittest.main()
    #import xmlrunner
    #unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
