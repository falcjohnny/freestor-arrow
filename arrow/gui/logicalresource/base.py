# Author                                : Johnny Wu
# Created                               : 2016/05/09
# Last Modified                         : 
# Version                               : 1.0

from oslo_log import log as logging
import arrow.test
from arrow import config

CONF = config.CONF
LOG = logging.getLogger(__name__)

class BaseLogicalResourceTest(arrow.test.BaseTestCase):
    """Base test case class for all Logical Resource GUI tests."""

    #credential type included "superadmin", "admin" and "user"
    credentials = ['superadmin']

    @classmethod
    def setUpClass(cls):
        super(BaseLogicalResourceTest, cls).setUpClass()
        cls.admin_client = cls.os.admin_client
        cls.vdev_client = cls.os.vdev_client
        cls.snapshot_client = cls.os.snapshot_client
        cls.mirror_client = cls.os.mirror_client
        cls.cache_client = cls.os.cache_client
        cls.hotzone_client = cls.os.hotzone_client
        cls.timemark_client = cls.os.timemark_client

    @classmethod
    def tearDownClass(cls):
        #cls.clear_snapshots()
        cls.clear_vdevs()
        #todo: Shift  remove_server() to another client, but not vdev_client 
        cls.admin_client.remove_server(CONF.fss.ip)
        super(BaseLogicalResourceTest, cls).tearDownClass()

    @classmethod
    def create_vdev(cls, size=None, **kwargs):
         cls.vdev_client.create_vdev(size, **kwargs)

    @classmethod
    def update_vdev(cls, vdev_name=None, new_vname=None, new_size=None):
         cls.vdev_client.update_vdev(vdev_name, new_vname, new_size)

    @classmethod
    def delete_vdev(cls, vdev_name):
         cls.vdev_client.delete_vdev(vdev_name)

    @classmethod
    def create_snapshot(cls, snap_size=None, vname=None):
         cls.snapshot_client.create_snapshot(snap_size,vname)

    @classmethod
    def delete_snapshot(cls, vname=None):
         cls.snapshot_client.delete_snapshot(vname)

    @classmethod
    def create_mirror(cls, vname=None, **kwargs):
         cls.mirror_client.create_mirror(vname, **kwargs)

    @classmethod
    def delete_mirror(cls, vname=None):
         cls.mirror_client.delete_mirror(vname)

    @classmethod
    def create_cache(cls, vname=None):
         cls.cache_client.create_cache(vname)

    @classmethod
    def delete_cache(cls, vname=None):
         cls.cache_client.delete_cache(vname)

    @classmethod
    def create_hotzone(cls, vname=None):
         cls.hotzone_client.create_hotzone(vname)

    @classmethod
    def delete_hotzone(cls, vname=None):
         cls.hotzone_client.delete_hotzone(vname)

    @classmethod
    def clear_vdevs(cls):
        for vdev in cls.vdevs:
            try:
                cls.vdev_client.delete_vdev(vdev)
            except Exception:
                pass

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
