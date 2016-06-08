# Author                                : Johnny Wu
# Created                               : 2016/05/09
# Last Modified                         : 
# Version                               : 1.0
from arrow import config
#from tempest import exceptions

CONF = config.CONF
    #Get config from arrow.conf

class Manager(object):

    """
    Base manager class

    Manager objects are responsible for providing a configuration object
    and a client object for a test case to use in performing actions.
    """

    def __init__(self, credentials=None):
        """
        Get the configuration of freestor-arrow and set them as attributes of Manager object
        """
        #get selenium setup info from configuration file
        self.hub = CONF.selenium.hub_ip
        self.browser = CONF.selenium.browser
        self.selenium_provider = [self.hub,self.browser]
        
        #get FMS login info from configuration file
        self.uri = CONF.identity.uri
        self.user = CONF.identity.username
        self.password = CONF.identity.password
        self.default_user = "superadmin"
        self.default_password = "freestor"
        
        #get FSS login info from configuration file
        self.ip = CONF.fss.ip
        self.fss_user = CONF.fss.user
        self.fss_password = CONF.fss.password
        self.pool_name = CONF.fss.pool_name
        self.fss_provider = [self.ip,self.fss_user,self.fss_password,self.pool_name]

        if credentials is None:
            self.credential_provider = [self.uri,self.user,self.password] #Todo: I should create a credentials class instead
        else:
            self.credential_provider = [self.uri,self.default_user,self.default_password]
        # Check if passed or default credentials are valid
        """if not self.credentials.is_valid():
            raise exceptions.InvalidCredentials()
        """
