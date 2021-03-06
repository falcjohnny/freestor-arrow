# Author                                : Johnny Wu
# Created                               : 2016/05/09
# Last Modified                         : 
# Version                               : 1.0

from oslo_log import log as logging
import arrow.test
from arrow import config

CONF = config.CONF
LOG = logging.getLogger(__name__)

class BaseClientAgentsTest(arrow.test.BaseTestCase):
    """Base test case class for all Client Agents GUI tests."""

    #credential type included "superadmin", "admin" and "user"
    credentials = ['superadmin']

    @classmethod
    def setUpClass(cls):
        super(BaseClientAgentsTest, cls).setUpClass()
        cls.admin_client = cls.os.admin_client
        cls.vdev_client = cls.os.vdev_client
        cls.cagent_client = cls.os.cagent_client
        cls.sanclient_client = cls.os.sanclient_client
        #os = manager; when you setup credentials and setup client manger, then you can control vdev_client service

    @classmethod
    def tearDownClass(cls):
        #cls.clear_snapshots()
        #cls.clear_vdevs()
        #todo: Shift  remove_server() to another client, but not vdev_client 
        cls.admin_client.remove_server(CONF.fss.ip)
        super(BaseClientAgentsTest, cls).tearDownClass()

    @classmethod
    def protect_disk(cls, client=None, disk=None, protocol=None, **kwargs):
         #if not kwargs['existed']: 
         #   kwargs['existed'] = None
         cls.cagent_client.protect_disk(client, disk, protocol, **kwargs)

    @classmethod
    def protect_single_client_disks(cls, client=None, numdisk=None, protocol=None, **kwargs):
         if kwargs['client_os'] == 'windows':
            for i in range(0,numdisk):
                disk = 'Disk ' + str(i)
                cls.cagent_client.protect_disk(client, disk, protocol, **kwargs)
         elif kwargs['client_os'] == 'linux':
            for i in range(97,97 + numdisk): #97=char "a"
                disk = '/dev/sd' + chr(i)
                cls.cagent_client.protect_disk(client, disk, protocol, **kwargs)
         else:
            pass

    @classmethod
    def protect_multiple_disks(cls, client = None, disk=None, protocol=None, nums=None):
         cls.cagent_client.protect_multi_disks(client, disk, protocol, nums)
    
    @classmethod
    def update_protection(cls, client=None, disk=None, **kwargs):
         cls.cagent_client.update_protection(client, disk, **kwargs)

    @classmethod
    def suspend_resume_protection(cls, client=None, disk=None, action=None):
         cls.cagent_client.suspend_resume_protection(client, disk, action)

    @classmethod
    def sync_mirror(cls, client=None, disk=None):
         cls.cagent_client.sync_mirror(client, disk)
  
    @classmethod
    def take_snapshot(cls, client=None, disk=None):
         cls.cagent_client.take_snapshot(client, disk)   
    
    @classmethod
    def remove_protected_disk(cls, client=None, disk=None):
         cls.cagent_client.remove_protected_disk(client, disk)

    @classmethod
    def remove_single_client_disks(cls, client=None, numdisk=None, **kwargs):
         if kwargs['client_os'] == 'windows':
            for i in range(0,numdisk):
                disk = 'Disk ' + str(i)
                cls.cagent_client.remove_protected_disk(client, disk)
         elif kwargs['client_os'] == 'linux':
            for i in range(97,97 + numdisk): #97=char "a"
                disk = '/dev/sd' + chr(i)
                cls.cagent_client.remove_protected_disk(client, disk)
         else:
            pass
    
    @classmethod
    def remove_all_single_client_disks(cls, client=None, numdisk=None, **kwargs):
         cls.cagent_client.remove_all_single_client_protected_disk(client)
         if kwargs['client_os'] == 'windows':
            LOG.info('===The single OS is "%s"  ===', kwargs['client_os'])
            for i in range(0,numdisk):
                disk = 'Disk ' + str(i)
                LOG.info('===Check if the protected disk "%s" is removed.===', disk) 
                for j in range(20):
                    try:
                        driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
                        time.sleep(1)
                        driver.find_element_by_xpath(".//*[contains(text(), '" + client + "')]").click()
                        time.sleep(1)
                        if not re.search(r"^[\s\S]*//span\[contains\(\.,'" + disk + "'\)\][\s\S]*$", driver.find_element_by_css_selector("BODY").text): break
                    except: pass
         elif kwargs['client_os'] == 'linux':
            LOG.info('===The single client OS is "%s"  ===', kwargs['client_os'])  
            for i in range(97,97 + numdisk): #97=char "a"
                disk = '/dev/sd' + chr(i)
                LOG.info('===Check if the protected disk "%s" is removed.===', disk)  
                for j in range(20):
                    try:
                        driver.find_element_by_xpath("//button[@ng-click='hardRefresh();']").click()
                        time.sleep(1)
                        driver.find_element_by_xpath(".//*[contains(text(), '" + client + "')]").click()
                        time.sleep(1)
                        if not re.search(r"^[\s\S]*//span\[contains\(\.,'" + disk + "'\)\][\s\S]*$", driver.find_element_by_css_selector("BODY").text): break
                    except: pass
         else:
            pass

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
