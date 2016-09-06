# Author                                : Johnny Wu
# Created                               : 2016/05/09
# Last Modified                         : 
# Version                               : 1.0
from arrow import manager
from arrow.services.administration.admin_client import BaseAdminClientJSON
from arrow.services.logicalresource.vdev_client import BaseVdevClientJSON
from arrow.services.logicalresource.snapshot_client import SnapshotClientJSON
from arrow.services.logicalresource.mirror_client import MirrorClientJSON
from arrow.services.logicalresource.cache_client import CacheClientJSON
from arrow.services.logicalresource.hotzone_client import HotzoneClientJSON
from arrow.services.logicalresource.timemark_client import TimemarkClientJSON
from arrow.services.logicalresource.sanclient_client import SANClientClientJSON
from arrow.services.physicalresource.pdev_client import PdevClientJSON
from arrow.services.clientagents.cagent_client import CagentClientJSON
from arrow import config
from oslo_log import log as logging

CONF = config.CONF
LOG = logging.getLogger(__name__)

class Manager(manager.Manager):

    """
    Top level manager for FMS arrow clients
    """
    def __init__(self, credentials=None):
        super(Manager, self).__init__(credentials=credentials)
        #self._set_vdev_clients()
        self._set_admin_clients() 

    def _set_admin_clients(self):
        self.admin_client = BaseAdminClientJSON(
            self.selenium_provider,self.credential_provider,self.fss_provider)
        #Parse the 'driver' attribute of admin_client to other clients you need
        self.vdev_client = BaseVdevClientJSON(self.admin_client.driver,default_vdev_size=CONF.vdev.vdev_size) 
        self.snapshot_client = SnapshotClientJSON(self.admin_client.driver)
        self.mirror_client = MirrorClientJSON(self.admin_client.driver)
        self.timemark_client = TimemarkClientJSON(self.admin_client.driver)
        self.cache_client = CacheClientJSON(self.admin_client.driver)
        self.hotzone_client = HotzoneClientJSON(self.admin_client.driver)
        self.pdev_client = PdevClientJSON(self.admin_client.driver)
        self.cagent_client = CagentClientJSON(self.admin_client.driver)
        self.sanclient_client = SANClientClientJSON(self.admin_client.driver)
