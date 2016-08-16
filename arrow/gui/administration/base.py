# Author                                : Johnny Wu
# Created                               : 2016/05/18
# Last Modified                         : 
# Version                               : 1.0

from oslo_log import log as logging
import arrow.test
from arrow import config

CONF = config.CONF
LOG = logging.getLogger(__name__)

class BaseAdministrationTest(arrow.test.BaseTestCase):
    """Base test case class for all Physical Resource GUI tests."""

    #credential type included "superadmin", "admin" and "user"
    credentials = ['superadmin']

    @classmethod
    def setUpClass(cls):
        super(BaseAdministrationTest, cls).setUpClass()
        cls.admin_client = cls.os.admin_client

    @classmethod
    def tearDownClass(cls):
        #Done: Shift  remove_server() to another client, but not vdev_client 
        cls.admin_client.remove_server(CONF.fss.ip)
        super(BaseAdministrationTest, cls).tearDownClass()

    @classmethod
    def add_server(cls, server_ip=None, server_user=None, server_passwd=None):
        cls.admin_client.add_server(server_ip,server_user,server_passwd)         

    @classmethod
    def remove_server(cls, fss_server=None):
        cls.admin_client.remove_server(fss_server)

    @classmethod
    def create_customer(cls, customer_name, domain, admin_pass, retype_pass):
        cls.admin_client.create_customer(customer_name, domain, admin_pass, retype_pass)

    @classmethod
    def remove_customer(cls, customer_name):
        cls.admin_client.delete_customer(customer_name)
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
