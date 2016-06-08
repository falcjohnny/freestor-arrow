# -*- coding: utf-8 -*-
# Author                                : Johnny Wu
# Created                               : 2016/05/09
# Last Modified                         : 
# Version                               : 1.0

from arrow import client
from arrow import config
#from arrow.common import credentials
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import six
import unittest, time, re

CONF = config.CONF

class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # It should never be overridden by descendants
        if hasattr(super(BaseTestCase, cls), 'setUpClass'):
            super(BaseTestCase, cls).setUpClass()
        #try:
            cls.setup_credentials() # get login credentials from arrow.conf file
        
        #except Exception:
        #    etype, value, trace = sys.exc_info()
        #    LOG.info("%s raised in %s.setUpClass. Invoking tearDownClass." % (
        #             etype, cls.__name__))
        #    cls.tearDownClass()
        #    try:
        #            six.reraise(etype, value, trace)
        #    finally:
        #        del trace  # to avoid circular refs
         
    @classmethod
    def tearDownClass(cls):
        cls.os.admin_client.driver.quit()
        #pass   

    @classmethod
    def setup_credentials(cls):
        """Login FMS"""
        for credentials_type in cls.credentials:
            # This may raise an exception in case credentials are not available
            # In that case we want to let the exception through and the test
            # fail accordingly
            # Check if credentials_type is string type or not
            if isinstance(credentials_type, six.string_types):
                manager = cls.get_client_manager(
                    credential_type=credentials_type)
                #setattr(cls, 'os_%s' % credentials_type, manager)
                if credentials_type == 'superadmin':
                    cls.os = manager

    @classmethod
    def get_client_manager(cls, credential_type=None):
        """Returns an FreeStor client manager

        :returns the created client manager
        :raises skipException: if the requested credentials are not available
        
        #Factory Pattern
            credentials_method = 'get_%s_creds' % credential_type
            if hasattr(cred_provider, credentials_method):
                creds = getattr(cred_provider, credentials_method)()
                #It will go to object cred_provider(python file) and call get_superadmin_creds()
            else:
                raise exceptions.InvalidCredentials(
                    "Invalid credentials type %s" % credential_type)"""
        return client.Manager(credential_type)
