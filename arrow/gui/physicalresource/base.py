# Author                                : Johnny Wu
# Created                               : 2016/05/09
# Last Modified                         : 
# Version                               : 1.0

from oslo_log import log as logging
import arrow.test
from arrow import config

CONF = config.CONF
LOG = logging.getLogger(__name__)

class BasePhysicalResourceTest(arrow.test.BaseTestCase):
    """Base test case class for all Physical Resource GUI tests."""

    #credential type included "superadmin", "admin" and "user"
    credentials = ['superadmin']

    @classmethod
    def setUpClass(cls):
        super(BasePhysicalResourceTest, cls).setUpClass()
        cls.vdev_client = cls.os.vdev_client
        cls.pdev_client = cls.os.pdev_client
        #os = manager; when you setup credentials and setup client manger, then you can control vdev_client service

    @classmethod
    def tearDownClass(cls):
        #cls.clear_snapshots()
        #cls.clear_vdevs()
        #todo: Shift  remove_server() to another client, but not vdev_client 
        cls.vdev_client.remove_server(CONF.fss.ip)
        super(BasePhysicalResourceTest, cls).tearDownClass()

    @classmethod
    def prepare_pdev(cls, acsl=None, category=None):
         cls.pdev_client.prepare_pdev(acsl, category)

    #@classmethod
    #def clear_vdevs(cls):
    #    for vdev in cls.vdevs:
    #        try:
    #            cls.vdev_client.delete_vdev(vdev)
    #        except Exception:
    #            pass

        #for volume in cls.volumes:
        #    try:
        #        cls.volumes_client.wait_for_resource_deletion(volume['id'])
        #    except Exception:
        #        pass
    #@classmethod
    #def clear_snapshots(cls):
    #    for snapshot in cls.snapshots:
    #        try:
    #            cls.snapshots_client.delete_snapshot(snapshot['id'])
    #        except Exception:
    #            pass
